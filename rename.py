"""Rename files and dirs according to parsed tag data"""

import os
from pathlib import Path
import pyfiglet
from tinytag import TinyTag
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
from mutagen.flac import FLAC

# dirty but can't read header afaict so...
cbr = [32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320]
various = ["VA", "Various", "Various Artists"]
extensions = [".mp3", ".aac", ".m4a",
              ".flac", ".ogg", ".opus", ".wma", ".wav"]


def update_tags(file_extension, file, key, tag_value):
    if file_extension == 'MP3':
        mutagen_obj = MP3(f'{file}', ID3=EasyID3)
    elif file_extension == 'FLAC':
        mutagen_obj = FLAC(f'{file}')
    mutagen_obj[f'{key}'] = f'{tag_value}'
    mutagen_obj.save()


def cleanse_chars(value):
    value = value.replace('/', '')
    value = value.replace(':', '-')
    value = value.replace('?', '')
    return value


def check_empties(audio_obj, filename):
    """Get user input for critical empty tags"""
    check_empty_tags = ['artist', 'year', 'album']
    new_tags = []
    for file in os.listdir(filename.parents[0]):
        if file.endswith((tuple(extensions))):
            file_extension = Path(file).suffix[1:].upper()
            f = os.path.join(filename.parents[0], file)
            for tag in check_empty_tags:
                if getattr(audio_obj, tag) in (None, ''):
                    new_tag_val = input(
                        f'`{tag.capitalize()}` is blank, enter a value: ')
                    if tag == 'year':  # purge after switching fully to mutagen
                        tag = 'date'
                    update_tags(file_extension, f, tag, new_tag_val)
                    new_tag_val = cleanse_chars(new_tag_val)
                else:
                    new_tag_val = getattr(audio_obj, tag)
                    new_tag_val = cleanse_chars(new_tag_val)
                new_tags.append(new_tag_val)
            return new_tags


def get_bitrate(filename, audio_obj):
    """Get bitrate for albums"""
    if filename.suffix in tuple(extensions[0:3]) and audio_obj.bitrate not in cbr:
        bitrate = f"{int(audio_obj.bitrate)} VBR"
    elif audio_obj.bitrate in cbr:
        bitrate = f"{int(audio_obj.bitrate)} CBR"
    else:
        try:
            bitrate = int(audio_obj.bitrate)
        except Exception as error:
            print(f"\033[91m Bitrate Error: {error}\033[0m\n")
    return bitrate


def rename_dir(path):
    """Rename dirs based on audio file tags"""
    print(f"\nWill run directory rename script in {path}")
    input("\nHit 'Enter' to run, 'CTRL+C' to quit: ")
    for root, dirs, files in os.walk(path, topdown=False):
        music_path = Path(root)
        for filename in music_path.rglob('*'):
            if filename.suffix in tuple(extensions):
                file_extension = filename.suffix[1:].upper()
                print(
                    f"\033[94m==>\033[0m \033[1mParsing\033[0m tag data for {filename.parts[-2]}...")
                try:
                    audio_obj = TinyTag.get(f"{filename}")
                except Exception as error:
                    print(f"\033[91m Parsing failed: {error}\033[0m\n")
                bitrate = get_bitrate(filename, audio_obj)
                artist, year, album = check_empties(audio_obj, filename)
                if audio_obj.albumartist in various:
                    artist = "Various"
                new_dir_name = f"{artist} - {year} - {album} ({file_extension}, {bitrate})"
                new_dir_path = filename.parents[1].joinpath(new_dir_name)
                ok = input(
                    f"\nRename `\033[93m{filename.parts[-2]}\033[0m` \n\t >> `\033[92m{new_dir_name}\033[0m`? (y/N):")
                if ok.lower() == 'y' or ok.lower() == 'yes':
                    try:
                        os.rename(filename.parents[0], new_dir_path)
                        print(
                            f"\033[1m\033[92m[SUCCESS]\033[0m Renamed {filename.parts[-2]}... \n\t\033[93m\x1b[5m>>\033[0m\033[0m \033[95m\033[1m{new_dir_name}\033[0m\033[0m\n")
                    except Exception as error:
                        print(f"\033[91m Rename failed: {error}\033[0m\n")
                else:
                    print(f'Skipping {filename.parts[-2]}...\n')
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
