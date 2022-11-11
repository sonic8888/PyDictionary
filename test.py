select_words_for_model = 'SELECT DISTINCT WordId, Word, SoundName FROM Words ORDER BY Word'
select = "SELECT DISTINCT SoundName, Word FROM Words WHERE Word LIKE '{:s}%' ORDER BY Word"
select_word = "SELECT Word, Transcription, SoundName FROM Words WHERE WordId = {:d}"
select_translate = "SELECT TranslateId, Translate, PartOfSpeach FROM Translates WHERE WordId = {:d}"
select_example = "SELECT Example FROM Examples WHERE TranslateId = {:d}"
delete_example = 'DELETE FROM Examples WHERE TranslateId = {:d}'
delete_translate = 'DELETE FROM Translates WHERE TranslateId = {:d}'
delete_word = 'DELETE FROM Words WHERE WordId = {:d}'
update_translate = "UPDATE Translates SET Translate = '{:s}', PartOfSpeach = '{:s}' WHERE TranslateId = {:d}"
update_example = "UPDATE Examples SET Example = '{:s}' WHERE TranslateId = {:d}"

list_sql_query = [select_words_for_model, select, select_word, select_translate, select_example, delete_example,
                  delete_translate, delete_word, update_translate, update_example]


def displey(index, name, translate_id, window=None, translate=None, part_of_speach=None, example=None):
    _sql = ''
    if name == 'Translate':
        _sql = list_sql_query[index].format(translate, part_of_speach, translate_id)
    else:
        _sql = list_sql_query[index].format(example, translate_id)

    print(_sql)


if __name__ == "__main__":
    _translate = 'добавить'
    _example = """I can't move, Tracy thought. I'll stay here.
Я не могу двигаться, подумала Трейси. Я останусь здесь."""
    _part_of_speach = 'сущ'
    _id = 2
    _name = 'Translates'
    displey(index=9, name=_name, translate_id=_id, translate=_translate, part_of_speach=_part_of_speach,
            example=_example)
