from sqlite3 import Cursor, IntegrityError, Connection

class KeyManager:
    def __init__(self, database_con: Connection, cur: Cursor):
        self.database_con = database_con
        self.cur = cur
        
        # create key table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS key_table(
                enc_key     TEXT,
                nonce       TEXT,
                tag         TEXT,
                owner       TEXT PRIMARY KEY)
            """)
        self.database_con.commit()
        
    def Add_key(self, key_info: tuple[str, str, str, str]) -> bool:
        # enc_key: str, nonce: str, tag: str, owner: str
        try:
            self.cur.execute("INSERT INTO key_table VALUES(?, ?, ?, ?)", key_info)
            self.database_con.commit()
            return True
        except IntegrityError:
            return False
        
    def Get_key(self, owner: str) -> tuple[str, str, str]:
        res = self.cur.execute(
            "SELECT enc_key, nonce, tag FROM key_table WHERE owner=?", 
            (owner, )).fetchone()
        return res
        
    def Update_key(self, key_info: tuple[str, str, str, str]) -> None:
        self.cur.execute(
            "UPDATE key_table SET enc_key=?, nonce=?, tag=? WHERE owner=?", 
            key_info)
        self.database_con.commit()
    
    def Delete_key(self, owner: str) -> bool:
        self.cur.execute("DELETE FROM key_table WHERE owner=?", (owner, ))
        self.database_con.commit()
    