# BINF6250F25
# Introduction

This project implements a Neighbor-Joining (NJ) algorithm for constructing phylogenetic trees from HIV-1 reverse transcriptase protein sequences. Unlike simpler clustering methods like UPGMA, Neighbor-Joining produces unrooted trees and does not assume a constant evolutionary rate across lineages, making it more biologically realistic for analyzing viral sequence relationships.

# Pseudocode
Put pseudocode in this box:

```
fucntion read_fasta(filename:fasta file)
    initialize a dictionary
    open fasta file and iterate through
    
    if line starts with ">" then grab accession number (sequence ID) and 
    add as key to dictionary. 
    If line does not start with ">" then add sequence lines to the current accession
    number as a value
    
function smith_waterman
    calculate the matrix dimensions
    fill matrix with scores
    normalize the scores

function build_distance_matrix
    create sequence id list
    initialize matrix for distances
    fill distance matrix with similarity scores between sequences
    
function get_min_distances
    create dictionary
    ignore diagonal values
    find position and value of minimum value in matrix
    
function neighbor_joining
    Initialize - Set up data structures
    Main Loop - Repeat until 2 nodes left
    Q-Matrix - Calculate corrected distances
    Find Minimum - Identify closest pair
    Branch Lengths - Calculate how far each node is from their parent
    Update Matrix - Merge nodes and recalculate distances
    Build Newick - Convert tree structure to string format
    
    
```

# Successes

- **Improved use of NumPy:** Rewrote `get_min_distance()` to leverage NumPy’s built-in matrix operations instead of manual loops, which made the code both shorter and faster.

- **Deeper conceptual understanding:** Gained stronger intuition about the relationship between distance matrices and tree topology, and how NJ avoids the constant-rate assumption of UPGMA.

- **Modular structure:** Reused and refined the Smith-Waterman implementation from a previous project, improving normalization and integration with later steps.

- **Testing and debugging practice:** Developed small-scale test cases (like short artificial sequences) to validate functions independently before integration.

- **Team coordination:** Able to coordinate with Allen via Microsoft Teams since our schedules didn’t align this week.

- **Commenting and documentation:** Made sure to leave detailed comments throughout the code—both from previous notes and to help my partner easily follow my logic and implementation decisions.



# Struggles

- **ETE3 visualization issues:** Spent hours troubleshooting `ete3` installation and runtime errors in the environment. Ultimately decided to focus on algorithm correctness before revisiting visualization.

- **Version control:** GitHub synchronization was unexpectedly complicated due to environment differences between Discovery and GitHub, leading to manual copy-paste corrections.

- **Conceptual pacing:** The combination of biological and computational logic (alignment → distance → tree construction) felt abstract at first, especially while balancing a heavy work schedule and illness.


# Personal Reflections
## Group Leader(Nikaela Aitken)

This was one of the hardest assignments for me, not because I think the material is super hard but because my schedule had been so full and then I got sick while traveling for work and when I started the assignment I wasn't already comfortable with the structural idea of what we were doing so I was basically in a flat out panic that had my planning session less productive than it normally was, which in turn led to me making some dumb mistakes and having to go back and totally rework sections, for example the `get_min` I originally wrote a loop and didn't take advantage at all of numpy. When I rewrote it, it was so much shorter and clearer and able to handle more faster.

Also I could not get the `ete3` to work, I spent hours trying to get this working before I decided just to focus on the rest of the code and come back to that issue later.

One thing that did come out of the mess I was making at the start of the assignment was a lot of testing on some of the later functions.

Also I still suck at GitHub. I somehow got my discovery environment out of sync with my GitHub and ended up copying pasting sections of the code directly into git to try and fix it all.

Side note: I liked that we were able to use a part of our code from the last assignment, I liked building on that.

## Other member
This was definitely a difficult assignment. Understanding the process for neighbor joining took some
extra research outside of class. It took a while to write the pseudocode since getting a good grip
on understanding took a while. I did run into some issues when attempting to write the neighbor joining
function where I was unable to correctly update the nodes in my version. My partner was successfully able
to update the nodes and so we went along with here version of the function. As I am stillimproving on my 
code its interesting to be exposed to different scenarios for learning. This project felt much math heavier
than other projects so I struggled to fully translate the process into code.

# Generative AI Appendix
ChatGPT (GPT-5) was used for: Refining markdown formatting and documentation structure along with providing feedback on readability and logical organization

All algorithmic logic, testing, and implementation code were written by the team.

"help me with my readme" + (current readme input) + code 

