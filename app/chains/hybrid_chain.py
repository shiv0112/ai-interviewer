import os
import uuid
from typing import List
from pathlib import Path
from datetime import datetime, timedelta

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain.chains import LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.docstore.document import Document
from langchain.schema.runnable import RunnableLambda
from langchain_core.output_parsers import StrOutputParser

from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, Filter, FieldCondition, MatchValue, PointStruct

from app.memory.hybrid_sessions import get_session
from app.config.settings import (
    GEMINI_MODEL,
    GEMINI_TEMP,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    SEARCH_TYPE,
    K,
    MAX_CHUNK_USAGE,
    VECTOR_DIM,
    DEBUG,
    QDRANT_REMOTE_URL,
    HYBRID_EVAL_PROMPT_PATH,
    HYBRID_PROMPT_PATH,
    EMBEDDING_MODEL,
    COLLECTION_NAME
)

# ─── Load API Key ─────────────────────────────────────────────────────────
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise EnvironmentError("Missing GEMINI_API_KEY environment variable.")

# ─── Initialize Embeddings and Qdrant Client ─────────────────────────────
embedding_model = GoogleGenerativeAIEmbeddings(
    model=EMBEDDING_MODEL,
    google_api_key=gemini_api_key
)

qdrant_client = QdrantClient(url=QDRANT_REMOTE_URL, prefer_grpc=False, timeout=30.0)

# ─── Document Ingestion ──────────────────────────────────────────────────
def ingest_documents(session_id: str, docs: List[Document]):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        add_start_index=True
    )
    chunks = splitter.split_documents(docs)

    texts = [doc.page_content for doc in chunks]
    if DEBUG:
        print(f"📥 Ingesting Text \n: {texts}")

    embeddings = embedding_model.embed_documents(texts)

    points = []
    for i, (embedding, doc) in enumerate(zip(embeddings, chunks)):
        payload = {
            "page_content": doc.page_content,
            "session_id": session_id,
            "metadata": {
                **(doc.metadata or {}),
                "chunk_id": f"{session_id}_{i}",
                "created_at": datetime.utcnow().isoformat(),
            }
        }

        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload=payload
        ))

    collections = qdrant_client.get_collections().collections
    if COLLECTION_NAME not in [col.name for col in collections]:
        qdrant_client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=VECTOR_DIM, distance=Distance.COSINE)
        )

    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    if DEBUG:
        print(f"✅ Successfully ingested {len(points)} chunks.")

# ─── Session-Based Retriever ─────────────────────────────────────────────
def get_session_retriever(session_id: str):
    store = QdrantVectorStore(
        client=qdrant_client,
        collection_name=COLLECTION_NAME,
        embedding=embedding_model,
        content_payload_key="page_content"
    )

    return store.as_retriever(
        search_type=SEARCH_TYPE,
        search_kwargs={
            "filter": {
                "must": [
                    {"key": "session_id", "match": {"value": session_id}}
                ]
            },
            "k": K,
            "fetch_k": 40,
            "lambda_mult": 0.5
        }
    )

# ─── Hybrid Chat QA Chain ────────────────────────────────────────────────
def build_hybrid_chain(session_id: str):
    prompt_template = PromptTemplate(
        input_variables=["context", "chat_history", "input", "jd_or_role"],
        template=Path(HYBRID_PROMPT_PATH).read_text()
    )

    def print_and_return(prompt: str) -> str:
        if DEBUG:
            print("🧾 Final Prompt Sent to LLM:\n", prompt)
        return prompt

    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        temperature=GEMINI_TEMP,
        google_api_key=gemini_api_key
    )

    retriever = get_session_retriever(session_id)

    def enrich_with_context(inputs):
        if DEBUG:
            print("🔍 Retrieving context for input:", inputs["input"])

        docs = retriever.invoke(inputs["input"])
        _, session = get_session(session_id)
        chunk_usage = session.chunk_usage

        filtered_docs = []
        for doc in docs:
            cid = doc.metadata.get("chunk_id")
            if not cid:
                if DEBUG:
                    print("⚠️ Skipping chunk due to missing chunk_id.")
                continue
            count = chunk_usage.get(cid, 0)
            if DEBUG:
                print(f"Chunk usage for {cid}: {count}")
            if count < MAX_CHUNK_USAGE:
                filtered_docs.append(doc)
                chunk_usage[cid] = count + 1
            else:
                if DEBUG:
                    print(f"⚠️ Skipping chunk due to usage threshold.")

        if not filtered_docs:
            if DEBUG:
                print("⚠️ No relevant chunks found. Using full resume as fallback.")
            context = session.resume_text
        else:
            context = "\n\n".join(doc.page_content for doc in filtered_docs)
            if DEBUG:
                print("📥 Retrieved context:\n", context[:500])

        return {
            "context": context,
            "input": inputs["input"],
            "chat_history": inputs.get("chat_history", ""),
            "jd_or_role": inputs["jd_or_role"]  
        }

    return (
        RunnableLambda(enrich_with_context)
        | prompt_template
        | RunnableLambda(print_and_return)
        | llm
        | StrOutputParser()
    )

# ─── Candidate Evaluation Chain ──────────────────────────────────────────
def get_evaluation_chain() -> LLMChain:
    template = HYBRID_EVAL_PROMPT_PATH.read_text()

    prompt = PromptTemplate(
        input_variables=["resume", "chat_history", "jd_or_role"],
        template=template
    )

    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        temperature=GEMINI_TEMP,
        google_api_key=gemini_api_key
    )

    return prompt | llm

# ─── Cleanup Expired Sessions ────────────────────────────────────────────
def delete_old_sessions(mins: int = 30):
    cutoff = datetime.utcnow() - timedelta(minutes=mins)
    if DEBUG:
        print(f"🕒 Removing sessions older than {cutoff.isoformat()}...")

    expired_sessions = set()
    offset = None

    while True:
        scroll_result = qdrant_client.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=None,
            with_payload=True,
            limit=500,
            offset=offset
        )

        points, next_offset = scroll_result
        if not points:
            break

        for point in points:
            payload = point.payload or {}
            session_id = payload.get("session_id")
            metadata = payload.get("metadata", {})
            created_at_str = metadata.get("created_at")

            if not session_id or not created_at_str:
                continue

            try:
                created_at = datetime.fromisoformat(created_at_str)
                if created_at < cutoff:
                    expired_sessions.add(session_id)
            except Exception as e:
                print(f"⚠️ Error parsing timestamp: {e} for point {point.id}")

        offset = next_offset
        if offset is None:
            break

    for session_id in expired_sessions:
        try:
            if DEBUG:
                print(f"🗑 Deleting expired session: {session_id}")
            qdrant_client.delete(
                collection_name=COLLECTION_NAME,
                points_selector=Filter(
                    must=[FieldCondition(key="session_id", match=MatchValue(value=session_id))]
                )
            )
        except Exception as e:
            print(f"❌ Failed to delete session {session_id}: {e}")
