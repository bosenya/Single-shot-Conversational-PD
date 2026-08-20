from . import memory

def llm_input(agent, prompt):
    model = agent.model
    client = agent.client
    agent_id = agent.id

    ## Send the current round's prompt using the previous response as the conversation context.
    response = client.responses.create(model = model, input = prompt, 
                                       previous_response_id = memory.get_previous_response(agent_id))

    ## Update memory so that the next round can continue from this response.
    memory.set_previous_response(agent_id, response.id)

    return response.output_text.strip()