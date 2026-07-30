from openai import OpenAI
from dotenv import load_dotenv
import os

class Agent:
    def __init__(self, id, model, key):
        self.id = id
        self.model = model
        self.client = OpenAI(api_key = key)

load_dotenv()
## Load Key from Environment
def get_key(API_key):
    key = os.getenv(API_key)
    if key is None:
        raise ValueError(f"KEY FAILED: {API_key}")
    return key

def llm_input(agent, prompt):
    response = agent.client.responses.create(model = agent.model, input = prompt)
    return response.output_text.strip()