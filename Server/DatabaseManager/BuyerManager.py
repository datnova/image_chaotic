from sqlite3 import Cursor, IntegrityError, Connection

class BuyerManager:
    def __init__(self, database_con: Connection, cur: Cursor):
        self.database_con = database_con
        self.cur = cur
        
        # create buyer table
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS buy_table(
                buyer       TEXT,
                img_name    TEXT,
                owner       TEXT,
                cost        INTEGER,
                UNIQUE(buyer, img_name, owner))
            """)
        self.database_con.commit()
        
    def Get_purchased_images(self, buyer: str) -> list[tuple[str, int, str]]:
        # get all owned img name
        res = self.cur.execute(
            "SELECT img_name, cost, owner FROM buy_table WHERE buyer=?", 
            (buyer, )).fetchall()

        # return list of owned img name 
        return res if res is not None else list()

    def Add_purchase(self, receipt: tuple[str, str, str, int]) -> bool:
        # buyer: str, img_name: str, owner: str, cost: int
        try:
            self.cur.execute("INSERT INTO buy_table VALUES(?, ?, ?, ?)", receipt)
            self.database_con.commit()
            return True
        except IntegrityError:
            return False
    
    def Check_purchased(self, buyer: str, img_name: str, owner: str) -> bool:
        return self.cur.execute(
            "SELECT count(1) FROM buy_table WHERE buyer=? AND img_name=? AND owner=?", 
            (buyer, img_name, owner)).fetchone()[0] != 0
        