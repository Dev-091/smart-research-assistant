import streamlit as st


def render_header():
    """Render the top hero area for the application."""
    st.markdown(
        """
        <section class="hero-shell">
            <div class="hero-copy">
                <span class="hero-badge">Production RAG Workspace</span>
                <h1>Smart Research Assistant</h1>
                <p>
                    Search, reason, and answer from your knowledge base with a
                    focused AI workspace built for serious document research.
                </p>
            </div>
            <div class="hero-status-card">
                <div class="status-pill">
                    <span class="status-dot"></span>
                    <span>System shell online</span>
                </div>
                <p>Frontend foundation is ready. Upload, indexing, and source workflows come next.</p>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )
