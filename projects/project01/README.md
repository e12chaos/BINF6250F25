# Project 01: Functional file parsing
Nikaela Aitken and Brooks Groharing

# Introduction
In this first assignment of the course, we implemented a program that can parse VCF (Variant Call Format) files. Specifically we load a .vcf data file taken from ClinVar, and crawl through its lines (without loading the full file in memory), and extracting all diseases associated with rare variants. These are combined to create a dictionary of observed diseases, and the number of variants associated with them in the file.

# Pseudocode
```
def parse_line(line):
	if line starts with #:
		return empty list

	fields = split line by tabs
	info_field = fields[7]
	info_pairs = split info_field by ;
	
	info_dict = new dictionary
	for pair in info_pairs:
	    extract value
	    extract key
	    info_dict[key] = value		
	
	filtered_diseases = new list
	if info_dict[AF_EXAC] < threshold:
		diseases = split info_dict[clndn] by |
		for disease in diseases:
      		if valid disease:
		        add to filtered_diseases
		return filtered_diseases
	else:
		return empty list

def read_file(file):
	disease_counts = new dict

	for line in file:
		diseases = parse_line(line)
		for disease in diseases:
			increment disease_counts[disease] by 1
```

# Successes
We were successful in implementing the code as described. The opportunity to practice string parsing in Python--an important skill for any kind of data scientist--was definitely a success.


# Struggles

The version control side of the project was initially a bit of a struggle. We actually initially worked on our code entirely on our local machines, and only uploaded the (feature complete) project to GitHub later.

# Personal Reflections
## Nikaela (Group Leader)

In this project, I was able to practice and remember some of the basics of Python, especially how to work with files, conditionals, and functions. I also gained experience incorporating Python into an R Markdown document, which was something I had never done before. Another important skill was carrying over ideas from past classes—both in terms of coding strategies and how to structure an analysis. I realized and relied heavily on clear comments in some of my past assignements: when I wasn’t sure how I had solved something before, I could look back at old assignments and my own notes to quickly remind myself of the reasoning and decisions I had made.

## Brooks (Contributor)

This project pulled in several skills covered in BINF6200, especially related to pythonic methods of file handling and string operations. Personally, my Python skills were pretty rusty--my Spring coursework most involved running tools on the command line, not writing programs--and I was glad for the refresher.

Neither of us had much experience using GitHub for collaborative projects, and this aspect of the assignment proved challenging. It was (will continue to be) a learning process--but I was excited to figure out, late in the process, how to sync/work on the project directly from OOD's RSTudio.

# Generative AI Appendix
Description of which generative AI was used and its version:

Claude Sonnet 4

The entire prompt that was used to generate the content. 
"Fix my code (entire ddef check_file_structure(filename) code chunk)"

An explanation of how it was used (e.g., to generate ideas).

Code debugging and syntax correction: When I encountered Python syntax errors (like missing quotes, indentation issues, and import statement problems), Claude helped identify and fix these issues.

A justification for why generative AI was used.

Because I was angry I couldnt get my chunk to run and knew it was something like  missing quotations so I used claude to help me fix it.
