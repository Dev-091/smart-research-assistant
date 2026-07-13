class PromptBuilder:

    def build_prompt(self, query, documents):

        context = ""

        for i, doc in enumerate(documents, start=1):

            context += (
                f"Source {i} "
                f"(Page {doc.metadata['page'] + 1})\n"
            )

            context += doc.page_content

            context += "\n\n"

        prompt = f"""
You are a helpful AI Research Assistant.

Answer the user's question ONLY using the provided context.

If the answer is not present in the context, reply exactly:

"I couldn't find that information in the provided document."

Context:
{context}

Question:
{query}

Answer:
"""

        return prompt

    def build_citation_metadata(self, documents, scores=None):
        citations = []

        for index, doc in enumerate(documents, start=1):
            metadata = getattr(doc, "metadata", {}) or {}
            citations.append(
                {
                    "source_id": index,
                    "document_name": metadata.get("document_name", "Unknown document"),
                    "page": metadata.get("page", 0) + 1,
                    "chunk_preview": doc.page_content[:300].strip(),
                    "similarity_score": None if scores is None else scores[index - 1],
                }
            )

        return citations
