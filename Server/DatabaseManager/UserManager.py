from sqlite3 import Cursor, IntegrityError, Connection
from typing import Union

class UserManager:
    def __init__(self, database_con: Connection, cur: Cursor):
        self.database_con = database_con
        self.cur = cur
        
        # create user table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS user_table(
                user_name   TEXT PRIMARY KEY,
                salt        TEXT,
                enc_pwd     TEXT,
                cookie      TEXT NOT NULL UNIQUE,
                exp         INTEGER,
                money       INTEGER)
            """)
        self.database_con.commit()
        
    def Add_user(self, user_info: tuple[str, str, str, int, int]) -> bool:
        # user_name: str, salt: str, enc_pwd: str, cookie: str, exp: int, money: int 
        try:
            self.cur.execute("INSERT INTO user_table VALUES(?, ?, ?, ?, ?, ?)", 
                user_info)
            self.database_con.commit()
            return True
        except IntegrityError:
            return False
    
    def User_existed(self, user_name: str) -> bool:
        return self.cur.execute(
            "SELECT count(1) FROM user_table WHERE user_name=?", 
            (user_name, )
        ).fetchone()[0] != 0
    
    def Get_user_info(self, cookie: str) -> Union[tuple[str, int], None]:
        res = self.cur.execute(
            "SELECT user_name, money FROM user_table WHERE cookie=?", 
            (cookie, ))
        return res.fetchone()
    
    def Get_user_security(self, user_name: str) -> Union[tuple[str, str], None]:
        res = self.cur.execute(
            "SELECT salt, enc_pwd FROM user_table WHERE user_name=?", 
            (user_name, )).fetchone()
        return res
        
    def Get_cookie_exp(self, cookie: str) -> Union[tuple[int], None]:
        res = self.cur.execute(
            "SELECT exp FROM user_table WHERE cookie=?", 
            (cookie, )).fetchone()
        return res
    
    def Get_cookie_user(self, user_name: str) -> Union[str, None]:
        res = self.cur.execute(
            "SELECT cookie FROM user_table WHERE user_name=?", 
            (user_name, )).fetchone()
        return res
    
    def Update_exp(self, cookie: str, new_exp: int) -> None:
        self.cur.execute(
            "UPDATE user_table SET exp=? WHERE cookie=?", 
            (new_exp, cookie))
        self.database_con.commit()
    
    def Update_cookie(self, user_name: str, new_cookie: str) -> None:
        self.cur.execute(
            "UPDATE user_table SET cookie=? WHERE user_name=?", 
            (new_cookie, user_name))
        self.database_con.commit()
    
    def Update_money(self, user_name: str, amount: int) -> None:
        self.cur.execute("UPDATE user_table SET money=money+? WHERE user_name=?", (amount, user_name))
        self.database_con.commit()
    
    def Delete_user(self, user_name: str = None, cookie: str = None) -> None:
        if user_name is not None:
            self.cur.execute("DELETE FROM user_table WHERE user_name=?", (user_name, ))
        elif cookie is not None:
            self.cur.execute("DELETE FROM user_table WHERE cookie=?", (cookie, ))
        self.database_con.commit()
        