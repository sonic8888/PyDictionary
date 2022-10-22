def displey():

    a = 'ab'
    query = f"SELECT DISTINCT Word FROM Words WHERE Word LIKE '{a}%' ORDER BY Word"
    print(query)
