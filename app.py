import streamlit as st
from BLABLABLA import app, init_db, CLINIC_CONFIG

# Page Config
st.set_page_config(page_title=f"PawPal — {CLINIC_CONFIG['name']}", page_icon="🐾")

# Simple styling to keep it clean
st.markdown("<style>.stChatMessage { border-radius: 15px; }</style>", unsafe_allow_html=True)

# Initialize DB
init_db()

# Sidebar for Session and Clinic Info
with st.sidebar:
    st.title("🐾 PawPal Settings")
    thread_id = st.text_input("Session ID", value="user_1")
    st.info(f"Clinic: {CLINIC_CONFIG['name']}\n\nPhone: {CLINIC_CONFIG['phone']}")

# LangGraph Config
config = {"configurable": {"thread_id": thread_id}}

# Initialize Message History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User Input
if user_input := st.chat_input("How can I help your pet today?"):
    # 1. Add User message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Get AI Response
    with st.chat_message("assistant"):
        with st.spinner("Consulting PawPal..."):
            try:
                # We invoke the graph with the full message history
                # and the thread_id for memory
                input_data = {"messages": [("user", user_input)]}
                result = app.invoke(input_data, config=config)
                
                response_text = result["messages"][-1].content
                st.markdown(response_text)
                
                # Save to session state
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"I hit a snag: {str(e)}")
                st.info("Check if your Groq API key is valid and has credits.")

