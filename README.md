# BINF6250F25
# Introduction

This project implements a Profile Hidden Markov Model (Profile HMM) to model conserved protein motifs from multiple sequence alignments (MSAs). The implementation reads aligned FASTA files and automatically constructs a position-specific probabilistic model with three types of states: Match states (M) that capture conserved positions with column-specific amino acid distributions, Insertion states (I) that model variable-length insertions using a shared background distribution, and Delete states (D) that allow sequences to skip conserved positions. The model uses a left-to-right topology where sequences flow through the motif structure, with transitions constrained to move forward through Match blocks while allowing insertions and deletions. Key features include automated column classification using the 50% gap rule to distinguish match vs. insert columns, pseudocount-based parameter estimation from training alignments, and a custom Viterbi algorithm that properly handles silent (non-emitting) states for optimal sequence to motif alignment. The resulting model can score new protein sequences for motif presence and decode the most likely alignment path, making it useful for identifying distant homologs and characterizing protein families.

# Pseudocode

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
    
    # **NEW: Compute shared background distribution for all insertion states**
    background_dist = compute_background_distribution(sequences, alphabet, pseudocount)
    
    # Set up emissions for Match and Insert states (not Silent ones)
    FOR state in all_states:
        IF state is emitting (M or I):
            # **MODIFIED: Insertion states use shared background**
            IF state is Insert:
                emit_counts[state] = copy(background_dist)
            ELSE (state is Match):
                Add pseudocount to every character in alphabet in emit_counts[state]
    
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
                    # **REMOVED: Don't increment emit_counts (using global background)**
                    current_state = next_state
                # Ignore gaps in insert columns
        
        # End of sequence: Transition to End state
        Increment trans_counts[current_state]["M(L+1)"]
    
    # --- Step 6: Normalize Counts to Probabilities ---
    # Convert absolute counts to percentages (0.0 to 1.0)
    final_trans = normalize_rows(trans_counts)
    
    # **MODIFIED: Insertion states skip normalization (already normalized)**
    final_emit = {}
    FOR state in emit_counts:
        IF state is Insert:
            final_emit[state] = emit_counts[state]  # Already normalized
        ELSE:
            final_emit[state] = normalize_row(emit_counts[state])
    
    final_init  = {"M0": 1.0, others: 0.0}
    
    Return new HMM(final_init, final_trans, final_emit)


# **NEW HELPER FUNCTION**
FUNCTION compute_background_distribution(sequences, alphabet, pseudocount):
    counts = {char: pseudocount for char in alphabet}
    total = pseudocount * length(alphabet)
    
    FOR seq in sequences:
        FOR char in seq:
            IF char is not GAP and char in alphabet:
                Increment counts[char]
                Increment total
    
    # Normalize to probabilities
    Return {char: counts[char] / total for char in alphabet}
```

# Successes
Through this project, we gained hands on experience with the architectural differences between standard HMMs and Profile HMMs, particularly understanding how position specific models that capture biological sequence conservation. We learned the importance of proper state topology design—recognizing that Match, Insert, and Delete states serve fundamentally different roles and require different emission strategies (position-specific vs. background distributions). A major learning point was handling silent states in dynamic programming algorithms; we discovered that standard Viterbi fails when states don't emit and that silent states require special initialization and within timestep propagation. We also deepened our understanding of MSA interpretation, learning to classify alignment columns programmatically and  trace state paths through the aligned sequences to generate the training counts. Finally,  we practiced debugging complex probabilistic models by systematically testing topology construction, parameter estimation, and decoding algorithms separately.

# Struggles
Initially, I felt quite overwhelmed and confused by the extensive instructions and materials provided for this assignment. However, the algorithm structure provided by Marcus served as a crucial turning point. Once I reviewed that structure, the objective became clear: unlike our previous work, the core challenge here was to parse and organize the raw data effectively to feed into the HMM, ultimately training a model unique to our specific motif.

# Personal Reflections
## Group Leader(Nikaela Aitken)
I'm interested in continuing to learn about HMMs and finding new ways to apply them to some personal projects I've been thinking about. For Profile HMMs, I started by digging into what they were conceptually and understanding how they differ from standard HMMs. After reading through the provided script, my partner (Tiange) had some new sections written, so I focused on how to improve what she had scripted out and debug anything that I foresaw as being an issue. This included implementing the shared background distribution for insertion states, refining the path-tracing logic to properly handle match vs. insert columns, and  reworking the Viterbi algorithm to handle silent states. Working through these fixes gave me a much deeper appreciation for the biological motivation behind Profile HMMs—particularly how the three-state architecture can captures both conservation and variation in protein families. The debugging process was challenging but rewarding, especially when dealing with the subtleties of silent state propagation in dynamic programming. Moving forward, I'm excited to explore how Profile HMMs could be applied to other sequence analysis problems I'm working on.

## Other member (Tiange Feng)
I think the most successful aspect of our HMM-related projects—including this one—was the decision Nikaela and I made at the very beginning to establish a clear framework for representing the various variables. Given the number of variables inherent in HMM algorithms, this early agreement significantly streamlined our subsequent coding process. We have a effective synergy and happy collaboration.

# Generative AI Appendix
Claude sonnet 4.5 "dont adjust anything other than just fixing the spacing. dont change any typos or comments just the spacing" 
