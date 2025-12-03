"""
Train HMM on 5' UTR sequences using Baum-Welch algorithm

This script loads UTR sequences and trains an HMM to identify
patterns in untranslated regions.

Authors: Nikaela Aitken & Tiange Feng
"""

import numpy as np
from baum_welch_hmm import HMM_Model, find_best_hmm, convert_hmm_params_to_matrices
from typing import List, Dict
import sys


def load_fasta_sequences(fasta_file: str, max_sequences: int = None) -> List[str]:
    """
    Load sequences from a FASTA file.

    Args:
        fasta_file: Path to FASTA file
        max_sequences: Maximum number of sequences to load (None for all)

    Returns:
        List of sequence strings
    """
    sequences = []
    current_seq = []

    try:
        with open(fasta_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith('>'):
                    # New sequence header
                    if current_seq:
                        seq = ''.join(current_seq).upper()
                        sequences.append(seq)
                        current_seq = []

                        if max_sequences and len(sequences) >= max_sequences:
                            break
                else:
                    # Sequence data
                    current_seq.append(line)

            # Add lastsequence
            if current_seq and (max_sequences is None or len(sequences) < max_sequences):
                seq = ''.join(current_seq).upper()
                sequences.append(seq)

    except FileNotFoundError:
        print(f"Error: File '{fasta_file}' not found.")
        print("Please run './download_utr_data.sh' first to download UTR sequences.")
        sys.exit(1)

    return sequences


def filter_sequences(sequences: List[str], min_length: int = 10,
                     max_length: int = 500) -> List[str]:
    """
    Filter sequences by length and valid nucleotides.

    Args:
        sequences: List of sequence strings
        min_length: Minimum sequence length
        max_length: Maximum sequence length

    Returns:
        Filtered list of sequences
    """
    valid_nucleotides = set('ACGT')
    filtered = []

    for seq in sequences:
        # Check  the length
        if len(seq) < min_length or len(seq) > max_length:
            continue

        # Check for valid nucleotides only
        if all(base in valid_nucleotides for base in seq):
            filtered.append(seq)

    return filtered


def analyze_sequences(sequences: List[str]) -> Dict:
    """
    Compute basic statistics about the sequences.

    Args:
        sequences: List of sequence strings

    Returns:
        Dictionary of statistics
    """
    lengths = [len(seq) for seq in sequences]
    total_bases = sum(lengths)

    # Count all the nucleotides
    base_counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0}
    for seq in sequences:
        for base in seq:
            if base in base_counts:
                base_counts[base] += 1

    stats = {
        'num_sequences': len(sequences),
        'min_length': min(lengths) if lengths else 0,
        'max_length': max(lengths) if lengths else 0,
        'mean_length': np.mean(lengths) if lengths else 0,
        'total_bases': total_bases,
        'base_frequencies': {base: count/total_bases for base, count in base_counts.items()}
    }

    return stats


def create_initial_utr_params(states: List[str], obs_alphabet: List[str],
                              base_frequencies: Dict[str, float] = None):
    """
    Create biologically-informed initial parameters for UTR analysis.

    Args:
        states: List of state names
        obs_alphabet: List of observation symbols (nucleotides)
        base_frequencies: Optional observed base frequencies

    Returns:
        Tuple of (init_probs, trans_probs, emit_probs)
    """
    # Default uniform base frequencies if not provided
    if base_frequencies is None:
        base_frequencies = {base: 0.25 for base in obs_alphabet}

    # Initial probabilities - uniform
    init_probs = {state: 1.0/len(states) for state in states}

    # Transition probabilities - slight self-preference
    trans_probs = {}
    for from_state in states:
        trans_probs[from_state] = {}
        for to_state in states:
            if from_state == to_state:
                trans_probs[from_state][to_state] = 0.7  # Stay in same state
            else:
                trans_probs[from_state][to_state] = 0.3 / (len(states) - 1)

    # Emission probabilities - start with observed frequencies
    emit_probs = {}
    for state in states:
        emit_probs[state] = {}
        for base in obs_alphabet:
            # Add small variation per state
            base_prob = base_frequencies.get(base, 0.25)
            emit_probs[state][base] = base_prob

    return init_probs, trans_probs, emit_probs


