import streamlit as st


def _render_metric_card(label: str, value: str):
    st.markdown(
        f"""
        <div class="sidebar-metric-card">
            <span>{label}</span>
            <strong>{value}</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_document_item(document):
    button_key = f"delete_{document['name']}"
    item_col, action_col = st.columns([5, 1])
    with item_col:
        st.markdown(
            f"""
            <div class="document-row">
                <strong>{document['name']}</strong>
                <span>{document['size_mb']} MB</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with action_col:
        return st.button("X", key=button_key, use_container_width=True)


def _get_option_index(options, current_value):
    return options.index(current_value) if current_value in options else 0


def render_sidebar(document_manager, app_settings, settings_options):
    documents = document_manager.list_documents()
    stats = document_manager.get_index_stats()

    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="sidebar-brand-mark">SR</div>
                <div>
                    <h2>Research OS</h2>
                    <p>AI document workspace</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<p class="sidebar-section-label">Upload PDFs</p>', unsafe_allow_html=True)
        uploaded_files = st.file_uploader(
            "Add research documents",
            type=["pdf"],
            accept_multiple_files=True,
            label_visibility="collapsed",
        )
        save_uploads = st.button("Save Uploaded PDFs", use_container_width=True, disabled=not uploaded_files)

        st.markdown('<p class="sidebar-section-label">Knowledge Base</p>', unsafe_allow_html=True)
        build_index = st.button("Build Knowledge Base", use_container_width=True, disabled=not documents)
        rebuild_index = st.button("Rebuild Knowledge Base", use_container_width=True, disabled=not documents)
        run_evaluation = st.button("Evaluate Knowledge Base", use_container_width=True, disabled=not documents)

        st.markdown('<p class="sidebar-section-label">Documents</p>', unsafe_allow_html=True)
        if documents:
            deleted_document = None
            for document in documents:
                if _render_document_item(document):
                    deleted_document = document["name"]
            delete_all = st.button("Delete All Documents", use_container_width=True)
        else:
            st.markdown(
                """
                <div class="document-empty-state">
                    <strong>No PDFs uploaded yet</strong>
                    <span>Upload one or more files to start building your research workspace.</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            deleted_document = None
            delete_all = False

        st.markdown('<p class="sidebar-section-label">System Overview</p>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            _render_metric_card("Embedding", app_settings["models"]["embedding_model"].split("/")[-1])
            _render_metric_card("Vector DB", "FAISS")
            _render_metric_card("Documents", str(stats["document_count"]))
        with col2:
            _render_metric_card("LLM", app_settings["models"]["llm_model"])
            _render_metric_card("Chunks", str(stats["chunk_count"]))
            _render_metric_card("Index", "Ready" if stats["index_ready"] else "Missing")

        st.markdown('<p class="sidebar-section-label">Settings</p>', unsafe_allow_html=True)
        with st.expander("Retrieval and Generation", expanded=False):
            top_k = st.slider("Top K Retrieval", min_value=1, max_value=10, value=app_settings["retrieval"]["top_k"])
            chunk_size = st.slider("Chunk Size", min_value=200, max_value=2000, step=100, value=app_settings["chunking"]["chunk_size"])
            chunk_overlap = st.slider(
                "Chunk Overlap",
                min_value=0,
                max_value=max(0, chunk_size - 1),
                step=50,
                value=min(app_settings["chunking"]["chunk_overlap"], max(0, chunk_size - 1)),
            )
            embedding_model = st.selectbox(
                "Embedding Model",
                options=settings_options["embedding_models"],
                index=_get_option_index(settings_options["embedding_models"], app_settings["models"]["embedding_model"]),
            )
            llm_model = st.selectbox(
                "LLM Model",
                options=settings_options["llm_models"],
                index=_get_option_index(settings_options["llm_models"], app_settings["models"]["llm_model"]),
            )
            temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, step=0.1, value=float(app_settings["generation"]["temperature"]))
            max_tokens = st.slider("Max Tokens", min_value=256, max_value=4096, step=256, value=app_settings["generation"]["max_tokens"])
            save_settings = st.button("Save Settings", use_container_width=True)
            reset_settings = st.button("Reset Settings", use_container_width=True)

        st.markdown('<p class="sidebar-section-label">Preferences</p>', unsafe_allow_html=True)
        theme = st.segmented_control(
            "Theme",
            options=["dark", "light"],
            selection_mode="single",
            default=st.session_state.theme,
            key="theme_selector",
            label_visibility="collapsed",
        )

        st.markdown('<p class="sidebar-section-label">Chat</p>', unsafe_allow_html=True)
        clear_chat = st.button("Clear Chat", use_container_width=True)

    return {
        "uploaded_files": uploaded_files or [],
        "save_uploads": save_uploads,
        "build_index": build_index,
        "rebuild_index": rebuild_index,
        "run_evaluation": run_evaluation,
        "delete_document": deleted_document,
        "delete_all": delete_all,
        "clear_chat": clear_chat,
        "theme": theme or st.session_state.theme,
        "save_settings": save_settings,
        "reset_settings": reset_settings,
        "settings": {
            "retrieval": {"top_k": top_k},
            "chunking": {"chunk_size": chunk_size, "chunk_overlap": chunk_overlap},
            "models": {"embedding_model": embedding_model, "llm_model": llm_model},
            "generation": {"temperature": temperature, "max_tokens": max_tokens},
        },
        "stats": stats,
    }
