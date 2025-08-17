import sqlite3

class Database:
    def __init__(self, db_name='data/high_scores.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS high_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player_name TEXT NOT NULL,
                score INTEGER NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.connection.commit()

    def insert_score(self, player_name, score):
        self.cursor.execute('''
            INSERT INTO high_scores (player_name, score)
            VALUES (?, ?)
        ''', (player_name, score))
        self.connection.commit()

    def get_high_scores(self, limit=10):
        self.cursor.execute('''
            SELECT player_name, score, date FROM high_scores
            ORDER BY score DESC
            LIMIT ?
        ''', (limit,))
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()