"""Export music db to csv"""
from datetime import date, datetime, time
import pandas as pd

date = datetime.now().date()
time = datetime.now().time().strftime('%H-%M-%S')

valid_operators = ["=", "<", ">", "<=", ">=", "!="]


def export_all(db):
    """Export all music info to csv"""
    try:
        music_df = pd.read_sql_query("SELECT * FROM music_info", db)
        music_df.to_csv(
            f'data/csv_exports/music_database-{date}-{time}.csv', index=False)
        print(
            f"✨ \n\033[1mSuccess!\033[0m\nExported all music info to 'data/csv_exports/music_database-{date}-{time}.csv'")
    except Exception as error:
        print(f"\033[91m Export failed: {error}\033[0m")
    input("Done! Hit 'Enter' to return...: ")


def export_albums(db):
    """Export full album list to csv"""
    try:
        music_df = pd.read_sql_query(
            "SELECT Album_Artist, Year, Album FROM music_info", db)
        music_df = music_df.drop_duplicates()
        music_df.to_csv(
            f'data/csv_exports/albums_database-{date}-{time}.csv', index=False)
        print(
            f"✨ \n\033[1mSuccess!\033[0m\n==> Exported album data to 'data/csv_exports/albums_database-{date}-{time}.csv'")
    except Exception as error:
        print(f"\033[91m Export failed: {error}\033[0m")
    input("Done! Hit 'Enter' to return...: ")


def export_by_bitrate(db):
    """Export conditionally by bitrate"""
    try:
        operator = ""
        while operator not in valid_operators:
            operator = input("Operator? (=, <, >, <=, >=, !=): ")
        bitrate = ""
        while not bitrate.isdigit():
            bitrate = input("Bitrate? (128, 192 etc): ")
        if operator == "=":
            music_df = pd.read_sql_query(
                "SELECT * FROM music_info WHERE Bitrate = (?)", db, params=(bitrate,))
        elif operator == "<":
            music_df = pd.read_sql_query(
                "SELECT * FROM music_info WHERE Bitrate < (?)", db, params=(bitrate,))
        elif operator == ">":
            music_df = pd.read_sql_query(
                "SELECT * FROM music_info WHERE Bitrate > (?)", db, params=(bitrate,))
        elif operator == "<=":
            music_df = pd.read_sql_query(
                "SELECT * FROM music_info WHERE Bitrate <= (?)", db, params=(bitrate,))
        elif operator == ">=":
            music_df = pd.read_sql_query(
                "SELECT * FROM music_info WHERE Bitrate >= (?)", db, params=(bitrate,))
        elif operator == "!=":
            music_df = pd.read_sql_query(
                "SELECT * FROM music_info WHERE Bitrate != (?)", db, params=(bitrate,))
        else:
            print("Please input a valid operator.\n")
        music_df.to_csv(
            f'data/csv_exports/bitrate_search-{date}-{time}-({operator}{bitrate}).csv', index=False)
        print(
            f"\n✨\033[1mSuccess!\033[0m\n==> Exported album data to 'data/csv_exports/bitrate_search-{date}-{time}-({operator}{bitrate}).csv'")
    except Exception as error:
        print(f"\033[91m Export failed: {error}\033[0m")
    input("Done! Hit 'Enter' to return...: ")


def export_by_length(db):
    """Export conditionally by song duration"""
    try:
        operator = ""
        while operator not in valid_operators:
            operator = input("Operator? (=, <, >, <=, >=, !=): ")
        duration = ""
        while not duration.isdigit():
            duration = input("Song length? (in minutes, whole): ")
        duration = int(duration) * 60
        if operator == "=":
            music_df = pd.read_sql_query(
                "SELECT * FROM music_info WHERE Duration = (?)", db, params=(duration,))
        elif operator == "<":
            music_df = pd.read_sql_query(
                "SELECT * FROM music_info WHERE Duration < (?)", db, params=(duration,))
        elif operator == ">":
            music_df = pd.read_sql_query(
                "SELECT * FROM music_info WHERE Duration > (?)", db, params=(duration,))
        elif operator == "<=":
            music_df = pd.read_sql_query(
                "SELECT * FROM music_info WHERE Duration <= (?)", db, params=(duration,))
        elif operator == ">=":
            music_df = pd.read_sql_query(
                "SELECT * FROM music_info WHERE Duration >= (?)", db, params=(duration,))
        elif operator == "!=":
            music_df = pd.read_sql_query(
                "SELECT * FROM music_info WHERE Duration != (?)", db, params=(duration,))
        else:
            print("Please input a valid operator.\n")
        music_df.to_csv(
            f'data/csv_exports/length_search-{date}-{time}({operator}{(duration / 60)}minutes).csv', index=False)
        print(
            f"\n✨\033[1mSuccess!\033[0m\n==> Exported album data to 'data/csv_exports/length_search{date}-{time}({operator}{(duration / 60)}minutes).csv'")
    except Exception as error:
        print(f"\033[91m Export failed: {error}\033[0m")
    input("Done! Hit 'Enter' to return...: ")


def export_missing(db):
    """Export files with missing tag data"""
    try:
        music_df = pd.read_sql_query(
            "SELECT * FROM music_info WHERE Album_Artist is null OR Artist is null OR Album is null OR Track_Number is null OR Genre is null OR Title is null OR Year is null", db)
        music_df.to_csv(
            f'data/csv_exports/missing_tag_search-{date}-{time}.csv', index=False)
        print(
            f"\n✨\033[1mSuccess!\033[0m\n==> Exported album data to 'data/csv_exports/missing_tag_search-{date}-{time}.csv'")
    except Exception as error:
        print(f"\033[91m Export failed: {error}\033[0m")
    input("Done! Hit 'Enter' to return...: ")
