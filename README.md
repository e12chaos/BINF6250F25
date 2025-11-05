# BINF6250F25
# Introduction
This project implements the Viterbi Algorithm for a Hidden Markov Model (HMM) in Python. Our goal was to construct an HMM capable of determining the most likely sequence of hidden states given an observed DNA sequence. The implementation demonstrates how dynamic programming can efficiently compute this sequence using log probabilities to avoid numerical underflow.

The project is structured modularly, emphasizing clean, testable functions for initialization, recursion, termination, and traceback steps of the Viterbi algorithm.

# Pseudocode

```
Functions:

1. convert_hmm_params_to_matrices()
   - Converts dictionaries of initial, transition, and emission probabilities
     into numpy arrays for efficient matrix operations.

2. viterbi() — Main Algorithm Function
   - Accepts the observation sequence as input.
   - Initializes a probability matrix with:
       Rows = hidden states (e.g., “I” and “G”)
       Columns = observed sequence positions (e.g., “GGCACTGAA”)
   - Performs initialization, recursion, termination, and traceback.

3. initialize()
   - Computes initial probabilities for each state:
       P(state) × P(first observation | state)
   - Fills the first column of the Viterbi matrix.

4. recurse()
   - For each position in the observation sequence:
       For each state, find:
         max(previous_state_prob × transition_prob × emission_prob)
   - Stores the highest log-probability and the best previous state.

5. terminate()
   - Identifies which state has the highest probability in the final column.
   - Returns both the index and log-probability of this state.

6. traceback()
   - Reconstructs the optimal path of hidden states by following the
     stored backpointers from the last observation backward.

7. log_probability()
   - Converts probabilities to log-space, returning -inf for zeros to
     prevent underflow.

8. get_emission_prob()
   - Retrieves the emission probability for a given state and observation.

9. get_transition_prob()
   - Retrieves the transition probability from one state to another.
```

# Successes

- Tiange did a great job documenting her sections of the code, making her logic and design choices easy to follow.
- I kept a consistent documentation style across my sections for clarity and collaboration.
- Our modular design allowed the project to be broken into helper functions, which made debugging and scaling much easier.
- The final implementation successfully reproduces the expected Viterbi output and can easily be extended to more complex HMMs.


# Struggles
- GitHub Integration: RStudio’s Git and GitHub synchronization still caused versioning issues. I had to manually copy files as a workaround.

# Personal Reflections
## Group Leader(Nikaela Aitken)

Tiange and I each spent time independently thinking through the project before meeting, and we were both pleasantly surprised by how closely our ideas aligned. From the start, we agreed that modularity and readability were key so we decided to separate the Viterbi algorithm into smaller helper functions for initialization, recursion, termination, and traceback. This design made debugging easier and helped us understand how each part of the algorithm fits into the overall workflow.

We decided early to use separate helper functions to make the code more modular and testable, which paid off throughout development. Tiange was highly responsive, organized, and easy to collaborate with.

I especially enjoyed building the helper functions and thinking through how to structure the code for scalability in future applications. 

## Other member
Other members' reflections on the project

# Generative AI Appendix
As per the syllabus
