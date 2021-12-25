# music_catalog
Populates a SQLite database with information parsed from audio files/tags for easier music library management. Supports conditional CSV exports, file renaming, and directory renaming. 

Currently stores the following data:

- `Artist`, `Album Artist`, `Year`, `Album`, `Track Number`, `Song Title`, `Extension`, `Bitrate`, `Sample Frequency`, `Channels`, `Genre`, `Duration`, `File Size`, `Full File Path`, `Directory`, `Insert Timestamp`, `BLAKE2B Hash`


## Setup 🔧
clone the repo and change to directory:
~~~
git clone https://github.com/dch42/music_catalog.git && cd music_catalog
~~~

Running `make` will install dependencies and add executable permissions to the script.

~~~
make
~~~

## Usage

- The script requires a path to audio files to be passed with `-p`. 
- Invoking without `-a`, `-r`, or `-e` will launch an interactive menu instead.

To **add** music from **path** to database:
~~~
./music_catalog.py -a -p ~/path/to/music
~~~

### Options
- `-p, --path PATH` *(REQUIRED)*
    - path to audio files
- `-a, --add`
    - scan and add file info to database
- `-r, --rename`
    - rename files and folders using tag data
- `-h, --help`
    - show this option list and exit




### Menu
Main menu interface options are:
~~~
- (a)dd:                Scan for audio files and add to database
- (d)ir rename: 	Rename dirs based on audio file tags
- (f)ile rename: 	Rename files based on audio file tags
- (e)xport: 	        Conditionally export database to csv
~~~
### CSV Export
Currently supports four export formats:
~~~
- (f)ull: 	Export all music info to csv
- (a)lbums: 	Export album info to csv
- (b)itrate: 	Export conditionally by bitrate
- (l)ength: 	Export conditionally by song duration
- (m)issing: 	Export files with missing tag data
~~~

Bitrate and length exports are determined using operators: `=, <, >, <=, >=, !=`

## Directory Rename Output
⚠️ Warning: Not extensively tested. Use at your own risk.

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

## Acknowledgements

Makes use of the wonderful [tinytag](https://github.com/devsnd/tinytag) and [🐼](https://github.com/pandas-dev/pandas) libraries.
