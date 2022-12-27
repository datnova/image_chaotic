from sqlite3 import Cursor, IntegrityError, Connection
from typing import Union

class ImageManager:
    def __init__(self, database_con: Connection, cur: Cursor):
        self.database_con = database_con
        self.cur = cur
        
        # create image table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS img_table(
                img_name    TEXT,
                cipher_img  TEXT,
                nonce       TEXT,
                tag         TEXT,
                owner       TEXT,
                cost        INTEGER,
                UNIQUE(img_name, owner))
            """)
        self.database_con.commit()
    
    def Add_image(self, img_info: tuple[str, str, str, str, str, int]) -> bool:
        # img_name: str, cipher_img: str, nonce: str, tag: str, owner: str. cost: int
        try:
            self.cur.execute("INSERT INTO img_table VALUES(?, ?, ?, ?, ?, ?)", img_info)
            self.database_con.commit()
            return True
        except IntegrityError:
            return False
        
    def Get_image_security(self, img_name: str, owner: str) -> tuple[str, str, str]:
        res = self.cur.execute(
            "SELECT cipher_img, nonce, tag FROM img_table WHERE img_name=? AND owner=?", 
            (img_name, owner)).fetchone()
        return res
    
    def Get_images_owned(self, owner: str) -> list[tuple[str, int]]:
        res = self.cur.execute(
            "SELECT img_name, cost FROM img_table WHERE owner=?", 
            (owner, )).fetchall()
        return res if res is not None else list()
    
    def Check_image(self, img_name: str, owner: str) -> bool:
        return self.cur.execute(
            "SELECT count(1) FROM img_table WHERE img_name=? AND owner=?", 
            (img_name, owner)).fetchone()[0] != 0
        
    def Get_cost(self, img_name: str, owner: str) -> Union[tuple[int], None]:
        cost = self.cur.execute(
            "SELECT cost FROM img_table WHERE img_name=? AND owner=?", 
            (img_name, owner)).fetchone()
        return cost
        