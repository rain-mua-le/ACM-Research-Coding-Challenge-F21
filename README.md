# ACM Research Coding Challenge Fall 2021

## Language, Libraries, and APIs
This coding challenge uses the Python language, the Natural Language Toolkit library, and the typing library.
## Outside Resources Used
I used the [typing library documentation](https://docs.python.org/3/library/typing.html), the [NLTK library documentation for wordnet](https://www.nltk.org/api/nltk.corpus.reader.html#module-nltk.corpus.reader.wordnet), the [NLTK library documentation for sentiwordnet](https://www.nltk.org/api/nltk.corpus.reader.html#module-nltk.corpus.reader.sentiwordnet), this [StackOverflow page about part-of-speech tagging for sentiwordnet](https://stackoverflow.com/questions/10223314/using-sentiwordnet-3-0), and [this free e-book on the NLTK library](https://www.nltk.org/book/).
## Approach
For my approach to this problem, I will be using rule-based sentiment analysis.
1. The file is parsed into two blocks of text using the fact that the blocks of text in the input file are separated by a blank line.
2. The blocks of text are preprocessed so that it is all lowercase and all punctuation and all stop words are deleted.
3. A Token class is created that stores the word token, its part of speech, and whether or not it has been negated.
4. Using the bag-of-words approach, the structure of the sentence is disregarded and each Token is stored with its frequency in a dictionary.
5. To determine if a token is negated, the preceding word is looked at. If it is "not", "no", or "nor", then the token after it is negated.
6. The part-of-speech is also attached to the token a built-in NLTK function.
7. A TokenScore class is created to store the token's positive score, negative score, and objective score.
8. The tokens are then scored using sentiwordnet. If the token is negated, the token's positive and negative score are reversed. The token's scores are also multiplied by its frequency.