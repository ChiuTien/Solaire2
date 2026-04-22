import pyodbc

class SQLServerDB:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            self.conn = pyodbc.connect(   #  CORRECTION ICI
                "DRIVER={ODBC Driver 18 for SQL Server};"
                "SERVER=localhost\\SQLEXPRESS;"
                "DATABASE=Solaire;"
                "UID=andie2;"
                "PWD=andie1234;"
                "Encrypt=yes;"
                "TrustServerCertificate=yes;"
            )
            print("Connexion OK")
            return self.conn

        except Exception as e:
            print(" Erreur connexion :", e)
            self.conn = None
            return None

    def cursor(self):
        if self.conn is None:
            self.connect()
        if self.conn is None:
            raise Exception(" Connexion échouée")
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
            self.conn = None


# ---------------- TEST ----------------
if __name__ == "__main__":
    try:
        db = SQLServerDB()

        result = db.fetch_all("SELECT * FROM appareil")

        for row in result:
            print(row)

        db.close()

    except Exception as e:
        print("Erreur :", e)
