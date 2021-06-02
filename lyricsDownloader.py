from constants import ALBUM_NAME
from constants import ARTIST
from constants import CLIENT_ACCESS_TOKEN
from constants import LYRICS_FOLDER_NAME
from constants import LYRICS_JSON
from constants import TEMPLATE_LYRICS_FILENAME

import json
import lyricsgenius as genius
import os


def main():
    if os.path.exists(LYRICS_JSON):
        os.remove(LYRICS_JSON)

    if not os.path.exists(LYRICS_FOLDER_NAME):
        os.mkdir(LYRICS_FOLDER_NAME)

    api = genius.Genius(CLIENT_ACCESS_TOKEN)
    api.search_album(ALBUM_NAME, ARTIST).save_lyrics()

    fin = open(LYRICS_JSON, "r")
    lyricsData = json.load(fin)
    fin.close()

    for track in lyricsData["tracks"]:
        songName = track["song"]["title_with_featured"]

        lyricsFileName = songName.replace(" ", "_")
        lyricsFileNameWithPath = TEMPLATE_LYRICS_FILENAME.format(lyricsFileName)

        lyrics = track["song"]["lyrics"]
        lyrics = lyrics.strip()

        fout = open(lyricsFileNameWithPath, "w")
        fout.write(lyrics)
        fout.close()

    if os.path.exists(LYRICS_JSON):
        os.remove(LYRICS_JSON)


if __name__ == "__main__":
    main()
