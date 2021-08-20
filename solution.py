from typing import Dict, List
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn

nltk.download("averaged_perceptron_tagger")
nltk.download("wordnet")
nltk.download("sentiwordnet")

class Token:
    def __init__(self, word: str, pos: str, is_negated: bool) -> None:
        self.word = word
        self.pos = pos
        self.is_negated = is_negated
    def __str__(self) -> str:
        return "Word: " + self.word + ", Part-of-speech: " + self.pos + ", Negated?: " + str(self.is_negated)
    def __hash__(self) -> int:
        return hash((self.word, self.pos, self.is_negated))
    def __eq__(self, o: object) -> bool:
        return (self.word, self.pos, self.is_negated) == (o.word, o.pos, o.is_negated)

class Scores:
    def __init__(self, positive: float, negative: float, objective: float) -> None:
        self.positive = positive
        self.negative = negative
        self.objective = objective
    def __str__(self) -> str:
        return "Positive Score: " + str(self.positive) + ", Negative Score: " + str(self.negative) + ", Objective Score: " + str(self.objective)

Blocks = List[str]
Bags = List[Dict[Token, int]]
TokenScores = List[Dict[Token, Scores]]

def parse(filename: str, stop_words_file: str) -> Blocks:
    f = open(filename, "r")
    raw_text: str = f.read()
    #Make it lowercase and remove newlines, extra spaces, and punctuations and parse text into blocks
    l: List[str] = [str(s.strip().lower().replace("\n", " ").replace("  ", " ").replace("\'", "").replace("\"", "").replace("`", "").replace(".", "").replace("?", "").replace("!", "").replace(";", "").replace(",", "")) for s in raw_text.strip().split("\n\n")]
    #Remove stop words from blocks
    stop = [str(s) for s in open(stop_words_file).read().strip().split("\n")]
    li: list = []
    for s in l:
        res = [w for w in s.split(" ") if w not in stop]
        dummy = " ".join(res)
        li.append(dummy)
    return li

def bag_of_words(block: Blocks) -> Bags:
    l: List = []
    negate: List = ["not, no", "nor"]
    for s in block:
        bag: Dict = {}
        temp = s.strip().split(" ")
        pos = nltk.pos_tag(temp)
        for i in range(0, len(temp)):
            dummy: str = temp[i]
            b: bool = False
            if i > 0 and temp[i - 1] in negate:
                b = True
            token = Token(dummy, pos[i][1], b)
            if token in bag:
                bag[token] += 1
            else:
                bag[token] = 1
        l.append(bag)
    return l

def scoring(bags: Bags) -> TokenScores:
    l: List = []
    for blocks in bags:
        d: Dict = {}
        for k, v in blocks.items():
            tag: str = ""
            s = None
            scores = None
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
            synsets = wn.synsets(k.word, pos=tag)
            if not synsets:
                continue
            else:
                s = synsets[0]
            ss = swn.senti_synset(s.name())
            p = ss.pos_score() * v
            n = ss.neg_score() * v
            o = ss.obj_score() * v
            if (k.is_negated):
                scores = Scores(n, p, o)
            else:
                scores = Scores(p, n, o)
            d[k] = scores
        l.append(d)
    return l

def results(token_scores: TokenScores) -> None:
    i = 1
    for blocks in token_scores:
        pos_neg_score = 0
        obj_score = 0
        for v in blocks.values():
            pos_neg_score += v.positive - v.negative
            obj_score += v.objective
        pos_neg_score /= len(blocks)
        obj_score /= len(blocks)
        if pos_neg_score < -0.05:
            print("Block " + str(i) + " is negative with a score of " + str(pos_neg_score))
        elif pos_neg_score > 0.05:
            print("Block " + str(i) + " is positive with a score of " + str(pos_neg_score))
        else:
            print("Block " + str(i) + " is neutral with a score of " + str(pos_neg_score))
        if obj_score < 0.45:
            print("Block " + str(i) + " is objective with a score of " + str(obj_score))
        elif obj_score > 0.55:
            print("Block " + str(i) + " is subjective with a score of " + str(obj_score))
        else:
            print("Block " + str(i) + " is neither objective nor subjective with a score of " + str(obj_score))
        i += 1

if __name__ == "__main__":
    blocks = parse("input.txt", "stop_words.txt")
    bags = bag_of_words(blocks)
    token_scores = scoring(bags)
    results(token_scores)