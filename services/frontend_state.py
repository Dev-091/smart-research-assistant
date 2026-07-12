from pathlib import Path

import streamlit as st

from services.document_manager import DocumentManager
from services.rag_service import RAGService


DEFAULT_THEME = "dark"
THEME_VARIABLES = {
    "dark": """
    :root {
        --bg: #07111f;
        --panel: rgba(9, 20, 37, 0.82);
        --panel-strong: #0d172a;
        --panel-soft: rgba(20, 33, 54, 0.72);
        --border: rgba(148, 163, 184, 0.18);
        --text: #e5eefb;
        --muted: #93a4bf;
        --accent: #5eead4;
        --accent-strong: #14b8a6;
        --warning: #f59e0b;
        --shadow: 0 24px 60px rgba(2, 6, 23, 0.35);
        --app-bg: radial-gradient(circle at top right, rgba(20, 184, 166, 0.08), transparent 28%), linear-gradient(180deg, #040b16 0%, #091220 100%);
        --hero-gradient: radial-gradient(circle at top left, rgba(94, 234, 212, 0.18), transparent 34%), linear-gradient(135deg, rgba(8, 15, 28, 0.96), rgba(12, 22, 41, 0.92));
        --sidebar-bg: rgba(5, 11, 22, 0.94);
        --chat-bg: rgba(6, 14, 26, 0.55);
        --chat-input-bg: rgba(6, 14, 26, 0.95);
    }
    """,
    "light": """
    :root {
        --bg: #eef5ff;
        --panel: rgba(255, 255, 255, 0.92);
        --panel-strong: #ffffff;
        --panel-soft: rgba(255, 255, 255, 0.88);
        --border: rgba(15, 23, 42, 0.10);
        --text: #10213a;
        --muted: #5b6b84;
        --accent: #0f766e;
        --accent-strong: #115e59;
        --warning: #d97706;
        --shadow: 0 24px 60px rgba(15, 23, 42, 0.08);
        --app-bg: radial-gradient(circle at top right, rgba(20, 184, 166, 0.10), transparent 24%), linear-gradient(180deg, #f6fbff 0%, #e8f0fb 100%);
        --hero-gradient: radial-gradient(circle at top left, rgba(15, 118, 110, 0.12), transparent 30%), linear-gradient(135deg, rgba(255, 255, 255, 0.96), rgba(237, 245, 255, 0.96));
        --sidebar-bg: rgba(247, 250, 255, 0.96);
        --chat-bg: rgba(255, 255, 255, 0.92);
        --chat-input-bg: rgba(255, 255, 255, 0.98);
    }
    """,
}


def initialize_session_state():
    """Create all UI session keys exactly once."""
    defaults = {
        "messages": [],
        "rag_service": None,
        "theme": DEFAULT_THEME,
        "last_build_summary": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def load_stylesheet(path: str):
    """Load the custom CSS file into the Streamlit page."""
    theme = st.session_state.get("theme", DEFAULT_THEME)
    theme_css = THEME_VARIABLES.get(theme, THEME_VARIABLES[DEFAULT_THEME])
    css = Path(path).read_text(encoding="utf-8")
    st.markdown(f"<style>{theme_css}\n{css}</style>", unsafe_allow_html=True)


def append_chat_message(role: str, content: str):
    """Persist a message in session state."""
    st.session_state.messages.append({"role": role, "content": content})


def clear_chat_history():
    """Remove all chat messages from the current session."""
    st.session_state.messages = []


def set_theme(theme: str):
    """Store the selected theme variant."""
    st.session_state.theme = theme


def get_rag_service():
    """Lazily return the backend service if it has already been loaded."""
    if st.session_state.rag_service is not None:
        return st.session_state.rag_service

    try:
        st.session_state.rag_service = RAGService()
    except Exception:
        st.session_state.rag_service = None

    return st.session_state.rag_service


def reload_rag_service():
    """Reload the backend service after rebuilding the index."""
    st.session_state.rag_service = RAGService()
    return st.session_state.rag_service


def clear_rag_service():
    """Remove the current backend service from session state."""
    st.session_state.rag_service = None


def get_document_manager():
    """Return the UI-facing document manager service."""
    return DocumentManager()
