import os
import sqlite3
from sqlite3 import Error
from Views.MessageBoxess import *

db_path_name = 'mobiles.db'
words_table_create = '''CREATE TABLE Words (
    id            INTEGER       PRIMARY KEY AUTOINCREMENT
                                NOT NULL,
    Word          VARCHAR (50)  UNIQUE NOT NULL,
    SoundName     VARCHAR (100),
    Transcription VARCHAR (50),
    State         INTEGER       NOT NULL
                                CHECK (State >= 1 || State <= 3) 
                                DEFAULT (1),
    DataInsert    TEXT (50)     NOT NULL,
    DataLastCall  TEXT (50)     NOT NULL
)'''
examples_table_create = '''CREATE TABLE Translates (
    Id           INTEGER      PRIMARY KEY AUTOINCREMENT
                              NOT NULL,
    WordId       INTEGER      NOT NULL,
    Translate    VARCHAR (50) NOT NULL,
    PartOfSpeach VARCHAR (50),
    FOREIGN KEY (
        WordId
    )
    REFERENCES Words (id) ON DELETE CASCADE
)'''
translates_table_create = '''CREATE TABLE Examples (
    Id          INTEGER       PRIMARY KEY AUTOINCREMENT
                              NOT NULL,
    TranslateId INTEGER       NOT NULL,
    Example     VARCHAR (200),
    FOREIGN KEY (
        TranslateId
    )
    REFERENCES Translates (id) ON DELETE CASCADE
)'''
con = None

select_words_for_model = 'SELECT  id, Word, SoundName FROM Words ORDER BY Word'
select = "SELECT  id, Word, SoundName FROM Words WHERE Word LIKE '{:s}%' ORDER BY Word"
select_word = "SELECT Word, Transcription, SoundName FROM Words WHERE id = {:d}"
select_translate = "SELECT id, Translate, PartOfSpeach FROM Translates WHERE WordId = {:d}"
select_example = "SELECT Example FROM Examples WHERE TranslateId = {:d}"
delete_example = 'DELETE FROM Examples WHERE TranslateId = {:d}'
delete_translate = 'DELETE FROM Translates WHERE id = {:d}'
delete_word = 'DELETE FROM Words WHERE id = {:d}'
update_translate = "UPDATE Translates SET Translate = '{:s}', PartOfSpeach = '{:s}' WHERE id = {:d}"
update_example = "UPDATE Examples SET Example = '{:s}' WHERE TranslateId = {:d}"
insert_example = "INSERT INTO Examples(TranslateId, Example) VALUES(?, ?)"
insert_translate = "INSERT INTO Translates(WordId, Translate, PartOfSpeach) VALUES(?, ?, ?)"

list_sql_query = [select_words_for_model, select, select_word, select_translate, select_example, delete_example,
                  delete_translate, delete_word, update_translate, update_example, insert_example, insert_translate]

_list_words_for_model = ['WordId', 'Word', 'SoundName', 'Words']
_list_select = ['SoundName', 'Word', 'Words']
_list_select_word = ['Word', 'Transcription', 'SoundName', 'Words']
_list_select_translates = ['TranslateId', 'Translate', 'PartOfSpeach', 'Translates']
_list_select_examples = ['Example', 'Examples']
_list_keys = [_list_words_for_model, _list_select, _list_select_word, _list_select_translates, _list_select_examples]


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


def select_data(window=None, index=0, value=None):
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
            if window:
                message_error = er.__str__()
                QMessageBox.critical(window, 'Error', message_error)
            else:
                print(er)
        finally:
            con.close()

    else:
        print('index out of range')


def delete_data(window=None, index=0, value=None):
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
            con.commit()
        except Error as er:
            if window:
                message_error = er.__str__()
                QMessageBox.critical(window, 'Error', message_error)
            else:
                print(er)
        finally:
            con.close()
    else:
        print('index out of range')


def update_data(index, name, translate_id, window=None, translate=None, part_of_speach=None, example=None):
    global con
    query = ''
    if index < len(list_sql_query):
        if name == 'Translate':
            query = list_sql_query[index].format(translate, part_of_speach, translate_id)
        else:
            query = list_sql_query[index].format(example, translate_id)
        try:
            con = sqlite3.connect(db_path_name)
            cur = con.cursor()
            cur.execute(query)
            con.commit()
        except Error as er:
            if window:
                message_error = er.__str__()
                QMessageBox.critical(window, 'Error', message_error)
            else:
                print(er)
        finally:
            con.close()

    else:
        print('index out of range')


def create_dictionary(window=None, index=0, value=None):
    _list_data = select_data(window, index, value)
    print(_list_data)


def insert_data(*values, window=None, index=0):
    global con
    query = ''
    if index < len(list_sql_query):
        query = list_sql_query[index]
        try:
            con = sqlite3.connect(db_path_name)
            cur = con.cursor()
            cur.execute(query, values)
            con.commit()
            return cur.lastrowid
        except Error as er:
            if window:
                message_error = er.__str__()
                QMessageBox.critical(window, 'Error', message_error)
            else:
                print(er)
        finally:
            con.close()

    else:
        print('index out of range')


def test(*values, index=0):
    global con
    query = ''
    list_values = [1, 'test example']
    # for val in values:
    #     list_values.append(val)
    query = list_sql_query[index]
    try:
        con = sqlite3.connect(r"D:\Documents\PythonProjects\PyDictionary\mobiles.db")
        cur = con.cursor()
        # _vals = tuple(values)
        cur.execute(query, values)
        con.commit()
        _id = cur.lastrowid
        print(_id)
        # list_data = cur.fetchall()
        # return list_data
    except Error as er:
        print(er)

    finally:
        con.close()


# create_dictionary(index=3, value=1)
# test(select_words_for_model)
sql_query = "DELETE FROM Examples WHERE TranslateId = 4"
_test_sql = "SELECT * FROM Examples WHERE TranslateId = :id"
select = "SELECT  id, Word, SoundName FROM Words WHERE Word LIKE ':val%' ORDER BY Word"
select_word = "SELECT Word, Transcription, SoundName FROM Words WHERE id = ?"
# test(3, 'движение', 'сущ', index=11)
