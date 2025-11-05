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


Setup

Define:
  the list of all possible hidden STATES (e.g., ['I', 'G'])
  a map for all possible OBSERVATIONS to indices (e.g., {'A': 0, 'C': 1, ...})
  initial_probabilities dictionary (e.g., "Prob. of starting in 'I' is 0.2")
  transition_probabilities dictionary (e.g., "Prob. of 'I' -> 'G' is 0.3")
  emission_probabilities dictionary (e.g., "Prob. of seeing 'A' in state 'I' is 0.1")

Inputs:
  convert dictionaries into matrices
      initial_matrix, transition_matrix, emission_matrix
  convert the input observation sequence into a list of corresponding number indices


------

viterbi() 
  takes in: observation_indices, state_names, initial_matrix, transition_matrix, emission_matrix)

  Initialization
    T = length of observation_indices
    N = number of states

    viterbi_table: size T x N, fill with zeros
    backpointer_table: size T x N, fill with zeros

  probability matrices --> log-space

  the first observation (t=0)
    first_observation = observation_indices[0]
    for each state (from j = 0 to N-1):
        log_prob = log_initial[j] + log_emission[j, first_observation]
        viterbi_table[0, j] = log_prob


  Loop through the rest of the observations
    for each time step (from t = 1 to T-1):
        current_observation = observation_indices[t]

        for each current_state (from j = 0 to N-1):

            # Find the best previous state
            max_prob_from_prev = -infinity
            best_prev_state_index = 0

            # Check all possible previous state
            for each previous_state (from i = 0 to N-1):
                # calculate the score of coming from that previous state
                score = viterbi_table[t-1, previous_state] + log_transition[previous_state, current_state]

                if score > max_prob_from_prev:
                    max_prob_from_prev = score
                    best_prev_state_index = previous_state

            # Store the best path info for (t, j)
            backpointer_table[t, j] = best_prev_state_index

            # Store the final log-prob of this path step
            final_log_prob = max_prob_from_prev + log_emission[current_state, current_observation]
            viterbi_table[t, j] = final_log_prob


    # Find the best log-probability from the last row of the table
    best_path_log_prob = -infinity
    last_state_index = 0

    for each state (from j = 0 to N-1):
        if viterbi_table[T-1, j] > best_path_log_prob:
            best_path_log_prob = viterbi_table[T-1, j]
            last_state_index = j


  Traceback
    Create an empty list best_path

    # Start with the last state found
    current_state_index = last_state_index

    # Loop back from the last step to the first
    for each time step (from t = T-1 down to 0):

        # Get the name of the state
        state_name = state_names[current_state_index]

        # Add the state name to the front of the path list
        insert state_name at the beginning of best_path

        # Use the backpointer table to find the state
        current_state_index = backpointer_table[t, current_state_index]


    return best_path, best_path_log_prob
```

# Successes

- Tiange did a great job documenting her sections of the code, making her logic and design choices easy to follow.
- I kept a consistent documentation style across my sections for clarity and collaboration.
- The final implementation successfully reproduces the expected Viterbi output and can easily be extended to more complex HMMs.


# Struggles
- GitHub Integration: RStudio’s Git and GitHub synchronization still caused versioning issues. I had to manually copy files as a workaround.
- We split up the code and wrote helper functions, but haven't called them in the main function.  I wanted to keep them in case we do want to use them. I think this might be something we tweak going forward but for now they are there just incase. 

# Personal Reflections
## Group Leader(Nikaela Aitken)

Tiange and I each spent time independently thinking through the project before meeting, and we were both pleasantly surprised by how closely our ideas aligned. From the start, we agreed that modularity and readability were key so we decided to separate the Viterbi algorithm into smaller helper functions for initialization, recursion, termination, and traceback. This design made debugging easier and helped us understand how each part of the algorithm fits into the overall workflow.

We decided early to use separate helper functions to make the code more modular and testable, which paid off throughout development. Tiange was highly responsive, organized, and easy to collaborate with.

I especially enjoyed building the helper functions and thinking through how to structure the code for scalability in future applications. We just need to figure out how to pull them in now. 

## Other member(Tiange

Nikaela and I had a very productive collaboration because we both came to our meetings having thoroughly considered the algorithm's design. This allowed us to align on the code's structure almost immediately. The primary technical challenge for me was to manage how the indices for states and observations corresponded across the initial, transition, and emission matrices. A related hurdle was implementing the backpointer, which was solved after reviewing previous projects. This process was a valuable learning experience for me.

# Generative AI Appendix
As per the syllabus
