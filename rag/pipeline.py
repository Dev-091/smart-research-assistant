from llm.llm_client import LLMClient
from llm.prompt_builder import PromptBuilder


class RAGPipeline:
    def __init__(self, retriever, llm_settings=None):
        self.retriever = retriever
        self.prompt_builder = PromptBuilder()
        self.llm = LLMClient(**(llm_settings or {}))

    def ask(self, query, history=None):
        search_query = query
        if history:
            contextualize_prompt = self.prompt_builder.build_contextualize_prompt(query, history)
            search_query = self.llm.generate(contextualize_prompt).strip()
            # Strip quotes if the LLM wrapped the question in them
            if search_query.startswith('"') and search_query.endswith('"'):
                search_query = search_query[1:-1]
        
        query_embedding = self.retriever.embedding_model.embed_query(search_query)
        scored_documents = self.retriever.vector_store.similarity_search_with_scores(
            query_embedding,
            self.retriever.top_k,
        )
        documents = [doc for doc, _ in scored_documents]
        scores = [score for _, score in scored_documents]
        prompt = self.prompt_builder.build_prompt(query, documents, history=history)
        answer = self.llm.generate(prompt)
        citations = self.prompt_builder.build_citation_metadata(documents, scores=scores)

        return {
            "answer": answer,
            "sources": citations,
        }
