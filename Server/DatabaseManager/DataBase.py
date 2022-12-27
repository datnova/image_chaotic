from sqlite3 import connect
from typing import Union
from .UserManager import UserManager
from .BuyerManager import BuyerManager
from .ImageManager import ImageManager
from .KeyManager import KeyManager

class DataBase:
    def __init__(self, database_dir):
        self.database_con = connect(database_dir)
        self.cur = self.database_con.cursor()
        
        self.user_table = UserManager(self.database_con, self.cur)
        self.buyer_table = BuyerManager(self.database_con, self.cur)
        self.image_table = ImageManager(self.database_con, self.cur)
        self.key_table = KeyManager(self.database_con, self.cur)
    
    def Create_user(self, user_info: tuple[str, str, str, str, int], key_info: tuple[str, str, str, str]) -> bool:
        return self.key_table.Add_key(key_info) and \
                self.user_table.Add_user(user_info)
    
    def Get_user_info(self, cookie: str) -> Union[tuple[str, int], None]:
        return self.user_table.Get_user_info(cookie)

    def Get_user_owned(self, owner: str) -> Union[list[tuple[str, int]], None]:
        if self.user_table.User_existed(owner) == False: return None
        return self.image_table.Get_images_owned(owner)
    
    def Get_user_purchased(self, cookie: str) -> list[tuple[str, int, str]]:
        buyer = self.user_table.Get_user_info(cookie)[0]
        return self.buyer_table.Get_purchased_images(buyer)
    
    def Get_user_security(self, user_name: str) -> Union[tuple[str, str], None]:
        return self.user_table.Get_user_security(user_name)
    
    def Get_cookie_exp(self, cookie: str) -> Union[tuple[int], None]:
        return self.user_table.Get_cookie_exp(cookie)
    
    def Update_cookie(self, user_name: str, new_cookie: str) -> None:
        return self.user_table.Update_cookie(user_name, new_cookie)
    
    def Update_exp(self, cookie: str, new_exp: str) -> None:
        return self.user_table.Update_exp(cookie, new_exp)
    
    def Get_user_key(self, owner: str) -> tuple[str, str, str]:
        return self.key_table.Get_key(owner)
    
    def Check_image_owned(self, img_name: str, owner: str) -> bool:
        return self.image_table.Check_image(img_name, owner)
    
    def Check_image_purchased(self, buyer: str, img_name: str, owner: str) -> bool:
        return self.buyer_table.Check_purchased(buyer, img_name, owner)
    
    def Add_image(self, img_info: tuple[str, str, str, str, str, int]):
        return self.image_table.Add_image(img_info)
    
    def Get_image(self, img_name: str, owner: str) -> tuple[str, str, str]:
        return self.image_table.Get_image_security(img_name, owner)
    
    def Add_purchase(self, receipt: tuple[str, str, str, int]) -> bool:
        self.buyer_table.Add_purchase(receipt)
    