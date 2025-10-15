# BINF6250F25
# Introduction

Pairwise sequence alignment is a key technique in bioinformatics used to compare two biological sequences, whether they’re DNA, RNA, or proteins. It helps reveal regions of similarity that can point to shared function or evolutionary relationships.

The **dynamic programming** approach makes this process much more efficient. Instead of testing every possible alignment, it breaks the problem into smaller more manageable pieces and stores the results to avoid repeating work. This makes the process systematic and reduces the overall complexity to **O(m × n)**, which is far more practical for real data and real resources.

The **Smith-Waterman algorithm** is a  common dynamic programming methods used for **local sequence alignment**. It finds the best local match between two sequences by comparing all possible pairs of segments and identifying the highest-scoring region. This makes it especially useful for finding conserved domains or motifs between related sequences, since it builds a scoring matrix that highlights areas of strong similarity.


## Pseudocode

```python

# Purpose: Calculate the score for each cell in the alignment matrix
def cal_score
    Step 1: Calculate diagonal score
    # Compare seq1[i-1] with seq2[j-1]
    if seq1[i-1] == seq2[j-1]:
        diag_score = matrix[i-1][j-1] + match
    else:
        diag_score = matrix[i-1][j-1] + mismatch

    Step 2: Calculate up score (gap in seq2)
    up_score = matrix[i-1][j] + gap

    Step 3: Calculate left score (gap in seq1)
    left_score = matrix[i][j-1] + gap

    Step 4: Smith-Waterman special — include 0
    score = max(diag_score, up_score, left_score, 0)

    Step 5: Figure out which direction gave the max score
    # This will be used later for traceback
    return score


# Function: smith_waterman

def smith_waterman
    Step 1: Initialize matrices with zeros
    Step 2: Fill the matrices using cal_score for each cell
    Step 3: Find the position with the maximum score
    Step 4: Traceback starting from that max position
    Step 5: Return the aligned sequences and final alignment score
```

# Successes

Our main success was coordinating effectively as a team and completing the project early.

Brooks and I communicated   and divided the work efficiently; each taking specific functions while still reviewing and troubleshooting the other’s work collaboratively.

# Struggles
The main challenge was managing time due to my travel schedule for work. However, we mitigated this by setting internal deadlines and completing the code portion by end of day Sunday, well ahead of schedule.

Another area of difficulty was initially understanding the dynamic programming logic behind the Smith-Waterman algorithm, but consistent practice and reviewing external resources helped clarify the concepts.

Github has still been a struggle for me (Nikaela) I still fear it.

# Personal Reflections
## Group Leader(Nikaela Aitken)

I started this module the same way I approach most projects — by ensuring I conceptually understand the material before writing any code. This week was a little more complex and I wasn't sure I understood the global vs. local alignment I reviewed the class resources and supplemented them with YouTube videos and articles to help reinforce my understanding:

What Is Dynamic Programming? — Spiceworks

YouTube: Smith-Waterman Explained

I think this project went really well. Brooks and I connected early, divided our tasks, and ended up collaborating on the final function — I drafted the skeleton while he integrated his function and handled debugging.

Despite traveling for work during the project, clear communication and planning allowed us to finish ahead of schedule. Brooks was awesome in that he went along with my desire to finish the coding by Sunday because of my work schedule these two weeks. 

I’m not sure if this assignment was simply more straightforward or if I’m finally getting a stronger handle on Python, but it felt smoother overall. Reading more about NumPy and learning to leverage libraries effectively has made coding much more efficient — something I realized after the previous assignment. I spent some time figuring out the libraries a bit, which helped me to use them efficiently. 



## Other member
Other members' reflections on the project

# Generative AI Appendix
As per the syllabus
