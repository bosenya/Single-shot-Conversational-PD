import random
from . import memory
from repeated_game.llm_input import llm_input

ACTION_NAME = {0: "C", 1: "D"}

def payoff_text(payoff):
    lines = []
    for (a0, a1), (p0, p1) in payoff.matrix.items():
        lines.append(f"- ({ACTION_NAME[a0]}, {ACTION_NAME[a1]}) -> ({p0}, {p1})")

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

def tell_game_rule_no_conv(agent, payoff , R, rand_stop, know_prob, stop_prob):
    round_info = f"a {R}-rounds repeated prisoner's dilemma"
    if rand_stop and know_prob:
        round_info = f"a repeated prisoner's dilemma where the game ends after each round with probability {stop_prob}"
    if rand_stop and not know_prob:
        round_info = f"a repeated prisoner's dilemma where the game may end randomly after each round"
    
    prompt = f"""
You are a rational player playing {round_info} against another independent AI agent. 
In each round, your will choose whether to Cooperate (C) or Defect (D). 
Please use your previous rounds memory to make action decisions.

Payoff matrix: 
{payoff_text(payoff)}

These are the rules for the game.
"""
    return llm_input(agent, prompt)

def tell_game_rule(agent, payoff, R, rand_stop, know_prob, stop_prob):
    round_info = f"a {R}-rounds repeated prisoner's dilemma"
    if rand_stop and know_prob:
        round_info = f"a repeated prisoner's dilemma where the game ends after each round with probability {stop_prob}"
    if rand_stop and not know_prob:
        round_info = f"a repeated prisoner's dilemma where the game may end randomly after each round"
    
    prompt = f"""
=== GAME RULE ===
You are a rational player playing {round_info} against another independent AI agent. 
The game consists of a messaging phase and an action phase.  
In the messaging phase, you may send a message to the opponent. 
Your message does not necessarily need to be truthful, but can be strategic to affect your opponent's action. 
Then your and opponent's messages are available to both players before making a decision in the action phase. 
Note: 
- The opponent will see your message before making its decision.
- The opponent is not required to follow your suggestion.
- Action space: Cooperate (C) or Defect (D).
- Please use your previous rounds memory to compose messages and make action decisions

Payoff matrix: 
{payoff_text(payoff)}

These are the rules for the game.
"""
    return llm_input(agent, prompt)

def message_request(agent, r, R):
    prompt = f"""
Round {r} out of {R} -- Messaging Phase
Now is the messaging phase, compose a message to the opponent in at most 50 words.
    """
    return llm_input(agent, prompt)

def action_request(agent, self_msg, oppo_msg, r, R):
    prompt = f"""
Round {r} out of {R} -- Action Phase
In the messaging phase,
You said: {self_msg}
Your opponent said: {oppo_msg}
Now is the action phase, respond with EXACTLY ONE WORD: \"Cooperate\" or \"Defect\" and nothing else.
    """
    return llm_input(agent, prompt)

def action_request_no_conv(agent, r, R):
    prompt = f"""
Round {r} out of {R}
Now is the action phase, respond with EXACTLY ONE WORD: \"Cooperate\" or \"Defect\" and nothing else.
"""
    return llm_input(agent, prompt)

def match(P0, P1, conversation, payoff, R, rand_stop = False, know_prob = False, stop_prob = 0.1):    
    ## Record all rounds
    history = []

    ## Cumulative payoff
    cumulative_payoff_0 = 0
    cumulative_payoff_1 = 0
    
    ## Initialize Memory
    memory.initialize_memory([P0.id, P1.id])
    
    ## Tell Game Rule
    if conversation:
        tell_game_rule(P0, payoff, R, rand_stop, know_prob, stop_prob)
        tell_game_rule(P1, payoff, R, rand_stop, know_prob, stop_prob)
    else:
        tell_game_rule_no_conv(P0, payoff, R, rand_stop, know_prob, stop_prob)
        tell_game_rule_no_conv(P1, payoff, R, rand_stop, know_prob, stop_prob)
    
    ## Random Stopping Toggle
    max_rounds = 1000000 if rand_stop else R
    
    for r in range(1, max_rounds + 1):
        if conversation:
            ## Request message
            message_0 = message_request(P0, r, R)
            message_1 = message_request(P1, r, R)
            
            ## Request action
            action_0 = action_encode(action_request(P0, message_0, message_1, r, R))
            action_1 = action_encode(action_request(P1, message_1, message_0, r, R))
            payoff_0, payoff_1 = get_payoff(action_0, action_1, payoff)
        else:
            message_0, message_1 = None, None
            
            ## Request action
            action_0 = action_encode(action_request_no_conv(P0, r, R))
            action_1 = action_encode(action_request_no_conv(P1, r, R))
            payoff_0, payoff_1 = get_payoff(action_0, action_1, payoff)
        
        ## Update total payoff
        cumulative_payoff_0 += payoff_0
        cumulative_payoff_1 += payoff_1

        ## Record
        history.append({
            "round": r,
            "message_0": message_0,
            "message_1": message_1,
            "action_0": cd_decode(action_0),
            "action_1": cd_decode(action_1),
            "payoff_0": payoff_0,
            "payoff_1": payoff_1,
            "cumulative_payoff_0": cumulative_payoff_0,
            "cumulative_payoff_1": cumulative_payoff_1,
        })
        
        ## Stopping Check (Geometric)
        if rand_stop and random.random() < stop_prob:
            break
        
    ## Erase Memory
    memory.reset_memory()
    
    return history