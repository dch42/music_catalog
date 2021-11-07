import os
import sys
import pathlib
import pyfiglet
from tinytag import TinyTag

# dirty but can't read header afaict so...
cbr = [32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320]
various = ["VA", "Various", "Various Artists"]
extensions = [".mp3", ".aac", ".m4a", ".mp4",
              ".flac", ".ogg", ".opus", ".wma", ".wav"]

path = sys.argv[1]


def rename_dir(path):
    """Rename dirs based on audio file tags"""
    print("\nWill run directory rename script in %s" % path)
    ok = input("\nHit 'Enter' to run, 'CTRL+C' to quit: ")
    for root, dirs, files in os.walk(path, topdown=False):
        for filename in files:
            if filename.endswith(tuple(extensions)):
                audio_file = os.path.join(root, filename)
                file_extension = pathlib.Path(audio_file).suffix[1:].upper()
                print(
                    "\033[94m==>\033[0m \033[1mParsing\033[0m tag data...")
                audio_obj = TinyTag.get("%s" % audio_file)
                if filename.endswith(tuple(extensions[0:3])) and audio_obj.bitrate not in cbr:
                    bitrate = "%s VBR" % int(audio_obj.bitrate)
                elif audio_obj.bitrate in cbr:
                    bitrate = "%s CBR" % int(audio_obj.bitrate)
                else:
                    bitrate = int(audio_obj.bitrate)
                if audio_obj.albumartist in various:
                    artist = "Various"
                else:
                    artist = audio_obj.artist
                new_dir_name = "%s - %s - %s (%s, %s)" % (artist, str(
                    audio_obj.year), audio_obj.album, file_extension, bitrate)
                new_dir_path = os.path.join(path, new_dir_name)
                try:
                    os.rename(root, new_dir_path)
                    print(
                        "✨ \033[1mSuccess!\033[0m Renamed %s... \n\t\033[93m\x1b[5m>>\033[0m\033[0m \033[95m\033[1m%s\033[0m\033[0m\n" % (root, new_dir_name))
                except Exception as e:
                    print("\033[91m Rename failed: ", e, "\033[0m\n")
                break
    done = input("\nDone! Hit 'Enter' to return...: ")


def rename_files(path):
    """Rename files based on audio file tags"""
    print("\nWill run file rename script in %s" % path)
    ok = input("\nHit 'Enter' to run, 'CTRL+C' to quit: ")
    for root, dirs, files, in os.walk(path, topdown=False):
        for filename in files:
            if filename.endswith(tuple(extensions)):
                audio_file = os.path.join(root, filename)
                file_extension = pathlib.Path(audio_file).suffix
                print(
                    "\033[94m==>\033[0m \033[1mParsing\033[0m tag data...")
                audio_obj = TinyTag.get("%s" % audio_file)
                if audio_obj.track[0].isdigit() and audio_obj.track[0] != "0":
                    if int(audio_obj.track) in range(0, 10):
                        track_num = "0%s" % audio_obj.track
                else:
                    track_num = audio_obj.track
                new_file_name = "%s - %s - %s %s%s" % (
                    track_num, audio_obj.artist, audio_obj.title, audio_obj.bitrate, file_extension)
                new_file_path = os.path.join(root, new_file_name)
                try:
                    os.rename(audio_file, new_file_path)
                    print(
                        "✨ \033[1mSuccess!\033[0m Renamed %s... \n\t\033[93m\x1b[5m>>\033[0m\033[0m \033[95m\033[1m%s\033[0m\033[0m\n" % (audio_file, new_file_path))
                except Exception as e:
                    print("\033[91m Rename failed: ", e, "\033[0m\n")
        done = input("\nDone! Hit 'Enter' to rename next album...: ")
    done = input("\nDone! Hit 'Enter' to return...: ")


if __name__ == "__main__":
    pyfiglet.print_figlet("RenameDir")
    rename_dir(path)
