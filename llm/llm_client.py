import os

from dotenv import load_dotenv
from groq import Groq

from config import GROQ_MODEL, MAX_TOKENS, TEMPERATURE

load_dotenv()


class LLMClient:
    def __init__(self, model=GROQ_MODEL, temperature=TEMPERATURE, max_tokens=MAX_TOKENS):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = model or GROQ_MODEL
        self.temperature = TEMPERATURE if temperature is None else temperature
        self.max_tokens = max_tokens or MAX_TOKENS

    def generate(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )

        return response.choices[0].message.content
