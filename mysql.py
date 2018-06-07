'''
    Это файлик с неудачным названием :)
    Здесь хранится код для того что бы заполнить csv
    файл в котором следует дозаполнить таблицу обращаясь
    к БД MySql
'''

import pymysql
import csv
import re
data_list = []

def get_pattern_and_acc_num_from_database():
    '''Получаем pattern и account_number из таблицы базы данных
       в виде кортежей'''
    conn = pymysql.connect("127.0.0.1","root","890","playground")
    cur = conn.cursor()
    mys = ("""
            select pattern, account_number
            from catalog
        """)
    cur.execute(mys)
    return cur.fetchall()
    
def create_list_from_csv(csvfile):
    data_list.clear()
    reader = csv.reader(csvfile, delimiter=';')
    print(reader)
    for line in reader:
        data_list.append(line)
    
def appending_values_to_acc_num():
    print(data_list)
    for i in data_list:
        if i[4]:
            continue
        for tupl in get_pattern_and_acc_num_from_database():
            res = re.search(tupl[0], i[2])
            if not res:
                continue
            i[4] = str(tupl[1])
    

def write_new_data_to_csv(csvfilename):
    with open(csvfilename, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        for line in data_list:
            writer.writerow(line)

def open_csv(csvfilename):
    with open(csvfilename) as filename:
        create_list_from_csv(filename)

def main_mysql(name):
    get_pattern_and_acc_num_from_database()
    open_csv(name)
    appending_values_to_acc_num()
    write_new_data_to_csv(name)
if __name__ == "__main__":
    main()
