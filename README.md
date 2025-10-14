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

## Other member(Jacque Caldwell)
Our skills seemed to mesh.   I was able to describe how we were going to refer to the graph with nodes and edges, and she just got it.  We did get her going with her git "tab" on Explorer, and that made her life much simpler than having to do command line git commands.   We did forget to reverse the string in print_eulerian_walk, but that was easily fixed, and should appear in our final solution.  

I struggled a bit with list(strings) implementation, continuing to see set errors that seem to pop up at random times, this seems to be something to do with the interpreted nature of python.

After the project was completed, I did read in a DNA sequence, and attempt to use it with our list -- despite some initial "recursion limit level being reached", I was able to prove that given the start node sequences of 1000 characters could go down to a kmer length of about 7 before having issues not being able to recreate the original string.
## Other member
Working with Nikaela, we were able to hit the ground running, I had started implementing early, however, she was able to point out how some of
the functions could be done easier through the defaultdict class structure, so we changed up the code a bit.  

I did struggle with some python code early that was not allowing me to do a .append on a Dict(list()), it told me that it couldn't do a .append on 
a "set" type (it seemed to be telling me that it didn't know what my variable really was).  Changing the parameter to my function to define the parameter did not help, but it started working after I attempted to do an isinstanceof right before the .append.  

I also struggled to figure out why our graph printed out looked like the provided one, however, the provided lambda command would not print out our final Eulerian walk correctly.  I re-wrote it slightly and contacted Marcus -- not sure what is going on there.

Did some thinking about trying some of the DNA segments that were in last weeks project in order to figure out if I could see how increasing kmer length would improve output.

# Generative AI Appendix
As per the syllabus
