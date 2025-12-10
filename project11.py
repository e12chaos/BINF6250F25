import numpy as np            # Workhorse
import numpy.random as nr     # Setting up random distributions
from copy import deepcopy     # For convergence checking

# --- [START] NEW IMPORTS ---
import sys
# --- [END] NEW IMPORTS ---

try:
    # Special Json library wrapper
    import ujson as json
    def to_json(data, precision = 2):
        return json.dumps(data, indent = 4, double_precision = precision)
except ImportError:
    import json
    def to_json(data, precision = 2):
        # Fallback wrapper
        return json.dumps(data, indent=4)

class HMM:
    """
    Main HMM class for Profile HMM implementation.
    Includes storage for model parameters and methods for training/decoding.
    """

    def __init__(self, init_probs, trans_probs, emit_probs):
        """
        Initialize the HMM object.
        """
        self.init_probs = init_probs
        self.trans_probs = trans_probs
        self.emit_probs = emit_probs

        self.hidden_states = list(self.trans_probs.keys())
        # Infer alphabet from the first emitting state found
        for state in self.emit_probs:
            if self.emit_probs[state]:
                self.alphabet = list(self.emit_probs[state].keys())
                break

    # -------------------------------------------------------------------------
    # ### NEW CODE SECTION: Profile HMM Construction ###
    # -------------------------------------------------------------------------



    @staticmethod
    def _compute_background_dist(sequences, alphabet, pseudocount):
        """Compute global amino acid frequencies for insertion states."""
    #Initialize the  counts with pseudocount to avoid zero probabilities
        counts = {char: pseudocount for char in alphabet}
        total = pseudocount * len(alphabet)
    #Count occurrences of each amino acid across all sequences. We include residues from both match and insert columns since this     represents the general background compositon   
        for seq in sequences:
            for char in seq:
                if char != '-' and char in counts:
                    counts[char] += 1
                    total += 1
        
        return {char: counts[char] / total for char in alphabet}

    @classmethod
    def from_msa(cls, fasta_file, alphabet="ACDEFGHIKLMNPQRSTVWY", pseudocount=0.1):
        """
        [NEW METHOD]
        Constructs a Profile HMM directly from a Multiple Sequence Alignment (MSA).

        Args:
            fasta_file (str): Path to the aligned FASTA file.
            alphabet (str): String of allowed characters (default: Protein AA).
            pseudocount (float): Small number added to counts to prevent zero probabilities.

        Returns:
            HMM: An initialized HMM object.
        """
        # 1. Parse Fasta
        sequences = []
        try:
            with open(fasta_file, 'r') as f:
                current_seq = []
                for line in f:
                    line = line.strip()
                    if line.startswith(">"):
                        if current_seq: sequences.append("".join(current_seq))
                        current_seq = []
                    else:
                        current_seq.append(line)
                if current_seq: sequences.append("".join(current_seq))
        except FileNotFoundError:
            print(f"Error: File {fasta_file} not found.")
            return None

        if not sequences:
            raise ValueError("No sequences found in FASTA file.")

        # 2. Determine Match Columns (50% Rule)
        seq_len = len(sequences[0])
        num_seqs = len(sequences)
        match_cols = []

        for col_idx in range(seq_len):
            gap_count = sum(1 for seq in sequences if seq[col_idx] == '-')
            # If gaps are less than 50%, it's a Match column
            if gap_count < (0.5 * num_seqs):
                match_cols.append(col_idx)

        L = len(match_cols) # Length of the model (number of Match states)

        # 3. Define States
        # M0 = Begin, M{L+1} = End
        match_states  = [f"M{i}" for i in range(L + 2)]
        insert_states = [f"I{i}" for i in range(L + 1)] # I0 to IL
        delete_states = [f"D{i}" for i in range(1, L + 1)] # D1 to DL

        all_states = match_states + insert_states + delete_states

        # 4. Initialize Counts with Pseudocounts
        # Initialize Transition Dictionary
        trans_counts = {s: {} for s in all_states}

        # Define Allowed Transitions (Topology)
        # From Mk, Ik, Dk -> M(k+1), I(k), D(k+1)
        # Note: boundary conditions (Start M0 and End M_Last)

        # Helper to safely init a transition if valid
        def add_edge(u, v):
            trans_counts[u][v] = pseudocount

        # Initialize standard Profile HMM topology
        for k in range(L + 1): # 0 to L
            current_M = f"M{k}"
            current_I = f"I{k}"
            current_D = f"D{k}" # Might not exist for k=0

            next_M = f"M{k+1}"
            next_I = f"I{k}"    # Self loop
            next_D = f"D{k+1}" if (k+1) <= L else None

            # Transitions from Match (k)
            add_edge(current_M, next_M)
            add_edge(current_M, next_I)
            if next_D: add_edge(current_M, next_D)

            # Transitions from Insert (k)
            add_edge(current_I, next_M)
            add_edge(current_I, next_I)
            if next_D: add_edge(current_I, next_D)

            # Transitions from Delete (k) - D0 doesn't exist
            if k > 0:
                add_edge(current_D, next_M)
                add_edge(current_D, next_I)
                if next_D: add_edge(current_D, next_D)

        # Initialize Emission Dictionary
        emit_counts = {s: {} for s in all_states}
        alpha_list = list(alphabet)

        # Compute background distribution for ALL insertion states
        background_dist = HMM._compute_background_dist(sequences, alphabet, pseudocount)

        for s in all_states:
            # Silent states (M0, End, Deletes) do not emit
            if s == "M0" or s == f"M{L+1}" or s.startswith("D"):
                continue

            # Insertion states use shared background distribution
            if s.startswith("I"):
                emit_counts[s] = background_dist.copy()
            else:
                # Match states get position-specific distributions
                for char in alpha_list:
                    emit_counts[s][char] = pseudocount

        # 5. Count Transitions and Emissions from Data
        for seq in sequences:
            curr_state = "M0"
            match_idx = 0  # Which match node we've PASSED (0 initially, before M1)

            for col_idx, char in enumerate(seq):
                is_match_col = col_idx in match_cols

                if is_match_col:
                    # Entering a new match column block
                    match_idx += 1
                    
                    if char != '-':
                        # Match State
                        next_state = f"M{match_idx}"
                        trans_counts[curr_state][next_state] += 1
                        emit_counts[next_state][char] += 1
                        curr_state = next_state
                    else:
                        # Delete State (gap in match column)
                        next_state = f"D{match_idx}"
                        trans_counts[curr_state][next_state] += 1
                        curr_state = next_state

                else:
                    # Insert column - emissions go to I{match_idx}
                    # match_idx tells us which match node we're "after"
                    if char != '-':
                        next_state = f"I{match_idx}"
                        trans_counts[curr_state][next_state] += 1
                        # Don't count emissions for background dist
                        # (already computed globally)
                        curr_state = next_state
                    # If char is '-', ignore (gap in insert column)

            # End of sequence -> Transition to End State
            end_state = f"M{L+1}"
            if end_state in trans_counts[curr_state]:
                trans_counts[curr_state][end_state] += 1

        # 6. Normalize Counts to Probabilities

        # Init probs: Always start at M0 with probability 1.0
        final_init = {s: 0.0 for s in all_states}
        final_init["M0"] = 1.0

        # Normalize Transitions
        final_trans = {}
        for src, targets in trans_counts.items():
            total = sum(targets.values())
            final_trans[src] = {}
            if total > 0:
                for dest, count in targets.items():
                    final_trans[src][dest] = count / total

        # Normalize Emissions
        final_emit = {}
        for state, emissions in emit_counts.items():
            final_emit[state] = {}
            if not emissions: continue # Skip silent states

            # Insertion states already have normalized background distribution
            if state.startswith("I"):
                final_emit[state] = emissions  # Already normalized
            else:
                # Normalize Match states
                total = sum(emissions.values())
                if total > 0:
                    for char, count in emissions.items():
                        final_emit[state][char] = count / total

        print(f"Profile HMM created with Length L={L}")
        return cls(final_init, final_trans, final_emit)

    # -------------------------------------------------------------------------
    # ### END NEW CODE SECTION ###
    # -------------------------------------------------------------------------

    def __str__(self):
        """String representation of HMM (JSON format)."""
        return to_json({
            "init_probs": self.init_probs,
            "trans_probs": self.trans_probs,
            "emit_probs": self.emit_probs
        })


    def viterbi(self, observation):
        """
        Viterbi Algorithm adapted for Profile HMMs with silent states.
        
        Args:
            observation (str): Input sequence (e.g., "VGQDH").
        
        Returns:
            tuple: (best_prob, best_path_list)
        """
        obs_len = len(observation)
        
        # Identify state types
        match_states = [s for s in self.hidden_states if s.startswith("M")]
        insert_states = [s for s in self.hidden_states if s.startswith("I")]
        delete_states = [s for s in self.hidden_states if s.startswith("D")]
        
        # DP tables
        v = [{} for _ in range(obs_len + 1)]
        backptr = [{} for _ in range(obs_len + 1)]
        
        # Initialize at t=0 (before any emissions)
        v[0]["M0"] = 0.0  # log(1.0) = 0
        backptr[0]["M0"] = None
        
        # Propagate silent states at t=0 (only D1 is reachable from M0)
        for state in delete_states:
            v[0][state] = -np.inf
            backptr[0][state] = None
        
        # Check if we can reach D1 from M0 at t=0
        if "D1" in self.trans_probs.get("M0", {}):
            v[0]["D1"] = v[0]["M0"] + np.log(self.trans_probs["M0"]["D1"] + 1e-300)
            backptr[0]["D1"] = "M0"
            
            # Propagate through deletion chain at t=0
            for state in sorted(delete_states):
                if v[0][state] > -np.inf:
                    for next_state in self.trans_probs.get(state, {}):
                        if next_state in delete_states:
                            new_prob = v[0][state] + np.log(self.trans_probs[state][next_state] + 1e-300)
                            if new_prob > v[0].get(next_state, -np.inf):
                                v[0][next_state] = new_prob
                                backptr[0][next_state] = state
        
        # Main recursion
        for t in range(1, obs_len + 1):
            obs_char = observation[t-1]
            
            # Initialize all states at time t
            for state in self.hidden_states:
                v[t][state] = -np.inf
                backptr[t][state] = None
            
            # Process emitting states (Match and Insert)
            for state in match_states + insert_states:
                # Skip Begin and End
                if state == "M0" or state == f"M{len(match_states)-1}":
                    continue
                
                # Check if this state can emit the observation
                if state not in self.emit_probs or obs_char not in self.emit_probs[state]:
                    continue
                
                emit_prob = np.log(self.emit_probs[state][obs_char] + 1e-300)
                
                # Find best predecessor from t-1
                best_prob = -np.inf
                best_prev = None
                
                for prev_state in self.hidden_states:
                    if v[t-1][prev_state] > -np.inf:
                        if state in self.trans_probs.get(prev_state, {}):
                            trans_prob = np.log(self.trans_probs[prev_state][state] + 1e-300)
                            candidate = v[t-1][prev_state] + trans_prob + emit_prob
                            if candidate > best_prob:
                                best_prob = candidate
                                best_prev = prev_state
                
                v[t][state] = best_prob
                backptr[t][state] = best_prev
            
            # Process silent states (Deletions) at time t
            # These can be reached from emitting states at time t (same timestep)
            changed = True
            while changed:
                changed = False
                for state in delete_states:
                    for prev_state in self.hidden_states:
                        if v[t][prev_state] > -np.inf:
                            if state in self.trans_probs.get(prev_state, {}):
                                trans_prob = np.log(self.trans_probs[prev_state][state] + 1e-300)
                                candidate = v[t][prev_state] + trans_prob
                                if candidate > v[t][state]:
                                    v[t][state] = candidate
                                    backptr[t][state] = prev_state
                                    changed = True
        
        # Termination - find best path to End state
        end_state = match_states[-1]  # M_{L+1}
        
        # End state can be reached from any state at t=obs_len
        best_prob = -np.inf
        best_last = None
        
        for state in self.hidden_states:
            if v[obs_len][state] > -np.inf:
                if end_state in self.trans_probs.get(state, {}):
                    trans_prob = np.log(self.trans_probs[state][end_state] + 1e-300)
                    candidate = v[obs_len][state] + trans_prob
                    if candidate > best_prob:
                        best_prob = candidate
                        best_last = state
        
        # Traceback
        if best_last is None:
            return -np.inf, []
        
        path = [end_state]
        current = best_last
        t = obs_len
        
        while current is not None and current != "M0":
            path.append(current)
            prev = backptr[t][current]
            
            # Determine if we move back in time
            if current in match_states or current in insert_states:
                if current != "M0":
                    t -= 1
            
            current = prev
        
        path.append("M0")
        path.reverse()
        
        return best_prob, path


# -------------------------------------------------------------------------
# ### NEW MAIN BLOCK FOR TESTING ###
# -------------------------------------------------------------------------

if __name__ == "__main__":
    # Example Usage
    print("--- Training Profile HMM from Motif 1 ---")
    hmm = HMM.from_msa("phmm_train_motif1.fasta", alphabet="ACDEFGHIKLMNPQRSTVWY")

    if hmm:
        # Print a snippet of the model
        print("\nModel Initialized.")
        print(f"States: {len(hmm.hidden_states)}")
        print(f"Transition M0->M1: {hmm.trans_probs['M0'].get('M1', 0):.4f}")

        # Test sequences
        test_seqs = ["VGQDH", "AAAAA"]
        print("\n--- Testing Sequences (Viterbi Scores) ---")
        for seq in test_seqs:
            try:
                score, path = hmm.viterbi(seq)
                print(f"Seq: {seq} | Log-Score: {score:.2f} | Path: {path}")
            except Exception as e:
                print(f"Seq: {seq} | Error calculating score (Silent state handling in Viterbi might be limited)")
