def llm_input(agent, prompt):
    response = agent.client.responses.create(model = agent.model, input = prompt)
    return response.output_text.strip()