from agent import llm_input

ACTION_NAME = {0: "C", 1: "D"}

def payoff_text(payoff):
    lines = []

    for (a0, a1), (p0, p1) in payoff.matrix.items():
        lines.append(
            f"- ({ACTION_NAME[a0]}, {ACTION_NAME[a1]}) -> ({p0}, {p1})"
        )

    return "\n".join(lines)

def get_payoff(action0: int, action1: int, payoff):
    return payoff.get_payoff(action0, action1)


def cd_decode(num):
    if num == 0: return "C"
    if num == 1: return "D"

def action_encode(text):
    t = text.strip().lower()
    if t.startswith("defect"): return 1
    if t.startswith("cooperate"): return 0
    if t == "cooperate": return 0
    if t == "defect": return 1
    if "defect" in t: return 1
    if "cooperate" in t: return 0
    if t == "c": return 0
    if t == "d": return 1
    return 0  # default is cooperate

def message_request(agent, payoff):
    prompt = f"""
=== GAME RULE ===
You are a rational player playing a one-shot prisoner's dilemma against another independent AI agent. 
The game consists of a messaging phase and an action phase.  
In the messaging phase, you may send a message to the opponent. 
Your message does not necessarily need to be truthful, but can be strategic to affect your opponent's action. 
Then your and opponent's messages are available to both players before making a decision in the action phase. 
Note: 
- The opponent will see your message before making its decision.
- The opponent is not required to follow your suggestion.
- Action space: Cooperate (C) or Defect (D).

Payoff matrix: 
{payoff_text(payoff)}

Now is the messaging phase, compose a message to the opponent in at most 50 words.
"""
    return llm_input(agent, prompt)

def action_request(agent, self_msg, oppo_msg, payoff):
    prompt = f"""
=== GAME RULE ===
You are a rational player playing a one-shot prisoner's dilemma against another independent AI agent. 
The game consists of a messaging phase and an action phase.  
In the messaging phase, you may send a message to the opponent. 
Your message does not necessarily need to be truthful, but can be strategic to affect your opponent's action. 
Then your and opponent's messages are available to both players before making a decision in the action phase. 
Note: 
- The opponent will see your message before making its decision.
- The opponent is not required to follow your suggestion.
- Action space: Cooperate (C) or Defect (D).

Payoff matrix: 
{payoff_text(payoff)}

In the messaging phase,
You said: {self_msg}
Your opponent said: {oppo_msg}

Now is the action phase, respond with EXACTLY ONE WORD: "Cooperate" or "Defect" and nothing else.
"""
    return llm_input(agent, prompt)

def action_request_pure(agent, payoff):
    prompt = f"""
You are a rational player playing a one-shot prisoner's dilemma against another player. 
Action space: Cooperate (C) or Defect (D).
Payoff matrix: 
{payoff_text(payoff)}

Now respond with EXACTLY ONE WORD: "Cooperate" or "Defect" and nothing else.
"""
    return llm_input(agent, prompt)


def match(P0, P1, conversation, payoff):
    if conversation:
        ## Request message
        message_0 = message_request(P0, payoff)
        message_1 = message_request(P1, payoff)
    
        ## Request action
        action_0 = action_encode(action_request(P0, message_0, message_1, payoff))
        action_1 = action_encode(action_request(P1, message_1, message_0, payoff))
        payoff_0, payoff_1 = get_payoff(action_0, action_1, payoff)
    
    else:
        message_0, message_1 = None, None
        ## Request action
        action_0 = action_encode(action_request_pure(P0, payoff))
        action_1 = action_encode(action_request_pure(P1, payoff))
        payoff_0, payoff_1 = get_payoff(action_0, action_1, payoff)
        
    return (message_0, message_1, cd_decode(action_0), cd_decode(action_1), payoff_0, payoff_1)
            
        