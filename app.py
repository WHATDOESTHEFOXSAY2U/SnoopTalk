import streamlit as st
from streamlit_chat import message
from agent import ChatAgent  # Renamed for clarity

st.set_page_config(page_title="SnoopTalk Chat")

def display_chat_messages():
    """
    Display chat messages stored in session state.
    """
    st.subheader("Conversation with Snoop AI")
    for idx, (msg, is_user) in enumerate(st.session_state["chat_messages"]):
        message(msg, is_user=is_user, key=f"msg_{idx}")

def process_user_input():
    """
    Process user's input, send it to ChatAgent, and display the response.
    """
    user_input = st.session_state["user_input"].strip()
    if user_input:
        with st.spinner("AI is responding..."):
            response_text, response_audio = st.session_state["chat_agent"].respond_to_query(user_input)

        # Clear user input and update chat history
        st.session_state["user_input"] = ""
        st.session_state["chat_messages"] += [(user_input, True), (response_text, False)]

        # Display audio response if available
        if response_audio:
            st.audio(response_audio, format="audio/wav")

def main():
    """
    Main function to initialize UI components and manage chat interactions.
    """
    if "chat_messages" not in st.session_state:
        st.session_state["chat_messages"] = []

    if "chat_agent" not in st.session_state:
        st.session_state["chat_agent"] = ChatAgent()

    st.header("Chat with AI Snoop Dogg")
    display_chat_messages()
    user_input = st.text_input("Say something to Snoop AI", key="user_input", on_change=process_user_input)

    st.sidebar.selectbox("Choose AI model", options=["GPT-3.5", "LLaMA-2"], index=0, key="selected_model")
    st.sidebar.text("Settings and options")

if __name__ == "__main__":
    main()