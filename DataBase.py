import sqlite3

class DataBase:
    def __init__(self, database_dir):
        self.database_con = sqlite3.connect(database_dir)
        self.cur = self.database_con.cursor()

        # create user database
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS user_table(
                user_name   TEXT PRIMARY KEY,
                salt        TEXT,
                enc_pwd     TEXT,
                cookie      TEXT NOT NULL UNIQUE,
                exp         INTEGER,
                money       INTEGER)
            """)

        # create buy_table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS buy_table(
                buyer       TEXT,
                img_name    TEXT,
                owner       TEXT)
            """)

        # create img database
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS img_table(
                img_name    TEXT,
                cipher_img  TEXT,
                key         TEXT,
                nonce       TEXT,
                tag         TEXT,
                owner       TEXT,
                cost        INTEGER,
                UNIQUE(img_name, owner))
            """)

        self.database_con.commit()
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.database_con.close()
    
    def close(self):
        print("Close database.")
        self.database_con.close()
        
        
    ### User database handling
    ### ----------------------
    def Create_user(self, user_name: str, enc_pwd: str, salt: str, cookie: str, exp: int) -> bool:
        try:
            self.cur.execute("INSERT INTO user_table VALUES(?, ?, ?, ?, ?, ?)", 
                (user_name, salt, enc_pwd, cookie, exp, 0))
            self.database_con.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        
    def Get_user_info(self, cookie: str) -> tuple[str, int] | None:
        res = self.cur.execute("SELECT user_name, money FROM user_table WHERE cookie=?", (cookie, ))
        return res.fetchone()
    
    def Get_user_own(self, user_name: str) -> list[str]:
        # get all owned img name
        res = self.cur.execute(
            """
            SELECT img_name 
              FROM img_table 
             INNER JOIN user_table 
                ON user_table.user_name = img_table.owner 
             WHERE user_name=?
            """, 
            (user_name, )).fetchall()

        # return list of owned img name 
        return list(map(lambda x: x[0], res)) if res is not None else list()

    def Get_user_buy(self, cookie: str) -> list[tuple[str, str]]:
        buyer = self.Get_user_info(cookie)[9]
        
        # get all owned img name
        res = self.cur.execute( \
            "SELECT img_name, owner FROM buy_table WHERE buyer=?", 
            (buyer, )).fetchall()

        # return list of owned img name 
        return res if res is not None else list()
        
    def Get_user_security(self, user_name: str) -> tuple[str, str] | None:
        res = self.cur.execute(
            "SELECT salt, enc_pwd FROM user_table WHERE user_name=?", 
            (user_name, )).fetchone()
        return res
        
    def Get_cookie_exp(self, cookie: str) -> int | None:
        res = self.cur.execute(
            "SELECT exp FROM user_table WHERE cookie=?", 
            (cookie, )).fetchone()
        return res
        
    def Delete_user(self, user_name: str) -> None:
        self.cur.execute("DELETE FROM user_table WHERE user_name=?", (user_name, ))
        self.cur.execute("DELETE FROM img_table WHERE owner=?", (user_name, ))
        self.cur.execute("UPDATE img_table SET owner='' WHERE owner=?", (user_name, ))
        self.database_con.commit()
        
        
    ### Update user database
    ### --------------------
    def Update_exp(self, cookie: str, new_exp: int) -> None:
        self.cur.execute(
            "UPDATE user_table SET exp=? WHERE cookie=?", 
            (new_exp, cookie))
    
    def Update_cookie(self, user_name: str, new_cookie: str) -> None:
        self.cur.execute(
            "UPDATE user_table SET cookie=? WHERE user_name=?", 
            (new_cookie, user_name))
    
    def Del_own_img(self, user_name: str, img_name: str) -> None:
        self.cur.execute( \
            "UPDATE img_table SET owner='' WHERE owner=? AND img_name=?", \
            (user_name, img_name))

    def Buy_img(self, cookie: str, owner: str, img_name: str) -> bool:
        # get cost
        cost = self.cur.execute(
            "SELECT cost FROM img_table WHERE owner=? AND img_name=?",
            (owner, img_name)
        ).fetchone()
        if cost is None: return False
        else: cost = cost[0]

        # get buyer from cookie
        buyer = self.Get_user_info(cookie)[0]

        # minus money from buyer
        if not self.Minus_money(buyer, cost): 
            return False
        
        # add money to owner
        self.Add_money(owner, cost)

        # update buy table
        self.cur.execute("INSERT INTO buy_table VALUES(?, ?, ?)", (buyer, img_name, owner))
        
        self.database_con.commit()
        return True 

    def Add_money(self, user_name: str, amount: int) -> None:
        self.cur.execute("UPDATE user_table SET money=money+? WHERE user_name=?", (amount, user_name))
        self.database_con.commit()
    
    def Minus_money(self, user_name: str, amount: int, force = False) -> bool:
        res = self.cur.execute("SELECT money FROM user_table WHERE user_name=?", (user_name, ))
        money = int(res.fetchone()[0])
        if money < amount and not force:
            return False

        self.cur.execute("UPDATE user_table SET money=money-? WHERE user_name=?", (amount, user_name))
        self.database_con.commit()
        return True

        
    ### Image database handling
    ### -----------------------
    def Add_image(self, img_name: str, cipher_img: str, key: str, nonce: str, tag: str, owner: str, cost: int = 0) -> bool:
        try:
            self.cur.execute("INSERT INTO img_table VALUES(?, ?, ?, ?, ?, ?, ?)", \
                (img_name, cipher_img, key, nonce, tag, owner, cost))
            self.database_con.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        
    def Get_image(self, owner: str, img_name: str) -> tuple[str, str, str, str, str, str, int] | None:
        res =  self.cur.execute(
            "SELECT * FROM img_table WHERE img_name=? AND owner=?", 
            (img_name, owner))
        return res.fetchone()
        