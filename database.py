import sqlite3


class DataBase:
    def __init__(self, db_name):
        self.conn = None
        self.db_name = db_name

        self.get_connection()
        self.create_table()
        self.close_connection()

    def get_connection(self):
        self.conn = sqlite3.connect(self.db_name)

    def close_connection(self):
        self.conn.close()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS settings (
        api_key TEXT NOT NULL PRIMARY KEY,
        url TEXT NOT NULL,
        language TEXT NOT NULL);
        """

        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()
        cursor.close()

    def insert_data(self, api_key, language):
        query = """
        INSERT INTO settings
        (api_key, url, language)
        VALUES (?, ?, ?);
        """

        params = (api_key, 'https://dadata.ru/', language)
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        cursor.close()

    def set_api_key(self, api_key):
        self.conn.cursor().execute('''UPDATE settings SET api_key= ? ''', (api_key,))
        self.conn.commit()

    def set_url(self, url):
        self.conn.cursor().execute('''UPDATE settings SET url= ? ''', (url,))
        self.conn.commit()

    def set_language(self, language):
        self.conn.cursor().execute('''UPDATE settings SET language= ?''', (language,))
        self.conn.commit()

    def get_api_key(self):
        cursor = self.conn.cursor()
        return cursor.execute("SELECT api_key FROM settings").fetchone()[0]

    def get_url(self):
        cursor = self.conn.cursor()
        return cursor.execute("SELECT url FROM settings").fetchone()[0]

    def get_language(self):
        cursor = self.conn.cursor()
        return cursor.execute("SELECT language FROM settings").fetchone()[0]

    def is_empty(self):
        return self.conn.cursor().execute("SELECT * FROM settings").fetchone() is None
