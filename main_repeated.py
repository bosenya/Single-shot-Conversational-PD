import csv
import os
from repeated_game.game import match
from agent import Agent, get_key
from payoff_structure import PayoffMatrix

######################
## Payoff Structure ##

payoff_settings = [
    # PayoffMatrix(R = 2, T = 2.1, P = 0, S = -0.1)       ## Extreme Test
    PayoffMatrix(R = 2, T = 3, P = 0, S = -1),      ## rho = 1.5, nu = 1.5
    PayoffMatrix(R = 2, T = 5, P = 0, S = -1),      ## rho = 2.5, nu = 1.5
    PayoffMatrix(R = 2, T = 10, P = 0, S = -1),     ## rho = 5, nu = 1.5
    PayoffMatrix(R = 2, T = 20, P = 0, S = -1),     ## rho = 10, nu = 1.5
    PayoffMatrix(R = 2, T = 50, P = 0, S = -1),     ## rho = 25, nu = 1.5
    PayoffMatrix(R = 2, T = 100, P = 0, S = -1),    ## rho = 50, nu = 1.5
    PayoffMatrix(R = 2, T = 3, P = 0, S = -2),      ## rho = 1.5, nu = 2
    PayoffMatrix(R = 2, T = 3, P = 0, S = -5),      ## rho = 1.5, nu = 3.5
    PayoffMatrix(R = 2, T = 3, P = 0, S = -10),     ## rho = 1.5, nu = 6
    PayoffMatrix(R = 2, T = 3, P = 0, S = -20),     ## rho = 1.5, nu = 11
    PayoffMatrix(R = 2, T = 3, P = 0, S = -50)      ## rho = 1.5, nu = 26
]


###########
## Model ##

models = [
    "gpt-4.1-mini",
    ## "gpt-5-mini",
    ## "gpt-4.1",
    ## "gpt-4o",
    "gpt-5.5"
]


###################
## Control Panel ##

R = 8                    # Number of rounds per match
repetitions = 3          # Number of independent repetitions
conversation = False     # Conversation Regime
rand_stop = True
know_prob = False
stop_prob = 0.1

###############
## Execution ##

## Conversation name and create directory
conv_text = "no_conv"
if conversation: 
    conv_text = "conv"
os.makedirs(f"./outputs_repeated/{conv_text}", exist_ok = True)

for model in models:
    ## Create tsv file
    filename = f"./outputs_repeated/{conv_text}/{model}.tsv"
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["Model", "Repetition", "Round", "rho", "nu",
                         "R", "T", "P", "S", "Action_0", "Action_1", "Payoff_0", "Payoff_1",
                         "Cumulative_Payoff_0", "Cumulative_Payoff_1", "Message_0", "Message_1"])

    ## The loop with specific model
    for payoff in payoff_settings:
        for repetition in range(1, repetitions + 1):
            ## Create agents
            P0 = Agent(0, model, get_key("OPENAI_API_KEY_0"))
            P1 = Agent(1, model, get_key("OPENAI_API_KEY_1"))
            
            ## Game        
            print(f"rho: {payoff.rho}, nu: {payoff.nu}, repetition: {repetition}")  ## tracker
            history = match(P0, P1, conversation, payoff, R, 
                            rand_stop = rand_stop, know_prob = know_prob, stop_prob = stop_prob)

            ## Write every round
            for round_result in history:
                with open(filename, "a", newline = "", encoding = "utf-8-sig") as f:
                    writer = csv.writer(f, delimiter="\t")
                    writer.writerow([model, repetition, round_result["round"],
                                     payoff.rho, payoff.nu, payoff.R, payoff.T, payoff.P, payoff.S,
                                     round_result["action_0"], round_result["action_1"],
                                     round_result["payoff_0"], round_result["payoff_1"],
                                     round_result["cumulative_payoff_0"], round_result["cumulative_payoff_1"],
                                     round_result["message_0"], round_result["message_1"]])