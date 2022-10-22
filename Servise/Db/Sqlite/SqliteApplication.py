import os
import sqlite3
from sqlite3 import Error
from Views.MessageBoxess import *

db_path_name = 'mobiles.db'
words_table_create = '''CREATE TABLE Words (
    WordId        INTEGER       PRIMARY KEY AUTOINCREMENT
                                NOT NULL,
    Word          VARCHAR (50)  NOT NULL,
    SoundName     VARCHAR (100),
    PartOfSpeach  VARCHAR (50),
    Transcription VARCHAR (50),
    State         INTEGER       NOT NULL
                                CHECK (State >= 1 || State <= 3) 
                                DEFAULT (1),
    DataInsert    TEXT (50)     NOT NULL,
    DataLastCall  TEXT (50)     NOT NULL
);'''
examples_table_create = '''CREATE TABLE Examples (
    ExampleId INTEGER       PRIMARY KEY AUTOINCREMENT
                            NOT NULL,
    WordId    INTEGER       REFERENCES Words (WordId) ON DELETE CASCADE
                                                      ON UPDATE CASCADE,
    Example   VARCHAR (200) 
);'''
translates_table_create = '''CREATE TABLE Translates (
    TranslateId INTEGER      PRIMARY KEY AUTOINCREMENT
                             NOT NULL,
    WordId      INTEGER      NOT NULL
                             REFERENCES Words (WordId) ON DELETE CASCADE
                                                       ON UPDATE CASCADE,
    Translate   VARCHAR (50) NOT NULL
)'''
con = None

select_words_for_model = 'SELECT DISTINCT SoundName, Word FROM Words ORDER BY Word'
select = "SELECT DISTINCT SoundName, Word FROM Words WHERE Word LIKE '{:s}%' ORDER BY Word"
list_sql_query = [select_words_for_model, select]


def create_empty_tables(window):
    global con
    try:
        con = sqlite3.connect(db_path_name)
        cur = con.cursor()
        cur.execute(words_table_create)
        cur.execute(examples_table_create)
        cur.execute(translates_table_create)
    except Error as er:
        message_error = er.__str__()
        QMessageBox.critical(window, 'Error', message_error)
    finally:
        con.close()


def is_db_exist():
    return os.path.exists(db_path_name)


def select_data(window, index=0, start=None):
    global con
    if index < len(list_sql_query):
        if start:
            query = list_sql_query[index]
            query = query.format(start)
        else:
            query = list_sql_query[index]
        try:
            con = sqlite3.connect(db_path_name)
            cur = con.cursor()
            cur.execute(query)
            list_data = cur.fetchall()
            return list_data
        except Error as er:
            message_error = er.__str__()
            QMessageBox.critical(window, 'Error', message_error)
        finally:
            con.close()
    else:
        print('index out of range')

# def test( ):
#
#     try:
#         con = sqlite3.connect(db_path_name)
#         cur = con.cursor()
#         cur.execute(query)
#         list_data = cur.fetchall()
#         return list_data
#     except Error as er:
#         message_error = er.__str__()
#         QMessageBox.critical(window, 'Error', message_error)
#     finally:
#         con.close()
