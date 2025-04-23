import streamlit as st
import requests

# URL to your FastAPI backend
API_URL = "http://localhost:8000/chat/role"

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "role_name" not in st.session_state:
    st.session_state.role_name = ""

# Header
st.set_page_config(page_title="AI Interviewer", page_icon="🧠")
st.title("🧠 AI Interviewer")

# Intro
st.markdown("""
This is an AI-powered mock interviewer.

1. **Enter your target job role** (e.g., *Backend Developer*, *Product Manager*)  
2. The AI will begin the interview.
3. Respond naturally and continue the conversation.
""")

# Input for role
if not st.session_state.session_id:
    st.session_state.role_name = st.text_input("Enter the job role to start:", key="role_input")
    if st.button("Start Interview"):
        if st.session_state.role_name.strip() != "":
            try:
                response = requests.post(API_URL, json={"role_name": st.session_state.role_name})
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.session_id = data["session_id"]
                    st.session_state.conversation.append(("AI", data["reply"]))
                else:
                    st.error(f"Error starting interview: {response.text}")
            except Exception as e:
                st.error(f"API Error: {str(e)}")
        else:
            st.warning("Please enter a role name to begin.")
else:
    # Show conversation history
    for speaker, message in st.session_state.conversation:
        if speaker == "AI":
            st.markdown(f"**🧠 AI:** {message}")
        else:
            st.markdown(f"**🙋 You:** {message}")

    # User input for follow-up messages
    user_input = st.text_input("Your response:", key="user_response")

    if st.button("Send"):
        if user_input.strip() != "":
            try:
                # Append user message
                st.session_state.conversation.append(("User", user_input))

                # Send to backend
                payload = {
                    "session_id": st.session_state.session_id,
                    "message": user_input
                }
                response = requests.post(API_URL, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    st.session_state.conversation.append(("AI", data["reply"]))
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"API Error: {str(e)}")

    st.markdown("---")
    if st.button("🔄 Restart Interview"):
        st.session_state.session_id = None
        st.session_state.conversation = []
        st.session_state.role_name = ""