def main():
    """
    Main function to train HMM on UTR sequences.
    """
    print("=" * 60)
    print("Training HMM on 5' UTR Sequences")
    print("=" * 60)

    # Configuration
    FASTA_FILE = "human_five_prime_utrs.fa"
    MAX_SEQUENCES = 1000  # Use subset for faster training
    MIN_LENGTH = 20
    MAX_LENGTH = 300

    # HMM Configuration
    # States could represent: regulatory regions, stable vs  unstable structures, etc.
    STATES = ['UTR_A', 'UTR_B']  # Two-state model
    OBS_ALPHABET = ['A', 'C', 'G', 'T']

    # Training parameters
    NUM_RESTARTS = 5
    MAX_ITERATIONS = 100
    PSEUDOCOUNT = 0.01

    # Load sequences
    print(f"\nLoading sequences from {FASTA_FILE}...")
    sequences = load_fasta_sequences(FASTA_FILE, max_sequences=MAX_SEQUENCES)
    print(f"Loaded {len(sequences)} sequences")

    # Filter sequences
    print(f"\nFiltering sequences (length {MIN_LENGTH}-{MAX_LENGTH})...")
    filtered_seqs = filter_sequences(sequences, min_length=MIN_LENGTH,
                                     max_length=MAX_LENGTH)
    print(f"Retained {len(filtered_seqs)} sequences after filtering")

    if len(filtered_seqs) == 0:
        print("Error: No sequences passed filtering. Adjust parameters.")
        sys.exit(1)

    # Analyze sequence
    print("\n" + "=" * 60)
    print("Sequence Statistics")
    print("=" * 60)
    stats = analyze_sequences(filtered_seqs)
    print(f"Number of sequences: {stats['num_sequences']}")
    print(f"Sequence length range: {stats['min_length']}-{stats['max_length']}")
    print(f"Mean sequence length: {stats['mean_length']:.1f}")
    print(f"Total bases: {stats['total_bases']}")
    print("\nBase frequencies:")
    for base, freq in sorted(stats['base_frequencies'].items()):
        print(f"  {base}: {freq:.4f}")

    # Train HMM with random restarts
    print("\n" + "=" * 60)
    print("Training HMM with Baum-Welch Algorithm")
    print("=" * 60)
    print(f"States: {STATES}")
    print(f"Number of restarts: {NUM_RESTARTS}")
    print(f"Max iterations per restart: {MAX_ITERATIONS}")
    print()

    best_params, best_likelihood = find_best_hmm(
        training_obs_list=filtered_seqs,
        states_list=STATES,
        obs_alphabet=OBS_ALPHABET,
        num_restarts=NUM_RESTARTS,
        max_iterations_per_run=MAX_ITERATIONS,
        pseudocount=PSEUDOCOUNT,
        verbose=True
    )

    # Display the results
    print("\n" + "=" * 60)
    print("Final Trained HMM Parameters")
    print("=" * 60)
    print(f"\nBest Log-Likelihood: {best_likelihood:.4f}")
    print(f"Perplexity: {np.exp(-best_likelihood / stats['total_bases']):.4f}")

    print("\n--- Initial Probabilities ---")
    for state, prob in best_params[0].items():
        print(f"  π({state}) = {prob:.4f}")

    print("\n--- Transition Probabilities ---")
    for from_state in STATES:
        print(f"  From {from_state}:")
        for to_state in STATES:
            prob = best_params[1][from_state][to_state]
            print(f"    A({from_state} → {to_state}) = {prob:.4f}")

    print("\n--- Emission Probabilities ---")
    for state in STATES:
        print(f"  State {state}:")
        emissions = best_params[2][state]
        for base in OBS_ALPHABET:
            print(f"    B({state}, {base}) = {emissions[base]:.4f}")

    # Save model parameters
    print("\n" + "=" * 60)
    print("Saving Model")
    print("=" * 60)

    import pickle
    model_data = {
        'states': STATES,
        'obs_alphabet': OBS_ALPHABET,
        'initial_probs': best_params[0],
        'transition_probs': best_params[1],
        'emission_probs': best_params[2],
        'log_likelihood': best_likelihood,
        'training_stats': stats
    }

    with open('utr_hmm_model.pkl', 'wb') as f:
        pickle.dump(model_data, f)

    print("Model saved to: utr_hmm_model.pkl")
    print("\nTraining complete!")


if __name__ == "__main__":
    main()
