import psycopg2
from typing import Union

class Database:
    def __init__(self, host : str, db_name : str, user : str, pdw : str):
        self.host = host
        self.db_name = db_name
        self.user = user
        self.pdw = pdw
        self.CONN = None
        self.cursor = None

    def connect(self):
        try:
            self.CONN = psycopg2.connect(
                host=self.host,
                database=self.db_name,
                user=self.user,
                password=self.pdw
            )
            self.cursor = self.CONN.cursor()
            return True
        except:
            return False

    def query(self, query) -> list[Union[bool,object]]:
        try:
            self.cursor.execute(query)
            return [True, self.cursor]
        except Exception as e:
            self.CONN.rollback()
            return [False, e]