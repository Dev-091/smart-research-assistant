import streamlit as st

from components.chat import render_chat_panel, render_chat_transcript
from components.header import render_header
from components.sidebar import render_sidebar
from services.frontend_state import (
    clear_chat_history,
    clear_rag_service,
    get_document_manager,
    get_rag_service,
    get_settings_service,
    initialize_session_state,
    load_stylesheet,
    reload_rag_service,
    set_theme,
    update_app_settings,
)


st.set_page_config(
    page_title="Smart Research Assistant",
    page_icon="AI",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _handle_sidebar_actions(sidebar_state, document_manager, settings_service):
    if sidebar_state["save_settings"]:
        saved_settings = settings_service.save_settings(sidebar_state["settings"])
        update_app_settings(saved_settings)
        clear_rag_service()
        st.session_state.last_build_summary = None
        st.toast("Settings saved. Rebuild the knowledge base to apply indexing changes.")
        st.rerun()

    if sidebar_state["reset_settings"]:
        default_settings = settings_service.save_settings(settings_service.get_defaults())
        update_app_settings(default_settings)
        clear_rag_service()
        st.session_state.last_build_summary = None
        st.toast("Settings reset to defaults")
        st.rerun()

    if sidebar_state["save_uploads"] and sidebar_state["uploaded_files"]:
        saved_files = document_manager.save_uploaded_files(sidebar_state["uploaded_files"])
        st.session_state.last_build_summary = None
        st.toast(f"Saved {len(saved_files)} PDF(s) to data/raw")
        st.rerun()

    if sidebar_state["delete_document"]:
        document_manager.delete_document(sidebar_state["delete_document"])
        clear_rag_service()
        st.session_state.last_build_summary = None
        st.toast(f"Deleted {sidebar_state['delete_document']}")
        st.rerun()

    if sidebar_state["delete_all"]:
        deleted_count = document_manager.delete_all_documents()
        clear_rag_service()
        clear_chat_history()
        st.session_state.last_build_summary = None
        st.toast(f"Deleted {deleted_count} document(s)")
        st.rerun()

    if sidebar_state["build_index"] or sidebar_state["rebuild_index"]:
        action_label = "Rebuilding" if sidebar_state["rebuild_index"] else "Building"
        try:
            with st.spinner(f"{action_label} knowledge base..."):
                build_summary = document_manager.build_knowledge_base(settings=st.session_state.app_settings)
                reload_rag_service()
                st.session_state.last_build_summary = build_summary
            st.toast(f"Knowledge base ready with {build_summary['chunk_count']} chunks")
        except Exception as error:
            clear_rag_service()
            st.session_state.last_build_summary = None
            st.error(f"Knowledge base build failed: {error}")
            return
        st.rerun()

    if sidebar_state["clear_chat"]:
        clear_chat_history()
        st.rerun()

    if sidebar_state["theme"] != st.session_state.theme:
        set_theme(sidebar_state["theme"])
        st.rerun()


def _render_build_status():
    summary = st.session_state.get("last_build_summary")
    if not summary:
        return

    st.markdown(
        f"""
        <div class="build-summary-card">
            <strong>Knowledge base ready</strong>
            <span>{summary['document_count']} document(s), {summary['page_count']} page(s), {summary['chunk_count']} chunk(s)</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main():
    initialize_session_state()
    load_stylesheet("styles/style.css")

    settings_service = get_settings_service()
    document_manager = get_document_manager()
    sidebar_state = render_sidebar(
        document_manager,
        st.session_state.app_settings,
        settings_service.get_options(),
    )
    _handle_sidebar_actions(sidebar_state, document_manager, settings_service)

    render_header()
    _render_build_status()
    render_chat_transcript()

    rag_service = get_rag_service()
    render_chat_panel(rag_service)


if __name__ == "__main__":
    main()
