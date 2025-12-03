# BINF6250F25
# Introduction

This project implements the Baum-Welch algorithm (Expectation-Maximization for Hidden Markov Models) and applies it to analyze 5' UTR (Untranslated Region) sequences from human genes. The Baum-Welch algorithm is an unsupervised learning method that trains HMM parameters from observation sequences without requiring labeled state information.

Biological Context:
5' UTRs are regulatory regions in mRNA that:

Affect translation efficiency
Contain regulatory elements (upstream open reading frames, internal ribosome entry sites, etc.)
Show conserved structural patterns

Learning Objectives:
The trained HMM can identify:

Different regulatory states within UTRs
Position-specific nucleotide preferences
Transition patterns between regulatory regions

This project builds on previous work:

Project 08: Viterbi algorithm for finding most likely state sequences
Project 09: Forward-Backward algorithms for computing posterior probabilities

# Pseudocode
Algorithm Structure Overview
The Baum-Welch algorithm involves four key steps:

Initialization:

Start with initial guesses for transition, emission, and initial probabilities
Set up convergence criteria and pseudocounts to prevent zero probabilities


Expectation Step (E):

Run Forward-Backward algorithm on training sequences
Calculate expected counts for transitions and emissions
Compute posterior probabilities for each state at each position
These expected counts represent how often each transition and emission is used


Maximization Step (M):

Update model parameters based on expected counts
Re-estimate initial, transition, and emission probabilities
Normalize to ensure valid probability distributions
Scale values to prevent numerical underflow


Iteration and Convergence:

Repeat E and M steps until convergence criteria are met
Monitor likelihood improvement between iterations
Handle multiple observation sequences appropriately



Core Pseudocode

