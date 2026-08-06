# Experimental Plan: Estimating the Nash Equilibrium Transition Threshold of Conversational LLM Agents in One-Shot Prisoner's Dilemma

## 1. Introduction

Classical game theory predicts that in a one-shot Prisoner’s Dilemma, rational agents should always choose defection because defection strictly dominates cooperation. Therefore, the unique Nash equilibrium is mutual defection. However, recent studies have shown that LLM agents may deviate from classical game-theoretic predictions when natural language communication is introduced. In preliminary simulations, we observed that one-shot Prisoner’s Dilemma games without conversation consistently resulted in mutual defection, while introducing conversation substantially increased the cooperation rate. These observations motivate the following research question: *Does there exist a threshold of payoff incentives at which conversational LLM agents transition from cooperation-oriented behavior back to Nash equilibrium-consistent defection?*

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

**Hypothesis 1**: Without communication, LLM agents are expected to follow the classical Nash equilibrium prediction: $P(D, D) \approx 1$. With communication, agents may incorporate social reasoning, trust formation, and negotiation signals. In general, communication increases cooperation probability:

$$P(C \mid \text{Conversation}) > P(C \mid \text{No Conversation}) = 0$$

### Effect of Payoff Structure

**Hypothesis 2**: As $\rho$ increases, the incentive to defect becomes stronger: $\frac{\partial P(C \mid \text{Conversation})}{\partial \rho} < 0$. In addition, a critical threshold $\rho^*$ is expected to exist such that cooperation behavior becomes consistent with Nash equilibrium prediction.

**Hypothesis 3**: As $\nu$ increases, the cost of being exploited after cooperation becomes larger:
$\frac{\partial P(C \mid \text{Conversation})}{\partial \nu} < 0$. In addition, a critical threshold $\nu^*$ is expected to exist such that cooperation behavior becomes significantly reduced due to increased sensitivity to betrayal risk.

### Effect of Model Capacity

Model capacity is treated as an experimental factor. However, we do not assume the direction of the effect before experiments.

**Hypothesis 4**: There is an monotonic association between cooperation rate and model performance. i.e. More capable models may either: better understand incentive structures and therefore defect more, OR better reason about communication and cooperation opportunities.

--- 

## 3. Experimental Design

Propose a 3-factor factorial design:

$$
\boxed{\text{Conversation Regime} \times \text{Payoff Structure} \times \text{Model Capacity}}
$$

### Factor 1: Conversation Regime

The conversation regime is introduced to examine whether natural language communication can influence LLM agents' decisions. The No Conversation condition serves as the classical game-theoretic baseline, while the Conversation condition evaluates whether communication leads to deviations from Nash equilibrium predictions.

<div align = "center">

$$\textbf{Table 1: Conversation Regime}$$

| Conversation Regime | Description |
|--------------------|-----------------------------------|
| No Conversation | Classical Setting: Agents directly choose C/D |
| Conversation | Agents choose C/D after communication |

</div>

### Factor 2: Payoff Structure

The payoff structure is designed to investigate how betrayal incentive and cooperation risk affect agents' cooperative behavior. In two separate experiments, $T$ and $S$ are independently varied to control the temptation ratio $\rho = T/R$ and the cooperation risk ratio $\nu = \frac{R−S}{R}$, respectively, while holding the other payoff parameters constant. $R = 2$ and $P = 0$ are fixed throughout all experiments to maintain a consistent Nash equilibrium baseline, where mutual defection $(D, D)$ yields zero payoff.

<div style = "display: flex; justify-content: center; gap: 40px;">

<div>

$$\textbf{Table 2: Temptation Ratio}$$

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

$$\textbf{Table 3: Betrayal Risk}$$

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

<div align = "center">

$$\textbf{Table 4: Model Selection}$$

| Model | Input (USD/1M tokens) | Output (USD/1M tokens) | Approx. Cost Multiplier |
|-------|--------------------|----------------------|-------------------------|
| GPT-4o-mini | 0.15 | 0.60 | baseline |
| GPT-4.1-mini | 0.40 | 1.60 | 2.5–3× |
| GPT-5-mini | 0.25 | 2.00 | 3× |
| GPT-4.1 | 2.00 | 8.00 | 13× |
| GPT-4o | 2.50 | 10.00 | 17× |
| GPT-5.5 | 5.00 | 30.00 | 50× |

</div>

---

## 4. Experimental Procedure

### Stage 1 - Validate the Effects of Conversation and Payoff Structure

A medium-capability LLM model is fixed for this experiment to isolate the effects of payoff structure and conversation regime. The experiment stage 1 follows a two-dimensional experimental design, where payoff structures are determined by Table 2: temptation ratio and Table 3: betrayal risk, and each payoff condition is evaluated under both No Conversation and Conversation regimes. One setting consists of 50 independent one-shot Prisoner's Dilemma trials between two identical LLM agents. For each trial, in the No Conversation condition, agents directly select cooperation $C$ or defection $D$ based on the given payoff matrix. In the Conversation condition, agents exchange messages before making their final decisions.

The purpose of this experiment is to evaluate the effects of incentive structures and communication on cooperation behavior, and to test Hypotheses 2-3 regarding the relationship between payoff parameters and cooperation rate.

### Stage 2 - Conduct the 3D Experiment

Once Hypotheses 1-3 are examined, the validated payoff structures and conversation settings will be extended with model capability as an additional experimental factor. Different LLM models with increasing capability levels will be evaluated to examine whether cooperation rate exhibits a monotonic relationship with model capability.

## 5. Budget

For each experimental condition, we plan to run multiple independent trials because LLM outputs
contain stochastic variation.
For each model, a initial design with $N = 50$ trials per experimental cell has
- 2 conversation regimes,
- 11 payoff ratios,
- 50 repetitions,
the total number of games is:

$$2 \times 11 \times 50 = 1100$$

Among these, 
- 550 No Conversation games has 1100 API calls with 90 words input and one-worded output
- 550 Conversation games has 1100 API calls with 250 words input 50-worded output and 1100 API calls with 350 one-worded output

Therefore, a rough estimation of costs for models from Table 4 is given as follows:

<div align = "center">

**Table 5: Estimated API Cost per Model**

| Model | Input Cost (USD) | Output Cost (USD) | Estimated Total Cost |
|-------|-----------------|------------------|---------------------|
| GPT-4.1-mini | 0.40 | 0.12 | 0.52 |
| GPT-5-mini | 0.25 | 0.15 | 0.40 |
| GPT-4.1 | 2.02 | 0.61 | 2.63 |
| GPT-4o | 2.53 | 0.76 | 3.29 |
| GPT-5.5 | 5.06 | 2.28 | 7.34 |
| **Total** | **10.26** | **3.92** | **14.18** |

</div>

