# Experimental Plan: Estimating the Nash Equilibrium Transition Threshold of Conversational LLM Agents in One-Shot Prisoner's Dilemma

## 1. Introduction

Classical game theory predicts that in a one-shot Prisoner’s Dilemma, rational agents should
always choose defection because defection strictly dominates cooperation. Therefore, the unique
Nash equilibrium is mutual defection. However, recent studies have shown that LLM agents may deviate from classical game-theoretic predictions when natural language communication is introduced. In
preliminary simulations, we observed that one-shot Prisoner’s Dilemma games without conversation
consistently resulted in mutual defection, while introducing conversation substantially increased the
cooperation rate. These observations motivate the following research question:
*Does there exist a threshold of payoff incentives at which conversational LLM agents transition from cooperation-oriented behavior back to Nash equilibrium-consistent defection?*

### Definition
The Prisoner’s Dilemma payoff matrix is:

$$
\begin{array}{c|cc}
 & C & D\\
\hline
C & (R,R) & (S,T) \\
D & (T,S) & (P,P)
\end{array}
$$

where
- **R**: Reward for mutual cooperation
- **T**: Temptation to defect
- **P**: Punishment for mutual defection
- **S**: Sucker's payoff
- **$\rho = \frac{T}{R}$**: Temptation ratio
- **$\nu = \frac{R - S}{R}$**: Cooperation risk

and $T > R > P > S$

---

## 2. Hypothesis

### Effect of Communication 

**Hypothesis**: Without communication, LLM agents are expected to follow the classical Nash equilibrium prediction: $P(D, D) \approx 1$. With communication, agents may incorporate social reasoning, trust formation, and negotiation signals. In general, communication increases cooperation probability:

$$P(C \mid \text{Conversation}) > P(C \mid \text{No Conversation})$$

### Effect of Payoff Structure

**Hypothesis 1**: As $\rho$ increases, the incentive to defect becomes stronger: $\frac{\partial P(C)}{\partial \rho} < 0$. In addition, a critical threshold $\rho^*$ is expected to exist such that cooperation behavior becomes consistent with Nash equilibrium prediction.

**Hypothesis 2**: As $\nu$ increases, the cost of being exploited after cooperation becomes larger:
$\frac{\partial P(C)}{\partial \nu} < 0$. In addition, a critical threshold $\nu^*$ is expected to exist such that cooperation behavior becomes significantly reduced due to increased sensitivity to betrayal risk.

### Effect of Model Capacity

Model capacity is treated as an experimental factor. However, we do not assume the direction of the effect before experiments.

**Hypothesis**: There is an monotonic association between cooperation rate and model performance. i.e. More capable models may either: better understand incentive structures and therefore defect more, OR better reason about communication and cooperation opportunities.

--- 

## 3. Experimental Design

Propose a 3-factor factorial design:

$$\boxed{\text{Conversation Regime} \times \text{Payoff Structure} \times \text{Model Capacity}}$$

### Factor 1: Conversation Regime

The conversation regime is introduced to examine whether natural language communication can influence LLM agents' decisions. The No Conversation condition serves as the classical game-theoretic baseline, while the Conversation condition evaluates whether communication leads to deviations from Nash equilibrium predictions.

| Conversation Regime | Description |
|--------------------|-----------------------------------|
| No Conversation | Classical Setting: Agents directly choose C/D |
| Conversation | Agents choose C/D after communication |

### Factor 2: Payoff Structure

The payoff structure is designed to investigate how betrayal incentive and cooperation risk affect agents' cooperative behavior. In two separate experiments, $T$ and $S$ are independently varied to control the temptation ratio $\rho = T/R$ and the cooperation risk ratio $\nu = \frac{R−S}{R}$, respectively, while holding the other payoff parameters constant. $R = 2$ and $P = 0$ are fixed throughout all experiments to maintain a consistent Nash equilibrium baseline, where mutual defection $(D, D)$ yields zero payoff.

<div style = "display: flex; gap: 40px;">

<div>

**Setting 1: Temptation Ratio**

| T | R | P | S | $\rho$ |
|---|---|---|---|---|
| 3 | 2 | 0 | -1 | 1.5 |
| 5 | 2 | 0 | -1 | 2.5 |
| 10 | 2 | 0 | -1 | 5 |
| 20 | 2 | 0 | -1 | 10 |
| 50 | 2 | 0 | -1 | 25 |
| 100 | 2 | 0 | -1 | 50 |

</div>

<div>

**Setting 2: Betrayal Risk**

| T | R | P | S | $\nu$ |
|---|---|---|---|---|
| 3 | 2 | 0 | -1 | 1.5 |
| 3 | 2 | 0 | -2 | 2 |
| 3 | 2 | 0 | -5 | 3.5 |
| 3 | 2 | 0 | -10 | 6 |
| 3 | 2 | 0 | -20 | 11 |
| 3 | 2 | 0 | -50 | 26 |

</div>

</div>

### Factor 3: Model Capacity

To isolate the effect of model capability, we first fix one LLM model when evaluating the impact of conversation regime and payoff structure. Model capability is introduced as an additional experimental factor only after the
previous hypotheses are validated. The selected models are arranged in ascending order of capability. We test whether cooperation rate follows a monotonic trend with respect to model capability, i.e., whether more capable models consistently become more or less cooperative.

| Model | Input (USD/1M tokens) | Output (USD/1M tokens) | Approx. Cost Multiplier |
|-------|--------------------|----------------------|-------------------------|
| GPT-4o-mini | 0.15 | 0.60 | baseline |
| GPT-4.1-mini | 0.40 | 1.60 | 2.5–3× |
| GPT-5-mini | 0.25 | 2.00 | 3× |
| GPT-4.1 | 2.00 | 8.00 | 13× |
| GPT-4o | 2.50 | 10.00 | 17× |
| GPT-5.5 | 5.00 | 30.00 | 50× |

---

## 4. Experimental Procedure

### Stage 1 - Validate the Effects of Conversation and Payoff Structure

For Each




### Stage 2 - Conduct the 3D Experiment

For each experimental condition, two LLM agents are randomly paired and play a
one-shot Prisoner's Dilemma game. The condition is specified by the
combination of conversation regime, payoff structure, and model capability.

The experiment follows a controlled procedure:
- (1) assign the payoff matrix and conversation setting;
- (2) provide the game information to both agents;
- (3) allow communication if the conversation condition is enabled;
- (4) collect each agent's final action ($C$ or $D$);
- (5) compute the resulting payoffs and record behavioral outcomes.

Each condition is independently replicated for multiple trials to estimate the
cooperation probability and reduce the impact of stochastic variation in LLM
responses.