```
# --- 1. Definition of Key Algorithm Variables ---

# E-Step (Expectation) Variables:
#   alpha (table, T x N):
#       - The log-forward probabilities
#       - alpha[t, i] = log(P(obs[1]...obs[t], state[t] = i))
#
#   beta (table, T x N):
#       - The log-backward probabilities
#       - beta[t, i] = log(P(obs[t+1]...obs[T] | state[t] = i))
#
#   gamma (table, T x N):
#       - The posterior probabilities
#       - gamma[t, i] = P(state[t] = i | all_obs)
#       - "Expected State Count" for a single position
#
#   log_xi_ij (scalar, calculated at each step t, i, j):
#       - The joint log-posterior for a transition
#       - log(P(state[t]=i, state[t+1]=j | all_obs))
#       - "Expected Transition Count" for a single transition

# M-Step (Maximization) Variables:
#   e_init_counts (dict, size N):
#       - Expected counts for starting in each state
#
#   e_trans_numer (dict, size N x N):
#       - Numerator: Expected counts of transitioning from state i to state j
#
#   e_trans_denom (dict, size N):
#       - Denominator: Expected counts of transitioning from state i to any state
#
#   e_emit_numer (dict, size N x M):
#       - Numerator: Expected counts of emitting observation k from state i
#
#   e_emit_denom (dict, size N):
#       - Denominator: Expected counts of emitting any observation from state i
#
#   pseudocount (scalar):
#       - Small value added to all counts to prevent zero probabilities


# --- 2. The HMM Model Class ---

class HMM_Model:
    
    function __init__(self, init_probs_dict, trans_probs_dict, 
                     emit_probs_dict, pseudocount=0.01):
        # Store initial parameter guesses (dictionaries)
        self.init_probs = init_probs_dict
        self.trans_probs = trans_probs_dict
        self.emit_probs = emit_probs_dict
        
        # Store smoothing value
        self.pseudocount = pseudocount
        
        # Infer states from initial probabilities
        self.states = list(init_probs_dict.keys())
        
        # Infer observation alphabet from first state's emissions
        first_state = self.states[0]
        self.obs_alphabet = list(emit_probs_dict[first_state].keys())
        
        # Create observation-to-index map
        self.obs_map = {symbol: i for i, symbol in enumerate(self.obs_alphabet)}

    function baum_welch_train(self, training_obs_list, 
                             max_iterations=100, 
                             convergence_threshold=1e-5,
                             check_frequency=10):
        
        # Store log-likelihood from previous convergence check
        previous_check_log_likelihood = -infinity

        for iter from 0 to max_iterations:
            
            # --- EXPECTATION STEP (E-Step) ---
            
            # Initialize expected counts with pseudocount
            e_init_counts = {state: self.pseudocount for state in self.states}
            
            e_trans_numer = {s_i: {s_j: self.pseudocount for s_j in self.states} 
                           for s_i in self.states}
            e_trans_denom = {s_i: (self.pseudocount * len(self.states)) 
                           for s_i in self.states}
            
            e_emit_numer = {s_i: {obs: self.pseudocount for obs in self.obs_alphabet} 
                          for s_i in self.states}
            e_emit_denom = {s_i: (self.pseudocount * len(self.obs_alphabet)) 
                          for s_i in self.states}
            
            # Store total log-likelihood for current iteration
            current_iter_log_likelihood = 0

            # Convert parameter dictionaries to matrices once per iteration
            init_matrix, trans_matrix, emit_matrix = call convert_hmm_params_to_matrices(
                self.states, self.obs_map, self.init_probs, 
                self.trans_probs, self.emit_probs
            )
            
            # Convert to log-space for stable calculation
            with np.errstate(divide='ignore'):
                log_init = np.log(init_matrix)
                log_trans = np.log(trans_matrix)
                log_emit = np.log(emit_matrix)

            # Iterate through each observation sequence
            for seq_str in training_obs_list:
                
                obs_seq = [self.obs_map[obs] for obs in seq_str]
                T = len(obs_seq)

                # Run forward-backward using current model parameters
                alpha_table, seq_log_prob = call forward(
                    obs_seq, self.states, init_matrix, trans_matrix, emit_matrix
                )
                
                beta_table = call backward(
                    obs_seq, self.states, trans_matrix, emit_matrix
                )

                # Combine to get Gamma and Xi
                # gamma = P(state[t]=i | all_obs)
                log_gamma_unnormalized = alpha_table + beta_table
                log_posterior_gamma = log_gamma_unnormalized - seq_log_prob
                gamma = np.exp(log_posterior_gamma)
                
                current_iter_log_likelihood += seq_log_prob
                
                # --- Accumulate Expected Counts ---
                
                # 1. Expected initial state counts (from gamma[0])
                for i, state_i in enumerate(self.states):
                    e_init_counts[state_i] += gamma[0, i]

                # 2. Expected transition counts (from Xi)
                for t from 0 to T-2:
                    obs_t_plus_1 = obs_seq[t+1]
                    
                    for i, state_i in enumerate(self.states):
                        e_trans_denom[state_i] += gamma[t, i]
                        
                        for j, state_j in enumerate(self.states):
                            # Calculate log(xi[t, i, j])
                            log_xi_ij = (alpha_table[t, i] + 
                                       log_trans[i, j] + 
                                       log_emit[j, obs_t_plus_1] + 
                                       beta_table[t + 1, j] - 
                                       seq_log_prob)
                            
                            # Add probability to numerator
                            e_trans_numer[state_i][state_j] += np.exp(log_xi_ij)
                
                # 3. Expected emission counts (from Gamma)
                for t from 0 to T-1:
                    current_obs_symbol = seq_str[t]
                    for i, state_i in enumerate(self.states):
                        e_emit_denom[state_i] += gamma[t, i]
                        e_emit_numer[state_i][current_obs_symbol] += gamma[t, i]

            # --- MAXIMIZATION STEP (M-Step) ---
            # Re-estimate model parameters by normalizing expected counts
            
            # 1. Update initial probabilities
            total_init = sum(e_init_counts.values())
            for state_i in self.states:
                self.init_probs[state_i] = e_init_counts[state_i] / total_init

            # 2. Update transition probabilities
            for state_i in self.states:
                for state_j in self.states:
                    self.trans_probs[state_i][state_j] = (
                        e_trans_numer[state_i][state_j] / e_trans_denom[state_i]
                    )
            
            # 3. Update emission probabilities
            for state_i in self.states:
                for obs in self.obs_alphabet:
                    self.emit_probs[state_i][obs] = (
                        e_emit_numer[state_i][obs] / e_emit_denom[state_i]
                    )

            # --- Check for Convergence ---
            if iter > 0 and (iter % check_frequency == 0):
                
                likelihood_change = abs(current_iter_log_likelihood - 
                                      previous_check_log_likelihood)
                
                if likelihood_change < convergence_threshold:
                    print "Convergence reached at iteration {iter}."
                    break
                
                previous_check_log_likelihood = current_iter_log_likelihood
        
        return self.init_probs, self.trans_probs, self.emit_probs, 
               current_iter_log_likelihood


# --- 3. Meta-Algorithm for Finding Global Optimum ---

function find_best_hmm(training_obs_list, states_list, obs_alphabet,
                      num_restarts=10, max_iterations_per_run=50, 
                      pseudocount=0.01):
    
    best_overall_model_params = null
    best_overall_log_likelihood = -infinity

    print "Starting {num_restarts} random restarts..."

    for i from 1 to num_restarts:
        print "--- Restart {i} ---"
        
        # 1. Randomize initial parameters
        init_guesses, trans_guesses, emit_guesses = (
            call create_random_initial_params(states_list, obs_alphabet)
        )
        
        # 2. Create new model with random guesses
        temp_model = HMM_Model(init_guesses, trans_guesses, 
                              emit_guesses, pseudocount)
        
        # 3. Run Baum-Welch to find local optimum
        (local_pi, local_A, local_B, local_log_likelihood) = (
            temp_model.baum_welch_train(
                training_obs_list, 
                max_iterations=max_iterations_per_run
            )
        )
        
        print "Restart {i} Log-Likelihood: {local_log_likelihood}"

        # 4. Keep best result
        if local_log_likelihood > best_overall_log_likelihood:
            best_overall_log_likelihood = local_log_likelihood
            best_overall_model_params = (local_pi, local_A, local_B)
            
    return best_overall_model_params, best_overall_log_likelihood


# --- 4. Helper Functions ---

function create_random_initial_params(states_list, obs_alphabet):
    """
    Creates random init, trans, and emit dictionaries.
    Ensures all probability rows sum to 1.
    """
    n_states = len(states_list)
    n_obs = len(obs_alphabet)

    # 1. Create random initial probabilities
    random_pi = {}
    init_values = call generate_normalized_random_vector(n_states)
    for i from 0 to n_states-1:
        random_pi[states_list[i]] = init_values[i]

    # 2. Create random transition probabilities
    random_A = {}
    for i from 0 to n_states-1:
        from_state = states_list[i]
        random_A[from_state] = {}
        trans_values = call generate_normalized_random_vector(n_states)
        
        for j from 0 to n_states-1:
            to_state = states_list[j]
            random_A[from_state][to_state] = trans_values[j]

    # 3. Create random emission probabilities
    random_B = {}
    for i from 0 to n_states-1:
        from_state = states_list[i]
        random_B[from_state] = {}
        emit_values = call generate_normalized_random_vector(n_obs)
        
        for j from 0 to n_obs-1:
            obs_symbol = obs_alphabet[j]
            random_B[from_state][obs_symbol] = emit_values[j]

    return random_pi, random_A, random_B


function generate_normalized_random_vector(size):
    """
    Generates a vector of random numbers that sum to 1.0.
    """
    vector = create_empty_array(size)
    total_sum = 0

    # 1. Generate random floats
    for i from 0 to size-1:
        val = random_float(0.0, 1.0)
        vector[i] = val
        total_sum = total_sum + val

    # 2. Handle edge case where all random numbers are 0
    if total_sum == 0:
        for i from 0 to size-1:
            vector[i] = 1.0 / size
    else:
        # 3. Normalize the vector
        for i from 0 to size-1:
            vector[i] = vector[i] / total_sum
            
    return vector
```

# Successes
Description of the team's learning points

# Struggles
Description of the stumbling blocks the team experienced

# Personal Reflections
## Group Leader(Nikaela Aitken)
I found this project very exciting because of its obvious applications in unsupervised machine learning. I was particularly interested in applying the Baum-Welch algorithm to UTR sequences, and I'm grateful I had the holiday week to work on it. this project required significant time and careful thought to implement properly.

Tiange's excellent outline was invaluable in helping me work through the algorithm step by step. The pseudocode structure made it much easier to translate the mathematical concepts into working code, and our division of labor allowed us to tackle both the core algorithm and the biological application effectively.

I think one of the biggest takeaways from this project is that unsupervised learning algorithms like Baum-Welch can discover meaningful patterns in data without labeled examples. This is particularly powerful for biological sequences where we often don't know the "ground truth" annotations. The algorithm found structure in UTR sequences purely from the sequences themselves, which is both computationally elegant and biologically useful.

This is definitely a project I would like to expand on in the future. The framework we built could be adapted to other genomic regions or even entirely different types of sequential data, and I'm excited about the possibilities for future applications.

## Other member
Other members' reflections on the project

# Generative AI Appendix
claude sonnet 4.5 "help me organize my readme using markdown." 
