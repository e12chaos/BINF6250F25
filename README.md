# BINF6250F25
# Introduction

This project implements the Burrows-Wheeler Transform (BWT) and related algorithms for efficient string processing and pattern matching. The implementation includes:

- **Suffix Array Construction**: Creates a sorted array of all suffix positions in a string
- **BWT Generation**: Computes the Burrows-Wheeler Transform from a suffix array
- **Character Counting Functions**: Calculates cumulative character counts and occurrence maps for efficient pattern searching
- **BWT Inversion**: Reconstructs the original string from its BWT representation

These components form the foundation for advanced text compression and searching algorithms used in bioinformatics applications like genome alignment and sequence analysis.

# Pseudocode
Put pseudocode in this box:

```


def BWT(string: str) -> str:

    #Make string into list of individual characters, put $ in last position
    string = list(string)

    # Establish empty nxn matrix where n is len(string)
    bwt_matrix = np.empty((n,n), dtype = str)

    # For loop for each row:
    for row in bwt_matrix:
	  # Insert list as the row
        row = string
	  # Pop first element and insert that as last element in list
        string.insert(0, string.pop(:-1))

    # Take matrix and numpy sort along axis 0 (rows)
    np.sort(bwt_matrix, axis = 0)

    # Take last column of matrix and establish that as bwt
    bwt = bwt_matrix[:,-1]

    return bwt 

def suffix_array(string: str) -> list[int]:
   
# Create a list of all suffices of the text, each paired with its starting position
suffixes = []
for i in range(len(string)-1):
suffixes.append(string[i:len(string)])

# Sort these suffix-position pairs lexicographically by suffix
positions = list(range(len(string)))
suffixes = list(zip(suffixes, positions))
suffixes.sort()

# Extract just the starting positions from the sorted pairs
suffix_array = [pair[1] for pair in suffixes]

# Return the list of sorted starting positions
return suffix_array

def BWT_from_suffix_array(

# Initialize an empty string of the same length as the input text
bwt = “”

# for each position in the suffix positions list do
# if the suffix starts at the beginning of the text then
# 	Add the last character of the text to the transformed result
# else
# 	Add the character preceding the suffix to the transformed result
for position in suffix_positions:
bwt = bwt + string[position-1]

# return the transformed result
return bwt

from collections import Counter


def cal_count(string: str) -> dict[str, int]:
   
# Initialize a dictionary to track character counts
chars = Counter(string)

# Initialize a result dictionary for cumulative counts
# Set initial cumulative count to zero
counts = chars.clear()

# for each character in the sorted alphabet do
# Store the current cumulative count for this character
# Increase the cumulative count by the frequency of this character
for char in chars:
	for compare in chars:
		if compare > char:
			counts[char] += chars[compare]

# return the dictionary of cumulative counts
return counts



def cal_occur(bwt_string: str) -> dict[str, list[int]]:
    
# Initialize a dictionary mapping each character to an array of zeros
characters = Counter(bwt_string)
Characters = characters.clear()
occur_map = defaultdict(list)
for char in characters:
	occur_map[char].append(0)

# for each position in the transformed text do
# Identify the character at the current position
# for each character in the alphabet do
# Copy the previous occurrence count to the current position
# Increment the occurrence count for the current character
for char in bwt_string:
	characters[

# return the dictionary of occurrence counts

def update_range(
  lower: int, 
  upper: int, 
  count: dict[str, int], 
  occur: dict[str, list[int]], 
  a: str) -> tuple[int, int]:
   
# Calculate new start position using character's count and occurrences at range start
# Calculate new end position using character's count and occurrences at range end
# return new start and end positions

We need to find which of the 'a' rows match our search
We use occur['a'] to count how many 'a's we've seen
Start at where the 'a' rows begin:

Add how many 'a's we need to skip based on our current position


def find_match(query: str, reference: str) -> list[int]:
    
# Initialize search range to cover the entire transformed text
# for each character in the pattern, processing from right to left do
# Update the search range based on the current character
# if the range becomes empty then
# return empty list as pattern is not found
# Collect all suffix positions within the final range
# return the list of matching positions

# Step 1: Get the BWT and other data structures
# Step 2: Initialize the range
# Step 3: Loop through query backwards
# Update range # Check if empty # Step 4: Collect matching positions # Step 5: Return results





```

# Successes
- **Effective collaboration**: Coordinating with my partner (Jason) to establish clear goals and timelines. We decided to aim for completion by Sunday night, which felt challenging over the weekend but ultimately gave us extra time for code cleanup and optimization.
- **Strong time management**: Finishing ahead of schedule allowed us to refine our implementation and strengthen the codebase. Plus the added benefit of not stressing abou itthe night before 
- **Meeting project objectives**: Successfully implemented all required functions with proper documentation and added some test cases.

# Struggles
- **Conceptual challenges**: Understanding the inverse BWT function and why the algorithm needed to work in reverse order took significant effort.
- **Debugging**: Working through indentation errors and logical bugs in the initial implementations required careful attention to detail.
- **Algorithm complexity**: Grasping how the different components (suffix arrays, character counts, occurrence maps) work together in the larger BWT framework.

# Personal Reflections
## Group Leader(Nikaela Aitken)
This project went pretty smoothly overall. I made a conscious decision not to repeat my approach from last week! instead, I invested time in reading documentation and watching educational videos to better understand the BWT algorithm conceptually before diving into the code. This preparation paid off, as I was able to grasp the underlying logic more thoroughly and contribute more effectively to the implementation. I really appreciate Jason being so on board to try and get this project done Sunday night as I knew my work week was going to be very busy. He was a great partner and we split up the functions and worked off our pseudocode. I was very grateful that so much pseudocode was provided. I think conceptually this was a harder topic and it was a relief that the proejct actually felt doable rather than smothering. 


## Other member
Other members' reflections on the project

# Generative AI Appendix
Nikaela - I used AI to help with the readme. I input our full finished code, y rough outline of the successes, struggles and personal reflection 

"help me write out a read me"
Claude Sonnet 4.5
