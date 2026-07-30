from game import match
from agent import Agent, get_key

P0 = Agent(0, "gpt-4.1-mini", get_key("OPENAI_API_KEY_0"))
P1 = Agent(1, "gpt-4.1-mini", get_key("OPENAI_API_KEY_1"))

conversation = True
trails = 30

match(P0, P1, trails, conversation)