from typing import Dict, List
import nltk

Blocks = List[str]
Bags = List[Dict[str, int]]

def parse(filename: str) -> Blocks:
    f = open(filename, "r")
    raw_text: str = f.read()
    l: List[str] = [str(s.strip().lower().replace("\n", " ").replace("  ", " ").replace(".", "").replace("?", "").replace("!", "").replace(",", "").replace(";", "").replace("\"", "").replace("`", "").replace("\'", "")) for s in raw_text.strip().split("\n\n")]
    return l

def bag_of_bigrams(block: Blocks) -> Bags:
    l: List = []
    for s in block:
        bag: Dict = {}
        temp = s.strip().split(" ")
        for i in range(0, len(temp) - 1):
            dummy: str = temp[i] + " " + temp[i + 1]
            if dummy in bag:
                bag[dummy] += 1
            else:
                bag[dummy] = 1
        l.append(bag)
    return l

if __name__ == "__main__":
    blocks = parse("input.txt")
    bags = bag_of_bigrams(blocks)
    print(bags)