import json
import time
from datetime import datetime

import streamlit as st

from services.frontend_state import append_chat_message


def render_chat_transcript():
    """Render the existing conversation history."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and message.get("response_time_ms") is not None:
                st.caption(f"Response time: {message['response_time_ms']} ms")
            if message["role"] == "assistant" and message.get("sources"):
                _render_sources(message["sources"], query=st.session_state.messages[st.session_state.messages.index(message)-1]["content"] if st.session_state.messages.index(message) > 0 else "")
            if message["role"] == "assistant" and message.get("download_payload"):
                st.download_button(
                    "Download chat",
                    data=message["download_payload"],
                    file_name="smart-research-chat.json",
                    mime="application/json",
                    key=f"download_{message['message_id']}",
                )


def _stream_text(text: str):
    """Yield text a word at a time to mimic live model streaming."""
    words = text.split()
    for index, word in enumerate(words):
        suffix = " " if index < len(words) - 1 else ""
        yield word + suffix
        time.sleep(0.02)


def _render_sources(sources, query=""):
    import re
    query_terms = [re.escape(term) for term in re.findall(r"\w+", query.lower()) if len(term) > 3]
    highlight_pattern = re.compile(rf"\b({'|'.join(query_terms)})\b", flags=re.IGNORECASE) if query_terms else None

    with st.expander("Sources", expanded=False):
        for source in sources:
            score = source.get("similarity_score")
            score_text = "N/A" if score is None else f"{score:.4f}"
            st.markdown(
                f"**Page {source['page']}** | {source['document_name']} | Score: {score_text}"
            )
            preview = source["chunk_preview"]
            if highlight_pattern:
                preview = highlight_pattern.sub(r"<mark>\1</mark>", preview)
            st.markdown(f"<div style='font-size:0.85em; color:gray;'>{preview}</div>", unsafe_allow_html=True)


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

    assistant_payload = {
        "role": "assistant",
        "content": "",
        "response_time_ms": None,
        "sources": [],
        "download_payload": None,
        "message_id": f"assistant_{int(time.time() * 1000)}",
    }

    with st.chat_message("assistant"):
        if rag_service is None:
            response = "Upload and build a knowledge base before starting the conversation."
            st.warning(response)
            assistant_payload["content"] = response
        else:
            start = time.perf_counter()
            st.info("Searching documents...")
            with st.spinner("Generating answer..."):
                result = rag_service.ask(question, history=st.session_state.messages)
            response = result["answer"]
            sources = result.get("sources", [])
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            st.write_stream(_stream_text(response))
            if sources:
                _render_sources(sources, query=question)
            assistant_payload.update(
                {
                    "content": response,
                    "response_time_ms": elapsed_ms,
                    "sources": sources,
                    "download_payload": json.dumps(
                        {
                            "question": question,
                            "answer": response,
                            "sources": sources,
                            "response_time_ms": elapsed_ms,
                            "created_at": datetime.utcnow().isoformat() + "Z",
                        },
                        indent=2,
                    ),
                }
            )

    append_chat_message("assistant", assistant_payload["content"])
    st.session_state.messages[-1].update(assistant_payload)
