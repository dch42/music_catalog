# music-catalog
A simple script to populate a SQLite database with information parsed from mp3 files and their tags for easier searching and CSV export. 

![Scanning dir to db](https://raw.githubusercontent.com/dch42/music-catalog/main/data/screenshots/scan.gif)
![Exporting to CSV](https://raw.githubusercontent.com/dch42/music-catalog/main/data/screenshots/export.gif)

Currently stores the following data:

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

Files are hashed during iteration to avoid duplicate data entries, and the database is checked for existing path entries prior to hashing.

## Usage
~~~
python3 music-catalog.py ~/path_to_music
~~~
To view this README invoke with `--help`

## Storage

The database resides at `data/music_library.db`.

Timestamped CSV exports are stored in `data/csv_exports`

## Features
- Export to CSV

## TODO
- Add timestamp check to guard clause
- Blob image data?
