import eyed3, sys, os, pyfiglet, sqlite3, hashlib
from tinytag import TinyTag
import pandas as pd
from datetime import date, datetime, time

date = datetime.now().date()
time = datetime.now().time().strftime('%H-%M-%S')

path = sys.argv[1]
hasher = hashlib.blake2b()
extensions = [".mp3", ".m4a"]

db = sqlite3.connect("./data/music_library.db")
cursor = db.cursor()

def menu_loop(menu):
    choice = None
    while choice != 'q':
        os.system("clear")
        pyfiglet.print_figlet("Musicatalogue")
        print("Music path: '%s'\n" % path)
        print("\n\033[1mMENU.........................................\033[0m\n")
        i = 1
        for key, value in menu.items():
            if i == 1 and menu == main_menu:
                print('\t\033[96m%s:\033[0m \t\t\033[95m%s\033[0m' % (value[2], value[0].__doc__))
                i += 1
            else:
                print('\t\033[96m%s:\033[0m \t\033[95m%s\033[0m' % (value[2], value[0].__doc__))
        print("\t\033[96m(q)uit/back\033[0m")
        choice = input('\nAction: ').lower().strip()
        if choice in menu:
            menu[choice][1]()

def go_back(question):
    go_back = None
    while go_back != 'y':
        go_back = input(question).lower().strip()

def iter_music(path, db, cursor, hasher):
    """Scan for audio files and add to database"""
    cursor.execute("""CREATE TABLE IF NOT EXISTS music_info(
    Hash TEXT PRIMARY KEY,
    Album_Artist TEXT,
    Artist TEXT, 
    Year TEXT, 
    Album TEXT, 
    Track_Number INTEGER, 
    Title TEXT,
    Bitrate INTEGER, 
    Sample_Frequency INTEGER, 
    Genre TEXT,
    Duration INTEGER,
    Path TEXT)
    """)
    for root, dirs, files in os.walk(path, topdown=False):
        for filename in files:
            if filename.endswith(tuple(extensions)):
                audio_file = os.path.join(root, filename)
                cursor.execute("SELECT * FROM music_info WHERE Path=?", (audio_file,))
                exists = cursor.fetchone()
                if not exists:
                    print("\nHashing  \033[4m%s\033[0m..." % filename)
                    with open(audio_file, 'rb') as file_to_hash:
                        buf = file_to_hash.read()
                        hasher.update(buf)
                        blake2b_hash = str(hasher.hexdigest())
                        print("\033[1m\033[95mBLAKE2B HASH:\033[0m\033[0m", blake2b_hash)
                    print("Parsing tag data from \033[4m%s\033[0m..." % filename)
                    audio_obj = TinyTag.get("%s" % audio_file)
                    try:
                        add_to_db(audio_file, audio_obj, db, cursor, blake2b_hash)
                    except Exception as e: print("\033[91m Insert failed: ", e, "\033[0m")
                else: 
                    print("\033[92m%s\033[0m already exists in db, skipping file..." % filename)
    print("\nDONE!\n")
    go_back('Go back to menu? y/N: ')

def add_to_db(audio_file, audio_obj, db, cursor, blake2b_hash):
    """Insert parsed info into database"""
    song_info = [(
        blake2b_hash,
        audio_obj.albumartist,
        audio_obj.artist,
        audio_obj.year,
        audio_obj.album,
        audio_obj.track,
        audio_obj.title,
        audio_obj.bitrate,
        audio_obj.samplerate,
        audio_obj.genre,
        audio_obj.duration,
        str(audio_file)

    )]

    cursor.executemany("INSERT INTO music_info VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", song_info)
    db.commit()

    print("\033[1m\033[96mSUCCESS:\033[0m Info for \033[1m%s - %s\033[0m inserted to the table!\033[0m" % (str(audio_obj.tag.artist), str(audio_obj.tag.title)))
    
def export_to_csv(db):
    """Conditionally export database to csv"""
    menu_loop(export_menu)

