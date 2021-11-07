# music-catalog
Populates a SQLite database with information parsed from audio files/tags for easier music library management. Supports conditional CSV exports, file renaming, and directory renaming. Makes use of the [tinytag](https://github.com/devsnd/tinytag) and [pandas](https://github.com/pandas-dev/pandas) libraries.

Currently stores the following data:

- Artist
- Album Artist
- Year
- Album
- Track Number
- Song Title
- Extension
- Bitrate
- Sample Frequency
- Channels
- Genre
- Duration (seconds)
- File Size
- Full File Path
- Directory
- Insert Timestamp
- BLAKE2B Hash

## Usage
~~~
python3 music-catalog.py ~/path_to_music
~~~
To view this README invoke with `--help`

Main interface options are:
~~~
- (a)dd: 		Scan for audio files and add to database
- (d)ir rename: 	Rename dirs based on audio file tags
- (f)ile rename: 	Rename files based on audio file tags
- (e)xport: 	    Conditionally export database to csv
~~~
## CSV Export
Currently supports four export formats:
~~~
- (f)ull: 	   Export all music info to csv
- (a)lbums: 	Export album info to csv
- (b)itrate: 	Export conditionally by bitrate
- (l)ength: 	Export conditionally by song duration
- (m)issing: 	Export files with missing tag data
~~~

Bitrate exports are determined using operators: `=, <, >, <=, >=, !=`

## Directory Rename Output

Currently renames directories formatted as such:
~~~
%Artist - %Year - %Album (%Extension, %Bitrate)
~~~

### Special Handling:

- Dirs are renamed using tag data parsed from the first audio file found in said directory. 
- If the album artist is "VA", "Various", "Various Artists", `%Artist` will be set to "Various", ignoring track artist tags.
- MP3, M4A, AAC files include CBR/VBR designation in `%Bitrate`.

## File Rename Output

Currently renames files:
~~~
%Track - %Artist - %Title %Bitrate.%Extension
~~~

### Special Handling:

- Zero padding for tracks 1-9

## Storage

The database resides at `data/music_library.db`.

Timestamped CSV exports are stored in `data/csv_exports`

## To-Do
- Blob image data
- Tagging functionality w/Discogs API
- Pad zero handling for albums with track total > 100
