# Language, Libraries, and APIs
This coding challenge uses the Python language, the Natural Language Toolkit library, and the typing library.
# Approach
For my approach to this problem, I will be using rule-based sentiment analysis.
1. The file is parsed into two blocks of text using the fact that the blocks of text in the input file are separated by a blank line.
2. The blocks of text are preprocessed so that it is all lowercase and all punctuation and all stop words are deleted.
3. A Token class is created that stores the word token, its part of speech, and whether or not it has been negated.
4. Using the bag-of-words approach, the structure of the sentence is disregarded and each Token is stored with its frequency in a dictionary.