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
    Transcription VARCHAR (50),
    State         INTEGER       NOT NULL
                                CHECK (State >= 1 || State <= 3) 
                                DEFAULT (1),
    DataInsert    TEXT (50)     NOT NULL,
    DataLastCall  TEXT (50)     NOT NULL
);'''
examples_table_create = '''CREATE TABLE Examples (
    ExampleId   INTEGER       PRIMARY KEY AUTOINCREMENT
                              NOT NULL,
    TranslateId INTEGER       REFERENCES Translates (TranslateId) ON DELETE CASCADE
                                                                  ON UPDATE CASCADE,
    WordId      INTEGER       REFERENCES Words (WordId) ON DELETE CASCADE
                                                        ON UPDATE CASCADE,
    Example     VARCHAR (200) 
);'''
translates_table_create = '''(
    TranslateId  INTEGER      PRIMARY KEY AUTOINCREMENT
                              NOT NULL,
    WordId       INTEGER      NOT NULL
                              REFERENCES Words (WordId) ON DELETE CASCADE
                                                        ON UPDATE CASCADE,
    Translate    VARCHAR (50) NOT NULL,
    PartOfSpeach VARCHAR (50) 
);'''
con = None

select_words_for_model = 'SELECT DISTINCT WordId, Word FROM Words ORDER BY Word'
select = "SELECT DISTINCT SoundName, Word FROM Words WHERE Word LIKE '{:s}%' ORDER BY Word"
select_word = "SELECT Word, Transcription, SoundName FROM Words WHERE WordId = {:d}"
select_translates = "SELECT TranslateId, Translate, PartOfSpeach FROM Translates WHERE WordId = {:d}"
select_examples = "SELECT Example FROM Examples WHERE TranslateId = {:d}"
list_sql_query = [select_words_for_model, select, select_word, select_translates, select_examples]


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


def select_data(window, index=0, value=None):
    global con
    if index < len(list_sql_query):
        if value:
            query = list_sql_query[index]
            query = query.format(value)
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


def test(sqlQuery):
    global con
    try:
        con = sqlite3.connect(db_path_name)
        cur = con.cursor()
        cur.execute(sqlQuery)
        list_data = cur.fetchall()
        return list_data
    except Exception as er:
        # message_error = er.__str__()
        # QMessageBox.critical(window, 'Error', message_error)
        print(er)
    finally:
        con.close()
