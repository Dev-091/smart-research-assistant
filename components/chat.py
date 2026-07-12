import time

import streamlit as st

from services.frontend_state import append_chat_message


def render_chat_transcript():
    """Render the existing conversation history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def _stream_text(text: str):
    """Yield text a word at a time to mimic live model streaming."""
    words = text.split()
    for index, word in enumerate(words):
        suffix = " " if index < len(words) - 1 else ""
        yield word + suffix
        time.sleep(0.02)


def render_chat_panel(rag_service):
    """Render the main chat input and assistant response flow."""
    question = st.chat_input("Ask a question about your research documents")
    if not question:
        st.markdown(
            """
            <div class="chat-empty-state">
                <h3>Ask sharper questions</h3>
                <p>
                    Your assistant is ready for document-grounded conversations.
                    The next module will connect upload and indexing controls.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    append_chat_message("user", question)
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        if rag_service is None:
            response = "Upload and build a knowledge base before starting the conversation."
            st.warning(response)
        else:
            with st.spinner("Generating answer..."):
                response = rag_service.ask(question)
            st.write_stream(_stream_text(response))

    append_chat_message("assistant", response)
