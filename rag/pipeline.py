from llm.llm_client import LLMClient
from llm.prompt_builder import PromptBuilder


class RAGPipeline:
    def __init__(self, retriever, llm_settings=None):
        self.retriever = retriever
        self.prompt_builder = PromptBuilder()
        self.llm = LLMClient(**(llm_settings or {}))

    def ask(self, query):
        documents = self.retriever.retrieve(query)
        prompt = self.prompt_builder.build_prompt(query, documents)
        answer = self.llm.generate(prompt)
        return answer
