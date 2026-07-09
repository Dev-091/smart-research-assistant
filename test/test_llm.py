from llm.llm_client import LLMClient

llm = LLMClient()

response = llm.generate(
    "What is Artificial Intelligence?"
)

print(response)