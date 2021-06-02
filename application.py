from constants import LYRICS_FOLDER_NAME
from flask import Flask, render_template
from PyDictionary import PyDictionary
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


def getSynonyms(word1: str, word2: str) -> List[List[str]]:
    synonymsOfWord1 = PyDictionary().synonym(word1)
    synonymsOfWord2 = PyDictionary().synonym(word2)
    return list(
        zip(random.sample(synonymsOfWord1, 2), random.sample(synonymsOfWord2, 2))
    )


def createQuestion() -> List[str]:
    lyricsFiles = os.listdir(LYRICS_FOLDER_NAME)
    randomLyricsFile = random.choice(lyricsFiles)
    randomLyricsFileWithPath = os.path.join(LYRICS_FOLDER_NAME, randomLyricsFile)
    randomLines = getRandomLines(randomLyricsFileWithPath)
    wordsInRandomLines = randomLines.strip().split()
    possibleCandidatesToRemove = list(
        filter(lambda word: len(word) > 4, wordsInRandomLines)
    )
    answer = random.sample(possibleCandidatesToRemove, 2)
    randomLines = randomLines.replace(answer[0], "______", 1).replace(
        answer[1], "______", 1
    )

    answer = list(map(lambda word: re.sub(r"[^A-Za-z0-9]", "", word), answer))
    decoy1, decoy2 = getSynonyms(answer[0], answer[1])

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
