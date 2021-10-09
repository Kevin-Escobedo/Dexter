import sqlite3

class PokedexDatabase:
    def __init__(self, databasePath: str = "pokedex.db"):
        self.db = sqlite3.connect(databasePath)
        self.cursor = self.db.cursor()
        self.dex_num = self.get_current_dex_num()

    def get_current_dex_num(self) -> int:
        '''Gets the current length of the database'''
        try:
            self.cursor.execute("SELECT COUNT(NUM) FROM POKEDEX")
            return self.cursor.fetchone()[0]
        except sqlite3.OperationalError:
            return 1

    def get_entry(self, dexnum: int) -> list:
        '''Gets the entry'''
        command = "SELECT * FROM POKEDEX WHERE NUM=?"
        self.cursor.execute(command, (dexnum,))
        return self.cursor.fetchone()
        
    def close_connection(self):
        '''Closes the connection to the database'''
        self.db.commit()
        self.db.close()
