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
    DataInsert    DATE     NOT NULL,
    DataLastCall  DATE     NOT NULL
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
select = "SELECT  id, Word, SoundName FROM Words WHERE Word LIKE ? ORDER BY Word"
select_word = "SELECT Word, Transcription, SoundName FROM Words WHERE id = ?"
select_translate = "SELECT * FROM Translates WHERE WordId = ?"
select_example = "SELECT * FROM Examples WHERE TranslateId = ?"
delete_example = 'DELETE FROM Examples WHERE id = ?'
delete_translate = 'DELETE FROM Translates WHERE id = ?'
delete_word = 'DELETE  FROM Words WHERE id = ?'
update_translate = '''UPDATE Translates SET Translate = ?, PartOfSpeach = ? WHERE id = ?'''
update_example = '''UPDATE Examples SET Example = ? WHERE TranslateId = ?'''
insert_example = "INSERT INTO Examples(TranslateId, Example) VALUES(?, ?)"
insert_translate = "INSERT INTO Translates(WordId, Translate, PartOfSpeach) VALUES(?, ?, ?)"
insert_word = "INSERT INTO Words('Word', 'SoundName', 'Transcription', State, 'DataInsert', 'DataLastCall')" \
              " VALUES(?, ?, ?, ?, ?, ?)"

list_sql_query = [select_words_for_model, select, select_word, select_translate, select_example, delete_example,
                  delete_translate, delete_word, update_translate, update_example, insert_example, insert_translate,
                  insert_word]
list_table_name = ['Words', 'Translates', 'Examples']
list_create_tables = [words_table_create, examples_table_create, translates_table_create]


# _list_words_for_model = ['WordId', 'Word', 'SoundName', 'Words']
# _list_select = ['SoundName', 'Word', 'Words']
# _list_select_word = ['Word', 'Transcription', 'SoundName', 'Words']
# _list_select_translates = ['TranslateId', 'Translate', 'PartOfSpeach', 'Translates']
# _list_select_examples = ['Example', 'Examples']
# _list_keys = [_list_words_for_model, _list_select, _list_select_word, _list_select_translates, _list_select_examples]


def create_empty_tables(window=None, sql_create_table=None):
    global con
    try:
        con = sqlite3.connect(db_path_name)
        cur = con.cursor()
        cur.execute(sql_create_table)
    except Error as er:
        message_error = er.__str__()
        QMessageBox.critical(window, 'Error', message_error)
    finally:
        con.close()


def is_db_exist():
    return os.path.exists(db_path_name)


def select_data_like(window=None, index=0, value=None):
    global con
    data = None
    query = None
    if index < len(list_sql_query):
        query = list_sql_query[index]
        data = (value + '%',)
    try:
        con = sqlite3.connect(db_path_name)
        cur = con.cursor()
        cur.execute(query, data)
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


def select_data(window=None, index=0, value=None):
    global con
    data = ()
    if index < len(list_sql_query):
        if value:
            query = list_sql_query[index]
            data = (value,)
        else:
            query = list_sql_query[index]
        try:
            con = sqlite3.connect(db_path_name)
            cur = con.cursor()
            cur.execute(query, data)
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
    data = ()
    if index < len(list_sql_query):

        query = list_sql_query[index]
        data = (value,)
        try:
            con = sqlite3.connect(r'D:\Documents\PythonProjects\PyDictionary\mobiles.db')
            cur = con.cursor()
            con.execute("PRAGMA foreign_keys = ON")
            cur.execute(query, data)
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
    data = None
    if index < len(list_sql_query):
        if name == 'Translate':
            # query = list_sql_query[index].format(translate, part_of_speach, translate_id)
            query = list_sql_query[index]
            data = (translate, part_of_speach, translate_id)
        else:
            # query = list_sql_query[index].format(example, translate_id)
            query = list_sql_query[index]
            data = (example, translate_id)
        try:
            con = sqlite3.connect(db_path_name)
            cur = con.cursor()
            con.execute("PRAGMA foreign_keys = ON")
            cur.execute(query, data)
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


def test(index=0):
    global con
    select = '''SELECT  id, Word, SoundName FROM Words WHERE Word LIKE ?  ORDER BY Word'''
    query = ''
    data = ('a' + '%',)
    list_values = [1, 'test example']
    # for val in values:
    #     list_values.append(val)
    query = list_sql_query[index]
    try:
        con = sqlite3.connect(r"D:\Documents\PythonProjects\PyDictionary\mobiles.db")
        cur = con.cursor()
        # _vals = tuple(values)
        cur.execute(select, data)
        list_data = cur.fetchall()
        return list_data
    except Error as er:
        print(er)

    finally:
        con.close()


def is_exist_table(window=None, table_name=None):
    global con
    sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='{:s}'".format(table_name)
    try:
        con = sqlite3.connect(r"D:\Documents\PythonProjects\PyDictionary\mobiles.db")
        cur = con.cursor()
        cur.execute(sql)
        list_data = cur.fetchall()
        return bool(list_data)
    except Error as er:
        if window:
            message_error = er.__str__()
            QMessageBox.critical(window, 'Error', message_error)
        else:
            print(er)
    finally:
        con.close()
    return True


def load(window=None):
    is_exist = True
    for index, name in enumerate(list_table_name):
        if not is_exist_table(window, name):
            is_exist = False
            create_empty_tables(window, list_create_tables[index])
    return is_exist


def main():
    # delete_data(index=7, value=10 )
    print(test())


if __name__ == '__main__':
    main()
