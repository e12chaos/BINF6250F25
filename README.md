# Introduction
This project implements Markov chains to generate text based on probabilistic patterns learned from training data. We built both 1st order and Nth order Markov models that can analyze text patterns and generate new sentences following similar linguistic structures. The implementation includes functions to build Markov models from text, generate random text sequences, and process different types of literature from  Dr. Seuss and some Shakespeare's sonnets.

# Pseudocode


```
def build_markov_model(markov_model, new_text, order):
    * Can use defaultdict(Counter) for model structure
    * Prepend *S* and append *E* to the text
       * Pad the start with n *S*
    * Iterate from len(text) - order + 1 -- has to be +1 else we won't get *E*
    * Use a sliding window from i:i+order 
       * Current state -- text[i:i+order]
       * Next state -- text[i+order:i+order+1] -- this will grab just the next element, 
         but it will already be a list so it won't have to be converted
       * Call counter().update to update the model w/ frequencies. (Should be fine to do 
         this since Counter() will count the words if they are in a list, which we get 
         from the slice. Otherwise passing in plain strings would just count the 
         characters of the string)
    * Will also need to convert the frequencies into probabilities, can just do this 
      w/ dictionary comprehension in another function

def generate_random_text(markov_model, seed):
    * Initiate empty list of words []
    * Determining the starting state, need to account for the order (pad starting)
    * While state != *E*:
       * Get next word()
       * Append word to list
       * Also need to update the state as a sliding window, since these are tuples 
         could concat 2 tuples
    * Once we reach end, join words back into a string separated by spaces
    * Could add max_iter in case we get some unlikely scenarios which would prevent 
      too much text from being generated if we want

def get_next_word(current_word, markov_model, seed):
    * Set random seed for reproducibility
    * Extract possible next words and their frequencies from current state
    * Convert frequencies to probabilities by dividing by total count
    * Use np.random.choice with probability distribution to select next word
    * Return selected word
```

# Successes
Successfully implemented both 1st order and Nth order Markov chains with flexible order parameters
Created text generation that handles start/end states properly using S and E markers
Implemented proper probability calculations and random word selection using numpy
Successfully processed different types of text data including simple yet amazing Dr. Seuss repetitive patterns and complex Shakespeare sonnets
Developed modular functions that can be easily extended and reused for different text analysis tasks
Divide and Conquer - we worked asynchronously because our schedules were both busy, but managed to get the project done and build upon each other's work

# Struggles
Managing tuple states and ensuring proper concatenation for state transitions required careful debugging
Github
R ondemand 


# Personal Reflections
## Group Leader
Working on this Markov chains project highlighted several areas of growth for me. I'm still struggling with GitHub - the version control workflow and pushing from onDemand rstudio, but I recognize this is a crucial skill I need to develop for collaborative programming projects.
Having a good partner who was willing to help me troubleshoot made a significant difference in completing this assignment. Their patience when I got stuck on the infinite loop issue and their willingness to work asynchronously allowed us to make steady progress despite different schedules. This collaboration taught me the value of clear communication about coding problems and the importance of explaining what isn't working rather than just saying "it's broken."
I found myself doing a lot of YouTube videos to review Python dictionaries, particularly nested dictionary structures and the Counter class from collections. The concept of storing states as tuples for higher-order Markov models was initially confusing, and these additional resources helped solidify my understanding of how the data structures work together.

## Other member
Other members' reflections on the project

# Generative AI Appendix
