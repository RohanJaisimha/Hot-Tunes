from constants import LYRICS_FOLDER_NAME
from flask import Flask, render_template
import nltk
nltk.download("wordnet")
from nltk.corpus import wordnet
from typing import List
import os
import random
import re

application = Flask(__name__)


def getRandomLines(filename: str) -> str:
    fin = open(filename, "r")
    lines = [line.strip() for line in fin]
    randomIdx = random.randrange(0, len(lines) - 5)
    return " <br> ".join(lines[randomIdx : randomIdx + 5])

def getSynonymsAndAntonyms(word: str) -> List[str]:
    synonyms = []
    antonyms = []

    for syn in wordnet.synsets(word):
        for lem in syn.lemmas():
            synonyms.append(lem.name())
            if lem.antonyms():
                antonyms.append(lem.antonyms()[0].name())

    return synonyms + antonyms


def getDecoys(word1: str, word2: str) -> List[List[str]]:
    decoysForWord1 = getSynonymsAndAntonyms(word1) 
    decoysForWord2 = getSynonymsAndAntonyms(word2) 

    decoysForWord1 = list(set(decoysForWord1))
    decoysForWord2 = list(set(decoysForWord2))

    return list(zip(random.sample(decoysForWord1, 2), random.sample(decoysForWord2, 2)))


def createQuestion() -> List[str]:
    lyricsFiles = os.listdir(LYRICS_FOLDER_NAME)
    randomLyricsFile = random.choice(lyricsFiles)
    randomLyricsFileWithPath = os.path.join(LYRICS_FOLDER_NAME, randomLyricsFile)
    randomLines = getRandomLines(randomLyricsFileWithPath)
    wordsInRandomLines = randomLines.strip().split()
    possibleCandidatesToRemove = list(
        set(filter(lambda word: len(word) > 4, wordsInRandomLines))
    )
    idxAnswer1 = random.randrange(0, len(possibleCandidatesToRemove) - 1)
    idxAnswer2 = random.randrange(idxAnswer1 + 1, len(possibleCandidatesToRemove))
    answer = list(map(possibleCandidatesToRemove.__getitem__, [idxAnswer1, idxAnswer2]))

    randomLines = randomLines.replace(answer[0], "______", 1).replace(
        answer[1], "______", 1
    )

    answer = list(map(lambda word: re.sub(r"[^A-Za-z0-9]", "", word), answer))
    decoy1, decoy2 = getDecoys(answer[0], answer[1])

    answer = f"{answer[0]}, {answer[1]}".lower()
    decoy1 = f"{decoy1[0]}, {decoy1[1]}".lower()
    decoy2 = f"{decoy2[0]}, {decoy2[1]}".lower()

    return answer, randomLines, decoy1, decoy2


@application.route("/")
def main():
    answer, question, decoy1, decoy2 = "", "", "", ""

    while not answer:
        try:
            answer, question, decoy1, decoy2 = createQuestion()
        except:
            pass

    return render_template(
        "main.html",
        answer=answer,
        question=question,
        decoy1=decoy1,
        decoy2=decoy2,
    )


if __name__ == "__main__":
    application.run(debug=True, port=5000, host="0.0.0.0")