def export_all(db):
    """Export all music info to csv"""
    try:
        music_df = pd.read_sql_query("SELECT * FROM music_info", db)
        music_df.to_csv('data/csv_exports/music_database-%s-%s.csv' % (date, time), index=False)
        print("\nSUCCESS!\nExported all music info to 'data/csv_exports/music_database-%s-%s.csv'" % (date, time))
    except Exception as e: print("\033[91m Export failed: ", e, "\033[0m")
    go_back('\nGo back to menu? y/N: ')

def export_albums(db):
    """Export album info to csv"""
    try:
        music_df = pd.read_sql_query("SELECT Album_Artist, Year, Album FROM music_info", db)
        music_df = music_df.drop_duplicates()
        music_df.to_csv('data/csv_exports/albums_database-%s-%s.csv' % (date, time), index=False)
        print("\nSUCCESS!\nExported album data to 'data/csv_exports/albums_database-%s-%s.csv'" % (date, time))
    except Exception as e: print("\033[91m Export failed: ", e, "\033[0m")
    go_back('\nGo back to menu? y/N: ')

def export_by_bitrate(db):
    """Export conditionally by bitrate"""
    #can't seem to input operator as var, hence case switch :(
    try:
        operator = input("Operator? (=, <, >, <=, >=): ")
        bitrate = input("Bitrate? (128, 192 etc): ")
        if operator == "=":
            music_df = pd.read_sql_query("SELECT * FROM music_info WHERE Bitrate = (?)", db, params=(bitrate,))
        elif operator == "<":
            music_df = pd.read_sql_query("SELECT * FROM music_info WHERE Bitrate < (?)", db, params=(bitrate,))
        elif operator == ">":
            music_df = pd.read_sql_query("SELECT * FROM music_info WHERE Bitrate > (?)", db, params=(bitrate,))
        elif operator == "<=":
            music_df = pd.read_sql_query("SELECT * FROM music_info WHERE Bitrate <= (?)", db, params=(bitrate,))
        elif operator == ">=":
            music_df = pd.read_sql_query("SELECT * FROM music_info WHERE Bitrate >= (?)", db, params=(bitrate,))
        else:
            print("Please input a valid operator.\n")
        music_df.to_csv('data/csv_exports/bitrate_search-%s-%s-%s%s.csv' % (date, time, operator, bitrate), index=False)
        print("\nSUCCESS!\nExported album data to 'data/csv_exports/bitrate_search-%s-%s-%s%s.csv'" % (date, time, operator, bitrate))
    except Exception as e: print("\033[91m Export failed: ", e, "\033[0m")
    go_back('\nGo back to menu? y/N: ')

def export_missing(db):
    """Export files with missing tag data"""
    try:
        music_df = pd.read_sql_query("SELECT  FROM music_info WHERE Album_Artist is null OR Artist is null OR Album is null OR Track_Number is null OR Genre is null OR Title is null OR Year is null", db)
        music_df.to_csv('data/csv_exports/missing_tag_search-%s-%s.csv' % (date, time), index=False)
        print("\nSUCCESS!\nExported album data to 'data/csv_exports/missing_tag_search-%s-%s.csv'" % (date, time))
    except Exception as e: print("\033[91m Export failed: ", e, "\033[0m")
    go_back('\nGo back to menu? y/N: ')

main_menu = {
    "a": [iter_music, lambda: iter_music(path, db, cursor, hasher), "(a)dd"],
    "e": [export_to_csv, lambda: export_to_csv(db), "(e)xport"]
}
export_menu = {
    "f": [export_all, lambda: export_all(db), "(f)ull"],
    "a": [export_albums, lambda: export_albums(db), "(a)lbums"],
    "b": [export_by_bitrate, lambda: export_by_bitrate(db), "(b)itrate"],
    "m": [export_missing, lambda: export_missing(db), "(m)issing"]
}

########################################################

if __name__ == '__main__':
    if sys.argv[1] == "--help":
        os.system("less README.md")
    else:
        menu_loop(main_menu)