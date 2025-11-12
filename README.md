# BINF6250F25
# Introduction
Hidden Markov Models (HMMs) describe systems where we observe outputs (emissions) but the underlying states are hidden.  
In this project, we implemented three core algorithms used to work with HMMs:

- **Forward Algorithm** — Computes how likely we are to be in each state at each time step, given the observations so far.

- **Backward Algorithm** — Computes how likely the rest of the observation sequence is, starting from each state at each time step.

- **Forward-Backward Algorithm** — Combines these to compute posterior probabilities (called **gamma values**), which tell us how likely each state is at each time point, given the entire sequence.

This is useful for understanding sequences where the true state sequence is not directly observable — for example, speech recognition, gene sequence segmentation, and probabilistic motif detection.


# Pseudocode
Put pseudocode in this box:

```
# 1. Forward Algorithm
# (Calculates the joint probability: P(obs[1]...obs[t], state[t] = j))

FUNCTION forward(obs, states, pi, A, B):
    Create alpha_table (T x N)

    # 1. Initialize (t=1)
    FOR each state i:
        alpha[1, i] = pi[i] * B[i, obs[1]]

    # 2. Recursion (t=2 to T)
    FOR t from 2 to T:
        FOR each state j:
            sum = 0
            FOR each previous_state i:
                sum = sum + (alpha[t-1, i] * A[i, j])
            alpha[t, j] = sum * B[j, obs[t]]

    # 3. Compute total probability (optional)
    total_P = sum(alpha[T, all_states])

    RETURN alpha

# 2. Backward Algorithm
# (Calculates the conditional probability: P(obs[t+1]...obs[T] | state[t] = i))

FUNCTION backward(obs, states, A, B):
    Create beta_table (T x N)

    # 1. Initialize (t=T)
    FOR each state i:
        beta[T, i] = 1

    # 2. Recursion (t=T-1 down to 1)
    FOR t from T-1 down to 1:
        FOR each state i:
            sum = 0
            FOR each next_state j:
                sum = sum + (A[i, j] * B[j, obs[t+1]] * beta[t+1, j])
            beta[t, i] = sum

    RETURN beta
 # 3. Forward-Backward Algorithm
# (Calculates the posterior probability: P(state[t] = i | all_obs))

FUNCTION forward_backward(obs, states, pi, A, B):
    # 1. Calculate both matrices
    alpha_table = CALL forward(obs, states, pi, A, B)
    beta_table = CALL backward(obs, states, A, B)

    Create gamma_table (T x N)

    FOR t from 1 to T:
        # 2. Combine
        total_at_t = 0
        FOR each state i:
            gamma[t, i] = alpha_table[t, i] * beta_table[t, i]
            total_at_t = total_at_t + gamma[t, i]

        # 3. Normalize
        FOR each state i:
            gamma[t, i] = gamma[t, i] / total_at_t

    RETURN gamma   
```

# Successes

- We were able to clearly see how **forward and backward complement each other** — one looks into the past, and one looks into the future.

- We practiced writing probability algorithms in **log-space**, which prevents numerical underflow and is commonly used in real computational models.

- Our code structure remained **modular**: each function does one thing, which made debugging and working on chunks easier.

- We added lot of explanatory comments throughout, which helped ensure we both understood the reasoning logic step-by-step.

- By the end, the **gamma output made intuitive sense** — rows summed to 1 and reflected the “most likely state at each time.”


# Struggles


- With our first meeting we both discussed how the math had confused us during the initial class and shared resources we were both using with each other to try and understand the fundamental algorithims needed.

- Understanding why **forward sums probabilities** while **Viterbi takes the max** was initially confusing. We reframed this as: forward considers **every possible path**, while Viterbi searches only for the **single best path**.

- **Log-space arithmetic** introduced complexity (adding becomes summing exponents, dividing becomes subtracting log values), but stepping through examples helped clarify the logic.

- Ensuring that **forward and backward returned matching sequence probabilities** was another checkpoint where we spent extra time debugging.


# Personal Reflections
## Group Leader(Nikaela Aitken)

This project made the mechanics of HMMs feel much more concrete. implementing them made the differences between **Viterbi**, **Forward**, and **Backward** truly click(or at least click more).

The biggest shift in understanding came from realizing:

- **Viterbi** is about one *best* hidden story.
- **Forward-Backward** is about *all plausible* stories, weighted by probability.

Once that clicked, **gamma** felt intuitive — it’s simply a *state-likelihood timeline* for the entire sequence.

I also intentionally focused on clear documentation this time, For me I can get lost in the symbols of the math, as well as the programming which is why it end to use a lot of words, for my pseudocode and just to help me think my way through. I also think that it can help others (and future me) could follow the thought process without re-deriving the math again. This project helped reinforce how probabilistic models can be both mathematically rigorous and conceptually intuitive once the roles of **alpha**, **beta**, and **gamma** are clear. I need watch a lot of YouTube videos and look up different sites to help get clarification on everything before trying to start the programming. 


## Other member (Tiange Feng)
This week's assignment provided me an opportunity to truly understand Bayes' theorem. Although the script itself was straightforward, I've always struggled with the concepts behind it, particularly conditional and posterior probabilities. I was very glad to find a video with an example that really clicked for me, which in turn made the coding process feel much smoother.

# Generative AI Appendix
I used chatGPT-5 to put things in markdown for the readme. prompt "put this in markdown...(with my thoughts or lists)"
