# BINF6250F25
# Introduction

This project implements a Neighbor-Joining (NJ) algorithm for constructing phylogenetic trees from HIV-1 reverse transcriptase protein sequences. Unlike simpler clustering methods like UPGMA, Neighbor-Joining produces unrooted trees and does not assume a constant evolutionary rate across lineages, making it more biologically realistic for analyzing viral sequence relationships.

# Pseudocode
Put pseudocode in this box:

```

```

# Successes

- **Improved use of NumPy:** Rewrote `get_min_distance()` to leverage NumPy’s built-in matrix operations instead of manual loops, which made the code both shorter and faster.

- **Deeper conceptual understanding:** Gained stronger intuition about the relationship between distance matrices and tree topology, and how NJ avoids the constant-rate assumption of UPGMA.

- **Modular structure:** Reused and refined the Smith-Waterman implementation from a previous project, improving normalization and integration with later steps.

- **Testing and debugging practice:** Developed small-scale test cases (like short artificial sequences) to validate functions independently before integration.


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
Other members' reflections on the project

# Generative AI Appendix
ChatGPT (GPT-5) was used for: Refining markdown formatting and documentation structure along with providing feedback on readability and logical organization

All algorithmic logic, testing, and implementation code were written by the team.

"help me with my readme" + (current readme input) + code 

