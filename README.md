#Language, Libraries, and APIs
---
This coding challenge uses the Python language, the Natural Language Toolkit library, and the typing library.
#Approach
---
1. The file is parsed into two blocks of text using the fact that the blocks of text in the input file are separated by a blank line.
2. The blocks of text are preprocessed so that it is all lowercase and all punctuation is deleted.
3. Using the bag-of-bigrams approach, create a list of dictionaries for each block that maps each bigram to their frequency.