#!/usr/bin/env python3
"""Parse audio file data and store in db"""

import os
import sys
import argparse
import pathlib
import hashlib
import sqlite3
from datetime import datetime
from tqdm import tqdm
import pyfiglet
from tinytag import TinyTag
import rename as rn
import export as ex

date = datetime.now().date()
time = datetime.now().time().strftime('%H-%M-%S')


hasher = hashlib.blake2b()
extensions = [".mp3", ".m4a", ".flac", ".ogg", ".opus", ".wma", ".wav"]

db = sqlite3.connect("./data/music_library.db")
cursor = db.cursor()

parser = argparse.ArgumentParser(
    description="Parse audio file data and store in db")
parser.add_argument(
    "-p", "--path", type=str, help='path to audio files')
parser.add_argument(
    "-a", "--add", help='scan and add file info to database', action="store_true")
args = parser.parse_args()

path = args.path if args.path else '.'


def menu_loop(menu):
    """Persistant modular menu"""
    choice = None
    while choice != 'q':
        os.system("clear")
        pyfiglet.print_figlet("Music Catalog")
        print(f"Music path: '{path}'\n")
        print("\n\033[1mMENU.........................................\033[0m\n")
        for key, value in menu.items():
            print(
                f'\033[96m{value[2]}:\033[0m \033[95m{value[0].__doc__}\033[0m')
        print("\033[96m(q)uit/back\033[0m")
        choice = input('\nAction: ').lower().strip()
        if choice in menu:
            menu[choice][1]()


def iter_music():
    """Scan for audio files and add to database"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS music_info(
        Album_Artist TEXT,
        Artist TEXT,
        Year TEXT,
        Album TEXT,
        Track_Number INTEGER,
        Title TEXT,
        Extension TEXT,
        Bitrate INTEGER,
        Sample_Frequency INTEGER,
        Channels TEXT,
        Genre TEXT,
        Duration INTEGER,
        Filesize TEXT,
        Path TEXT,
        Directory TEXT,
        Last_Updated TEXT,
        Hash TEXT PRIMARY KEY)
        """)
    for root, dirs, files in os.walk(path, topdown=False):
        for filename in tqdm(files, colour='green', desc=f'{os.path.basename(root)}...'):
            if filename.endswith(tuple(extensions)):
                audio_file = os.path.join(root, filename)
                cursor.execute(
                    "SELECT * FROM music_info WHERE Path=?", (audio_file,))
                exists = cursor.fetchone()
                cursor.execute(
                    "SELECT Last_Updated FROM music_info WHERE Path=?", (audio_file,))
                last_ran = cursor.fetchone()
                if not last_ran:
                    last_ran = (0,)
                last_file_mod = os.stat(f'{audio_file}').st_mtime
                last_file_mod = datetime.fromtimestamp(last_file_mod)
                if not exists and str(last_ran[0]) < str(last_file_mod):
                    file_extension = pathlib.Path(audio_file).suffix
                    tqdm.write(
                        f"\n==> \033[1mHashing\033[0m \033[4m{filename}\033[0m...")
                    with open(audio_file, 'rb') as file_to_hash:
                        buf = file_to_hash.read()
                        hasher.update(buf)
                        blake2b_hash = str(hasher.hexdigest())
                    tqdm.write(
                        "==> \033[1mParsing\033[0m tag data...")
                    try:
                        audio_obj = TinyTag.get(f'{audio_file}')
                    except Exception as error:
                        tqdm.write(f"\033[91m Parse failed: {error}\033[0m")
                    try:
                        add_to_db(audio_file, audio_obj,
                                  blake2b_hash, root, file_extension)
                    except Exception as error:
                        tqdm.write(f"\033[91m Insert failed: {error}\033[0m")
                else:
                    tqdm.write(
                        f"\033[92m{filename}\033[0m already exists in db, skipping file...")
    input("\nDone! Hit 'Enter' to return...: ")


def add_to_db(audio_file, audio_obj, blake2b_hash, root, file_extension):
    """Insert parsed info into database"""
    last_updated = str(datetime.now())

    song_info = [(
        audio_obj.albumartist,
        audio_obj.artist,
        audio_obj.year,
        audio_obj.album,
        audio_obj.track,
        audio_obj.title,
        file_extension,
        audio_obj.bitrate,
        audio_obj.samplerate,
        audio_obj.channels,
        audio_obj.genre,
        audio_obj.duration,
        audio_obj.filesize,
        str(audio_file),
        str(root),
        last_updated,
        blake2b_hash
    )]

    cursor.executemany(
        "INSERT INTO music_info VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", song_info)
    db.commit()

    tqdm.write(
        f"\033[1m\033[92m[SUCCESS]\033[0m Info for \033[1m\033[95m{str(audio_obj.artist)} - {str(audio_obj.title)}\033[0m\033[0m inserted to the table!\033[0m")


def export_to_csv():
    """Conditionally export database to csv"""
    menu_loop(export_menu)


main_menu = {
    "a": [iter_music, lambda: iter_music(), "(a)dd"],
    "d": [rn.rename_dir, lambda: rn.rename_dir(path), "(d)ir rename"],
    "f": [rn.rename_files, lambda: rn.rename_files(path), "(f)ile rename"],
    "e": [export_to_csv, lambda: export_to_csv(db), "(e)xport"]
}
export_menu = {
    "f": [ex.export_all, lambda: ex.export_all(db), "(f)ull"],
    "a": [ex.export_albums, lambda: ex.export_albums(db), "(a)lbums"],
    "b": [ex.export_by_bitrate, lambda: ex.export_by_bitrate(db), "(b)itrate"],
    "l": [ex.export_by_length, lambda: ex.export_by_length(db), "(l)ength"],
    "m": [ex.export_missing, lambda: ex.export_missing(db), "(m)issing"]
}

########################################################

if __name__ == '__main__':
    if args.add:
        iter_music()
    else:
        menu_loop(main_menu)
