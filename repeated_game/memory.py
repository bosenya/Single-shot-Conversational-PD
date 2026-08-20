## MEMORY STORAGE

previous_response_ids = {}
initialized_agents = {}

## INITIALIZE MEMORY

def initialize_memory(agent_ids):
    global previous_response_ids, initialized_agents
    previous_response_ids = {agent_id: None for agent_id in agent_ids}
    initialized_agents = {agent_id: False for agent_id in agent_ids}

## INITIALIZATION FLAG

def is_initialized(agent_id):
    return initialized_agents.get(agent_id, False)

def set_initialized(agent_id, value=True):
    initialized_agents[agent_id] = value

## RESPONSE MEMORY

def get_previous_response(agent_id):
    return previous_response_ids.get(agent_id)

def set_previous_response(agent_id, response_id):
    previous_response_ids[agent_id] = response_id

def reset_memory():
    global previous_response_ids, initialized_agents
    previous_response_ids.clear()
    initialized_agents.clear()