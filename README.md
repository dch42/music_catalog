# music-catalog
Populates a SQLite database with information parsed from audio files and their tags:

- Artist
- Album Artist
- Year
- Album
- Track Number
- Song Title
- Bitrate
- Sample Frequency
- Mode
- File Path
- BLAKE2B Hash

Files are hashed during iteration to use as PRIMARY KEY to avoid duplicate data entries.

## Usage
~~~
python3 music-catalog.py ~/path_to_music
~~~
For extra info invoke with `--help`

## Features
- Export to CSV
