from constants import LYRICS_FOLDER_NAME
import os
import re


def main():
    lyricsFiles = os.listdir(LYRICS_FOLDER_NAME)
    lyricsFilesWithFullPath = map(
        lambda lyricsFile: os.path.join(LYRICS_FOLDER_NAME, lyricsFile), lyricsFiles
    )
    for lyricsFile in lyricsFilesWithFullPath:
        fin = open(lyricsFile, "r")
        lyrics = fin.read().strip()
        fin.close()

        lyrics = re.sub(r"\[[^\[\]]*\]", "", lyrics)
        lyrics = re.sub(r"[\n]+", "\n", lyrics)
        lyrics = lyrics.strip()

        fout = open(lyricsFile, "w")
        fout.write(lyrics)
        fout.close()


if __name__ == "__main__":
    main()
