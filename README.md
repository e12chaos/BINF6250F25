# BINF6250F25
# Introduction
This project implements a De Bruijn graph–based algorithm to reconstruct paths from k-mers in a given input string.  
We used Python to represent the graph with dictionaries and performed a recursive Eulerian walk to produce the final tour.

# Pseudocode
- **add_edge(self, left, right)**
  - Access the graph dictionary.  
  - Add `right` to the list at key `left`.  
  - `self.graph[left].append(right)`

- **remove_edge(self, left, right)**
  - Similar to `add_edge`, but use `remove` instead.  
  - `self.graph[left].remove(right)`

- **build_debruijn_graph(self, input_string, k)**
  - Extract k-mers from the input string.  
  - Split each k-mer into `left` and `right`.  
  - Call the `add_edge` function above to build the graph.  
  - Save the first k-mer as the starting node.

- **eulerian_walk(self, node, seed=None)**
  - Begin the walk at the starting node.  
  - For each node:  
    - Follow a random valid edge from the node.  
    - Remove that edge after using it.  
    - Recurse to continue the walk.  
  - Recursion stops when the current node has no remaining edges.  
  - Always check if a node still has edges before continuing.

```
Some pseudocode here
```

# Successes
- Clarified De Bruijn graph principles through early team discussions.  
- Simplified `add_edge` and `remove_edge` to single-line operations by using **`defaultdict(list)`**.  
- Strengthened understanding of recursion and graph traversal in Python.  
- Gained experience with GitHub for version control and collaboration.

# Struggles
- Learning to structure the project within a class-based design rather than only standalone functions.  
- Debugging edge removal during recursion to avoid skipped or duplicated nodes.  
- Adjusting logic to make the last line of the expected output align with the sample output. Especially the last line 
- Initial friction getting our GitHub workflow set up for collaborative coding. aka Nikaela struggles

# Personal Reflections
## Group Leader(Nikaela Aitken)
Working with Jacqueline in the early pseudocode sessions helped clarify core graph-assembly concepts.  
During code reviews, I noticed how others leveraged Python libraries effectively, which motivated me to explore **class functions** and especially **`collections.defaultdict`**.  

Resources that were most helpful:  
- [Using defaultdict in Python (YouTube)](https://www.youtube.com/watch?v=JH4q65dZPvY)  
- [Intro to Python Class Functions (YouTube)](https://www.youtube.com/watch?v=UtkTd8UaxEo)  
- [De Bruijn Graphs for Genome Assembly – Lecture Notes (JHU)](https://www.cs.jhu.edu/~langmea/resources/lecture_notes/assembly_dbg.pdf)

Using these, we reduced the `add_edge` and `remove_edge` logic from ~8 lines down to 1 line each, making the code cleaner and more efficient.

I was actually surprised that this assignment took less time than our previous ones (though it was still time intensive). Since we finished early, we had the chance to discuss how we might apply this approach to DNA and even ancient DNA assembly.

## Other member
Other members' reflections on the project

# Generative AI Appendix
As per the syllabus
