# ACM Research Coding Challenge Fall 2021

## Language, Libraries, and APIs
This coding challenge uses the Python language, the Natural Language Toolkit library, and the typing library.

## Outside Resources Used
I used the [typing library documentation](https://docs.python.org/3/library/typing.html), the [NLTK library documentation for wordnet](https://www.nltk.org/api/nltk.corpus.reader.html#module-nltk.corpus.reader.wordnet), the [NLTK library documentation for sentiwordnet](https://www.nltk.org/api/nltk.corpus.reader.html#module-nltk.corpus.reader.sentiwordnet), this [StackOverflow page about part-of-speech tagging for sentiwordnet](https://stackoverflow.com/questions/10223314/using-sentiwordnet-3-0), and [this free e-book on the NLTK library](https://www.nltk.org/book/).

## Approach
For my approach to this problem, I will be using [rule-based sentiment analysis](https://monkeylearn.com/sentiment-analysis/).
1. The file is parsed.
2. The block of text is preprocessed so that it is all lowercase and all punctuation and all stop words are deleted.
3. A Token class is created that stores the word token, its part of speech, and whether or not it has been negated.
4. Using the [bag-of-words approach](https://machinelearningmastery.com/gentle-introduction-bag-words-model/), the structure of the sentence is disregarded and each Token is stored with its frequency in a dictionary.
5. To determine if a token is negated, the preceding word is looked at. If it is "not", "no", or "nor", then the token after it is negated.
6. The part-of-speech is also attached to the token using a built-in NLTK function.
7. A TokenScore class is created to store the token's positive score, negative score, and objective score.
8. The tokens are then scored using sentiwordnet. If the token is negated, the token's positive and negative score are reversed. The token's scores are also multiplied by its frequency.
9. The results are calculated by subtracting the overall negative score from the overall positive score and then divided by the number of tokens. Similarly, the overall objective score is divided by the number of tokens.
10. Finally, the Block, Bag, TokenScores, and results are printed to their respective files.

## Summary of Results
The block of text is positive with a score of 0.0595 and objective with a score of 0.6534.

## Analysis of Results
For the positivity/negativity score, if the score was < -0.05 it has more negative words than positive words. Else if the score was > 0.05, it has more positive words than negative words. Else, there are roughly the same amount of positive and negative words. Since the score obtained was 0.0595 for the positivity/negativity score, there are slightly more positive words than negative words. Thus, it can be concluded that the sentiment of the text is more positive.
For the objectivity score, if the score was < 0.45 it has more subjective words than objective words. Else if the score was > 0.55 it has more objective words than subjective words. Else, there are roughly the same amount of subjective and objective words. Since the objective score was 0.6534 for the text, there are more objective words than subjective words. Thus, it can be concluded that the text is more objective.
The results for the positivity/negativity score made sense to me because the first half seemed more negativity with some negation thrown in the mix while the second half seemed more positive to me. Therefore, it made sense that it is only slightly more positive than negative. On the other hand, the objectivity score surprised me because the text as a whole seemed more subjective since it is a story, but the results tell us that the text has more objective words than subjective words.

## Explanation for Approach
The reason I used the rule-based approach was because there was not enough sufficient training data for the machine learning approach to work. Furthermore, I used the bag-of-words approach to the problem, because maintaining the structure of the sentence would mean more rules must be created to analyze the both the macro-structure and micro-structure of the sentence. this will craete too many rules, which will become unmanageable.

## To Run Solution Program
Run `git clone https://github.com/rain-mua-le/ACM-Research-Coding-Challenge-F21.git` in the terminal, then change directories to the created folder to run these commands:
`
python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python solution.txt
`