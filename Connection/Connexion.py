import pyodbc

class SQLServerDB:
    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=localhost,1433;"  
            "DATABASE=EnergieDB;"
            "UID=sa;"
            "PWD=123pubgA!"
        )
        return self.conn

    def cursor(self):
        if not self.conn:
            self.connect()
        return self.conn.cursor()

    def execute(self, query, params=None):
        cur = self.cursor()
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        self.conn.commit()

    def fetch_all(self, query, params=None):
        cur = self.cursor()
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        return cur.fetchall()

    def close(self):
        if self.conn:
            self.conn.close()