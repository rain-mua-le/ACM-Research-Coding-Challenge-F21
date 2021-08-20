from typing import Dict, List
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn

nltk.download("averaged_perceptron_tagger")
nltk.download("wordnet")
nltk.download("sentiwordnet")

#This class stores a token's word, part-of-speech, and whether or not it has been negated
class Token:
    def __init__(self, word: str, pos: str, is_negated: bool) -> None:
        self.word = word
        self.pos = pos
        self.is_negated = is_negated
    def __str__(self) -> str:
        return "(Word: " + self.word + ", Part-of-speech: " + self.pos + ", Negated?: " + str(self.is_negated) + ")"
    def __hash__(self) -> int:
        return hash((self.word, self.pos, self.is_negated))
    def __eq__(self, o: object) -> bool:
        return (self.word, self.pos, self.is_negated) == (o.word, o.pos, o.is_negated)

#This class stores a token's positive score, negative score, and objective score
class Scores:
    def __init__(self, positive: float, negative: float, objective: float) -> None:
        self.positive = positive
        self.negative = negative
        self.objective = objective
    def __str__(self) -> str:
        return "(Positive Score: " + str(self.positive) + ", Negative Score: " + str(self.negative) + ", Objective Score: " + str(self.objective) + ")"

#Aliases
Bag = Dict[Token, int]
TokenScores = Dict[Token, Scores]

def parse(filename: str, stop_words_file: str) -> str:
    f = open(filename, "r")
    raw_text: str = f.read()
    f.close()
    #Make it lowercase and remove newlines, extra spaces, and punctuations
    s:str = raw_text.strip().lower().replace("\n", " ").replace("  ", " ").replace("\'", "").replace("\"", "").replace("`", "").replace(".", "").replace("?", "").replace("!", "").replace(";", "").replace(",", "").replace("\n\n", " ")
    #Remove stop words
    stop = [str(s) for s in open(stop_words_file).read().strip().split("\n")]
    res = [w for w in s.split(" ") if w not in stop]
    dummy = " ".join(res)
    return dummy

def bag_of_words(block: str) -> Bag:
    negate: List[str] = ["not", "no", "nor"]
    bag: Dict = {}
    #Split block of text into word tokens
    temp = block.strip().split(" ")
    #Tag each word with its part-of-speech
    pos = nltk.pos_tag(temp)
    for i in range(0, len(temp)):
        dummy: str = temp[i]
        #If word is a negate word, skip it 
        if dummy in negate:
            continue
        b: bool = False
        #If negate word comes before, make negate property for this word true
        if i > 0 and temp[i - 1] in negate:
            b = True
        token = Token(dummy, pos[i][1], b)
        if token in bag:
            bag[token] += 1
        else:
            bag[token] = 1
    return bag

def scoring(bags: Bag) -> TokenScores:
    d: Dict = {}
    for k, v in bags.items():
        tag: str = ""
        s = None
        scores = None
        #Give different tags for each corresponding part-of-speech so that it will work with sentiwordnet
        if k.pos.startswith("J"):
            tag = "a"
        elif k.pos.startswith("N"):
            tag = "n"
        elif k.pos.startswith("R"):
            tag = "r"
        elif k.pos.startswith("V"):
            tag = "v"
        else:
            continue
        #Get synset of word
        synsets = wn.synsets(k.word, pos=tag)
        if not synsets:
            continue
        else:
            s = synsets[0]
        #Get scores and multiply by frequency
        ss = swn.senti_synset(s.name())
        p = ss.pos_score() * v
        n = ss.neg_score() * v
        o = ss.obj_score() * v
        if (k.is_negated):
            scores = Scores(n, p, o)
        else:
            scores = Scores(p, n, o)
        d[k] = scores
    return d

def results(token_scores: TokenScores, bags: Bag) -> str:
    result: str = ""
    pos_neg_score = 0
    obj_score = 0
    num_of_tokens = 0
    for v in bags.values():
        num_of_tokens += v
    for v in token_scores.values():
        pos_neg_score += v.positive - v.negative
        obj_score += v.objective
    pos_neg_score /= num_of_tokens
    obj_score /= num_of_tokens
    if pos_neg_score < -0.05:
        result += "The block of text is negative with a score of " + str(pos_neg_score) + "\n"
    elif pos_neg_score > 0.05:
        result += "The block of text is positive with a score of " + str(pos_neg_score) + "\n"
    else:
        result += "The block of text is neutral with a score of " + str(pos_neg_score) + "\n"
    if obj_score < 0.45:
        result += "The block of text is subjective with a score of " + str(obj_score) + "\n"
    elif obj_score > 0.55:
        result += "The block of text is objective with a score of " + str(obj_score) + "\n"
    else:
        result += "The block of text is neither objective nor subjective with a score of " + str(obj_score)
    return result

if __name__ == "__main__":
    block = parse("input.txt", "stop_words.txt")
    file_blocks = open("Blocks.txt", "w")
    file_blocks.write(block + "\n")
    file_blocks.close()
    bag = bag_of_words(block)
    file_bags = open("Bags.txt", "w")
    for k, v in bag.items():
        file_bags.write(str(k) + "- " + str(v) + "\n")
    file_bags.close()
    token_scores = scoring(bag)
    file_token_scores = open("TokenScores.txt", "w")
    for k, v in token_scores.items():
        file_token_scores.write(str(k) + "- " + str(v) + "\n")
    file_token_scores.close()
    result = results(token_scores, bag)
    file_results = open("Results.txt", "w")
    file_results.write(result)
    file_results.close()