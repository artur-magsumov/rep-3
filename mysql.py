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

    reader = csv.reader(csvfile, delimiter=';')

    for line in reader:
        data_list.append(line)
    
def appending_values_to_acc_num():
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

##if __name__ == "__main__":
##values_from_database = get_pattern_and_acc_num_from_database()
##      open_csv()
##    appending_values_to_acc_num()
##    write_new_data_to_csv()
get_pattern_and_acc_num_from_database()
