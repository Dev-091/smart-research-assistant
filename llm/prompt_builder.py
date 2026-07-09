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