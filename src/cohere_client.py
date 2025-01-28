import cohere
from config import COHERE_API_KEY, PROMPT_TEMPLATE

class CohereClient:
    def __init__(self):
        self.client = cohere.Client(COHERE_API_KEY)

    def generate_json(self, resume_text):
        response = self.client.generate(
            model="command-xlarge-nightly",
            prompt=PROMPT_TEMPLATE + f"\nResume:\n{resume_text}",
            max_tokens=1000,
            temperature=0.7,
        )
        return response.generations[0].text.strip()
