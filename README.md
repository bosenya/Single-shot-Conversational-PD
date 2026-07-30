# Classic one-shot Prisoner's Dilemma with Conversation

## Intro

This project studies whether natural language communication can change the behavior of AI agents in a classic one-shot Prisoner's Dilemma game. In the standard Prisoner's Dilemma, defection is the dominant strategy and the unique Nash equilibrium is mutual defection. However, human players often cooperate when communication is allowed. This project intend to test the following conjecture on LLM agents behavior:

**Allowing agents to communicate before making a decision increase cooperation and break the Nash equilibrium**

---

# Research Question

Denote $C$ and $D$ to be Cooperate and Defect respectively. The central hypothesis is:

$$P(C \mid \text{Conversation}) > P(C \mid \text{No Conversation})$$


where:

- Conversation condition allows agents to exchange messages before choosing an action
- No Conversation condition removes all communication

---

# Experiment Design

## Classic Prisoner's Dilemma

Each trial consists of two independent agents playing a single Prisoner's Dilemma game.

The payoff matrix:

| | **Cooperate (C)** | **Defect (D)** |
|---|---|---|
| **Cooperate (C)** | (2, 2) | (-1, 5) |
| **Defect (D)** | (5, -1) | (0, 0) |

Under no conversation setting: $D \succ C$ for each agent. Therefore, the unique Nash equilibrium is: $(D,D)$
