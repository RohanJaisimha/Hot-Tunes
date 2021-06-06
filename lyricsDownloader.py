from constants import ALBUMS_AND_ARTISTS
from constants import CLIENT_ACCESS_TOKEN
from constants import LYRICS_FOLDER_NAME
from constants import TEMPLATE_LYRICS_FILENAME

import json
import lyricsgenius as genius
import os


def downloadLyrics(album: str, artist: str) -> None:
    api = genius.Genius(CLIENT_ACCESS_TOKEN)
    lyricsData = api.search_album(album, artist).to_dict()

    for track in lyricsData["tracks"]:
        songName = track["song"]["title_with_featured"]

        lyricsFileName = songName.replace(" ", "_")
        lyricsFileNameWithPath = TEMPLATE_LYRICS_FILENAME.format(lyricsFileName)

        lyrics = track["song"]["lyrics"]
        lyrics = lyrics.strip()

        fout = open(lyricsFileNameWithPath, "w")
        fout.write(lyrics)
        fout.close()


def main():
    if not os.path.exists(LYRICS_FOLDER_NAME):
        os.mkdir(LYRICS_FOLDER_NAME)

    for album, artist in ALBUMS_AND_ARTISTS:
        downloadLyrics(album, artist)


if __name__ == "__main__":
    main()
