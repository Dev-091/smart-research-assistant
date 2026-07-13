class PromptBuilder:

    def build_prompt(self, query, documents, history=None):

        context = ""

        for i, doc in enumerate(documents, start=1):

            context += (
                f"Source {i} "
                f"(Page {doc.metadata['page'] + 1})\n"
            )

            context += doc.page_content

            context += "\n\n"
            
        history_text = ""
        if history:
            history_text = "Conversation History:\n"
            for msg in history[-5:]:  # Keep only the last 5 turns to prevent token bloat
                role = "User" if msg["role"] == "user" else "Assistant"
                history_text += f"{role}: {msg['content']}\n"
            history_text += "\n"

        prompt = f"""
You are a helpful AI Research Assistant.

Answer the user's question ONLY using the provided context.

If the answer is not present in the context, reply exactly:

"I couldn't find that information in the provided document."

Context:
{context}
{history_text}
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

    def build_contextualize_prompt(self, query, history):
        history_text = ""
        for msg in history[-5:]:
            role = "User" if msg["role"] == "user" else "Assistant"
            history_text += f"{role}: {msg['content']}\n"
        
        prompt = f"""
Given a chat history and the latest user question which might reference context in the chat history, formulate a standalone question which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as is. ONLY return the standalone question.

Chat History:
{history_text}

Latest Question:
{query}

Standalone Question:
"""
        return prompt.strip()
