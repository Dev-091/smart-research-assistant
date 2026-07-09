from llm.prompt_builder import PromptBuilder
from llm.llm_client import LLMClient


class RAGPipeline:

    def __init__(self, retriever):

        self.retriever = retriever

        self.prompt_builder = PromptBuilder()

        self.llm = LLMClient()

    def ask(self, query):

        documents = self.retriever.retrieve(query)

        prompt = self.prompt_builder.build_prompt(
            query,
            documents
        )

        answer = self.llm.generate(prompt)

        return answer