


def add_data_from_csv():
    from csv import reader
    db_path = input('drag and drop the goole csv file\
here or just type the full path: ').replace("'", '').strip()

    pass_l = []

    with open(db_path) as file:
        reader = reader(file)
        for row in reader:
            name= row[0]
            url = row[1]
            username = row[2]
            password = row[3]
            note = row[4]
            pass_l.append((name, url, username, password, note))

    return pass_l
