"""Rename files and dirs according to parsed tag data"""

import os
import pathlib
import pyfiglet
from tinytag import TinyTag

# dirty but can't read header afaict so...
cbr = [32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320]
various = ["VA", "Various", "Various Artists"]
extensions = [".mp3", ".aac", ".m4a",
              ".flac", ".ogg", ".opus", ".wma", ".wav"]


def check_empties(audio_obj):
    """Get user input for critical empty tags"""
    if audio_obj.artist == '' or audio_obj.artist == 'None':
        artist = input('`Artist` is blank, enter a value: ')
        artist = artist.replace('/', '')
    else:
        artist = audio_obj.artist
        artist = artist.replace('/', '')
    if audio_obj.album == '' or audio_obj.album == 'None':
        album = input('`Album` is blank, enter a value: ')
        album = album.replace('/', '')
    else:
        album = audio_obj.album
        album = album.replace('/', '')
    if str(audio_obj.year) == '' or str(audio_obj.year) == 'None':
        year = input('`Year` is blank, enter a value: ')
    else:
        year = str(audio_obj.year)
    return artist, year, album


def rename_dir(path):
    """Rename dirs based on audio file tags"""
    print(f"\nWill run directory rename script in {path}")
    input("\nHit 'Enter' to run, 'CTRL+C' to quit: ")
    for root, dirs, files in os.walk(path, topdown=False):
        for filename in files:
            if filename.endswith(tuple(extensions)):
                audio_file = os.path.join(root, filename)
                file_extension = pathlib.Path(audio_file).suffix[1:].upper()
                print(
                    f"\033[94m==>\033[0m \033[1mParsing\033[0m tag data for {os.path.basename(root)}...")
                try:
                    audio_obj = TinyTag.get(f"{audio_file}")
                except Exception as error:
                    print(f"\033[91m Parsing failed: {error}\033[0m\n")
                if filename.endswith(tuple(extensions[0:3])) and audio_obj.bitrate not in cbr:
                    bitrate = f"{int(audio_obj.bitrate)} VBR"
                elif audio_obj.bitrate in cbr:
                    bitrate = f"{int(audio_obj.bitrate)} CBR"
                else:
                    try:
                        bitrate = int(audio_obj.bitrate)
                    except Exception as error:
                        print(f"\033[91m Bitrate Error: {error}\033[0m\n")
                artist, year, album = check_empties(audio_obj)
                if audio_obj.albumartist in various:
                    artist = "Various"
                new_dir_name = f"{artist} - {year} - {album} ({file_extension}, {bitrate})"
                new_dir_path = os.path.join(
                    path, root.split('/')[-2], new_dir_name)
                print(f'{new_dir_path=}')
                ok = input(
                    f"\nRename `\033[93m{os.path.basename(root)}\033[0m` \n\t >> `\033[92m{new_dir_name}\033[0m`? (y/N):")
                if ok.lower() == 'y' or ok.lower() == 'yes':
                    try:
                        os.rename(root, new_dir_path)
                        print(
                            f"\033[1m\033[92m[SUCCESS]\033[0m Renamed {root}... \n\t\033[93m\x1b[5m>>\033[0m\033[0m \033[95m\033[1m{new_dir_name}\033[0m\033[0m\n")
                    except Exception as error:
                        print(f"\033[91m Rename failed: {error}\033[0m\n")
                else:
                    print(f'Skipping {os.path.basename(root)}...\n')
                break
    input("\nDone! Hit 'Enter' to return...: ")


def rename_files(path):
    """Rename files based on audio file tags"""
    print(f"\nWill run file rename script in {path}")
    input("\nHit 'Enter' to run, 'CTRL+C' to quit: ")
    for root, dirs, files, in os.walk(path, topdown=False):
        for filename in files:
            if filename.endswith(tuple(extensions)):
                audio_file = os.path.join(root, filename)
                file_extension = pathlib.Path(audio_file).suffix
                print(
                    "\033[94m==>\033[0m \033[1mParsing\033[0m tag data...")
                audio_obj = TinyTag.get(f"{audio_file}")
                if audio_obj.track[0].isdigit() and audio_obj.track[0] != '0':
                    if int(audio_obj.track) in range(0, 10):
                        track_num = f"0{audio_obj.track}"
                else:
                    track_num = audio_obj.track
                if audio_obj.artist == '' or audio_obj.album == '':
                    print(
                        f'\033[91mSkipping {filename}, blank tags...')
                    break
                new_file_name = f"{track_num} - {audio_obj.artist} - {audio_obj.title} {audio_obj.bitrate}{file_extension}"
                new_file_path = os.path.join(root, new_file_name)
                ok = input(
                    f"\nRename `\033[93m{audio_file}\033[0m` \n\t >> `\033[92m{new_file_path}\033[0m`? (y/N):")
                if ok.lower() == 'y' or ok.lower() == 'yes':
                    try:
                        os.rename(audio_file, new_file_path)
                        print(
                            f"\033[1m\033[92m[SUCCESS]\033[0m Renamed {audio_file}... \n\t\033[93m\x1b[5m>>\033[0m\033[0m \033[95m\033[1m{new_file_path}\033[0m\033[0m\n")
                    except Exception as error:
                        print(f"\033[91m Rename failed: {error}\033[0m\n")
        input("\nDone! Hit 'Enter' to rename next album...: ")
    input("\nDone! Hit 'Enter' to return...: ")


if __name__ == "__main__":
    pyfiglet.print_figlet("Renamer")
    rename_dir(path)
    rename_files(path)
