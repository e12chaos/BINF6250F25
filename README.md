# BINF6250F25
# Introduction
Description of the project

# Pseudocode
Put pseudocode in this box:

```
FUNCTION from_msa(fasta_filename, alphabet, pseudocount):

    # --- Step 1: Parse Data ---
    sequences = read_fasta_file(fasta_filename)
    num_seqs = length(sequences)
    seq_len = length(sequences[0])

    # --- Step 2: Determine Architecture (Match Columns) ---
    match_cols = []
    FOR col_index from 0 to seq_len:
        gap_count = count_gaps_in_column(sequences, col_index)
        
        # 50% Rule
        If gap_count < (0.5 * num_seqs):
            Append col_index TO match_cols

    L = length(match_cols)  # This is the length of our Profile HMM

    # --- Step 3: Define State Names ---
    # Create lists of state names based on length L
    match_states  = ["M0", "M1", ... "ML", "M(L+1)"]
    insert_states = ["I0", "I1", ... "IL"]
    delete_states = ["D1", "D2", ... "DL"]
    all_states = match_states + insert_states + delete_states

    # --- Step 4: Initialize Probabilities (Pseudocounts) ---
    # Create empty dictionaries for Transitions and Emissions
    trans_counts = {state: {} for state in all_states}
    emit_counts  = {state: {} for state in all_states}

    # Set up the allowed connections (Topology) with small pseudocounts
    FOR k from 0 to L:
        # Match transitions: M_k -> M_k+1, I_k, D_k+1
        # Insert transitions: I_k -> M_k+1, I_k, D_k+1
        # Delete transitions: D_k -> M_k+1, I_k, D_k+1
        Add pseudocount to allowed_transitions in trans_counts
    
    # Set up emissions for Match and Insert states (not Silent ones)
    FOR state in all_states:
        IF state is emitting (M or I):
            Add pseudocount to every character in alphabet in emit_counts

    # --- Step 5: Count Observed Transitions/Emissions ---
    FOR seq in sequences:
        current_state = "M0"
        match_node_index = 0  # We start at node 0

        FOR col_index, char in seq:
            
            IF col_index is in match_cols:
                match_node_index += 1
                
                IF char is not GAP:
                    # Case: Match
                    next_state = "M" + match_node_index
                    Increment trans_counts[current_state][next_state]
                    Increment emit_counts[next_state][char]
                    current_state = next_state
                Else:
                    # Case: Delete
                    next_state = "D" + match_node_index
                    Increment trans_counts[current_state][next_state]
                    current_state = next_state
            
            Else (It is an Insert column):
                IF char is not GAP:
                    # Case: Insert
                    next_state = "I" + match_node_index
                    Increment trans_counts[current_state][next_state]
                    Increment emit_counts[next_state][char]
                    current_state = next_state
                # Ignore gaps in insert columns

        # End of sequence: Transition to End state
        Increment trans_counts[current_state]["M(L+1)"]

    # --- Step 6: Normalize Counts to Probabilities ---
    # Convert absolute counts to percentages (0.0 to 1.0)
    final_trans = normalize_rows(trans_counts)
    final_emit  = normalize_rows(emit_counts)
    final_init  = {"M0": 1.0, others: 0.0}

    Retrun new HMM(final_init, final_trans, final_emit)
```

# Successes
Description of the team's learning points

# Struggles
Initially, I felt quite overwhelmed and confused by the extensive instructions and materials provided for this assignment. However, the algorithm structure provided by Marcus served as a crucial turning point. Once I reviewed that structure, the objective became clear: unlike our previous work, the core challenge here was to parse and organize the raw data effectively to feed into the HMM, ultimately training a model unique to our specific motif.

# Personal Reflections
## Group Leader(Nikaela Aitken)
Group leader's reflection on the project

## Other member (Tiange Feng)
I think the most successful aspect of our HMM-related projects—including this one—was the decision Nikaela and I made at the very beginning to establish a clear framework for representing the various variables. Given the number of variables inherent in HMM algorithms, this early agreement significantly streamlined our subsequent coding process. We have a effective synergy and happy collaboration.

# Generative AI Appendix
As per the syllabus
