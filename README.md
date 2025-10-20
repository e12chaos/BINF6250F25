# BINF6250F25
# Introduction
Description of the project

# Pseudocode
Put pseudocode in this box:

```
def read_fasta(filename: str) -> Dict[str, str]:
    """Reads sequences from FASTA file.

    Args:
        filename (str): Path to FASTA file containing HIV RT sequences

    Returns:
        Dict[str, str]: Dictionary mapping sequence IDs to sequences

    Examples:
        >>> seqs = read_fasta("lafayette_SARS_RT.fasta")
        >>> len(seqs) > 0
        True
    """
read in the file
take the accession number as key (its the line with ">" and its the number between the 
third "|" and fourth "|")
skip a line and get the sequence until a line hits ">".
then for the line where we get ">", repeat previous loop until lines are empty


    
    
def smith_waterman(
    sequence1: str,
    sequence2: str,
    match_score: float = 2.0,
    mismatch_penalty: float = -1.0,
    gap_penalty: float = -1.0
) -> float:
    """Implements Smith-Waterman local alignment algorithm.

    Args:
        sequence1 (str): First HIV RT sequence
        sequence2 (str): Second HIV RT sequence
        match_score (float): Score for matching characters
        mismatch_penalty (float): Penalty for mismatched characters
        gap_penalty (float): Penalty for gaps

    Returns:
        float: Normalized similarity score between sequences

    Examples:
        >>> seq1 = "ACGT"
        >>> seq2 = "ACGT"
        >>> smith_waterman(seq1, seq2)
        1.0
    """
take in two sequences
initialize a matrix to perform smith-waterman local alignment
score matrix one by one for the local alignment
Grab the best score for the alignment
divide by the number if sequences were identical to normalize score
return normalized similarity score between sequences

    
    
def build_distance_matrix(sequences: Dict[str, str]) -> Tuple[np.ndarray, List[str]]:
    """Builds distance matrix using Smith-Waterman scores.

    Args:
        sequences (Dict[str, str]): Dictionary of HIV RT sequences

    Returns:
        Tuple[np.ndarray, List[str]]: Distance matrix and list of sequence IDs

    Examples:
        >>> seqs = read_fasta("lafayette_SARS_RT.fasta")
        >>> mat, ids = build_distance_matrix(seqs)
        >>> mat[0:3, 0:3]  # Show 3x3 slice of distance matrix
        array([[0.000, 0.004, 0.012],
              [0.004, 0.000, 0.012],
              [0.012, 0.012, 0.000]])
        >>> len(ids)  # Number of sequences
        19
    """
take in dictionary of HIV RT Sequences from read_fasta()
call smith_waterman algorith to calculate similarity scores between sequences
distance is 1 - normalized similarity score. Perform that for each score
store scores in matrix (len(dictionary) X len(dictionary)) for comparing scores
create list of dictionary keys (sequence IDs)
    
    
def get_min_distance(matrix):
    ''' Function to find the smallest value off-daigonal in the distance
    matrix provided. This is used in the UPGMA algorithm.
    
    Args: 
        matrix (2D numpy array): a distance matrix

    Returns:
        min (float): The smallest distance in the matrix
        pos (tuple): The x and y position of the smallest distance
take in distance matrix
find minimum value in the distance matrix
now find the distance of that minimum value to the other sequences
Distance can be calculated with distance with:
d((AB), C) = (d(A,C) + d(B,C)) / 2
d((AB), D) = (d(A,D) + d(B,D)) / 2
remove the already calculated row and column
repeat until each distance is calculated


        
        
def neighbor_joining(
    distance_matrix: np.ndarray,
    labels: List[str]
) -> str:
    """Implements Neighbor-Joining algorithm for phylogenetic tree construction.

    Args:
        distance_matrix (np.ndarray): Distance matrix from Smith-Waterman scores
        labels (List[str]): Sequence identifiers

    Returns:
        str: Newick format tree string

    Examples:
        >>> seqs = read_fasta("lafayette_SARS_RT.fasta")
        >>> mat, ids = build_distance_matrix(seqs)
        >>> tree = neighbor_joining(mat, ids)
        >>> tree.startswith("((DM1:0.002,DM2:0.002)")  # Start of Newick string
        True
        >>> tree.count(",")  # Number of separators in tree
        18
    """
    
def plot_tree(newick_tree: str) -> None:
    """Plots phylogenetic tree using ete3.

    Args:
        newick_tree (str): Tree in Newick format
    """
```

# Successes
Description of the team's learning points

# Struggles
Description of the stumbling blocks the team experienced

# Personal Reflections
## Group Leader(Nikaela Aitken)
Group leader's reflection on the project

## Other member
Other members' reflections on the project

# Generative AI Appendix
As per the syllabus
