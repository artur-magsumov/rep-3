from __future__ import print_function
import json
import jsonschema
from jsonschema import validate
import sys
import pymysql

schema = {
         "type": "object",
         "properties": {
                       "id": {"type": "number"},
                       "pattern": {"type": "string"},
                       "description": {"type": "string"},
                       "account_number": {"type": "number"},
                       },
         }

def read_db():
    conn = pymysql.connect('127.0.0.1', 'root', '890', 'playground')
    query = """select * from catalog"""
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(query)
        data = cursor.fetchall()
    for idx, item in enumerate(data):
        try:
            validate(item, schema)
            sys.stdout.write("Record #{}: OK\n".format(idx))
            return str(json.dumps(data, indent=4)).encode("utf8")
        except jsonschema.exceptions.ValidationError as ve:
            return b'error'

if __name__ == "__main__":
    print(read_db())
