from DatabaseManager.DataBase import DataBase
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from os import urandom
from base64 import b64encode, b64decode
from time import time
from typing import Union
from json import loads, dump
from CipherImg.Decrypt import DecryptImg
from CipherImg.Encrypt import EncryptImg

COOKIE_LIFE_LIMIT = 3600 * 12
DATABASE_KEY_FILE = "database_key.json"

class ServerApp:
    def __init__(self, database_dir: str):
        self.db = DataBase(database_dir)
        self.db_key = None

    def Create_user_info(self, user_name: str, password: str) -> tuple[str, str, str, str, int]:
        # user_name: str, salt: str, enc_pwd: str, cookie: str, exp: str, money: int 
        salt = urandom(8)

        h = SHA256.new()
        h.update(salt + password.encode() + salt)
        
        salt = b64encode(salt).decode()
        enc_pwd = b64encode(h.digest()).decode()
        cookie = b64encode(urandom(32)).decode()
        exp = int(time()) + COOKIE_LIFE_LIMIT
        money = 100
        return (user_name, salt, enc_pwd, cookie, exp, money)
    
    def Create_key_info(self, owner: str, key: bytes = None) -> tuple[str, str, str, str]:
        # enc_key: str, nonce: str, tag: str, owner: str
        key = urandom(16) if key is None else key
        cipher = AES.new(self.db_key, AES.MODE_GCM)
        cipher.update(owner.encode())
        enc_key, tag = cipher.encrypt_and_digest(key)

        # convert to base64 for saving
        enc_key = b64encode(enc_key).decode()
        nonce = b64encode(cipher.nonce).decode()
        tag = b64encode(tag).decode()
        return (enc_key, nonce, tag, owner)
    
    def Create_user(self, user_name: str, password: str) -> dict[str, Union[str, bool]]:
        if not (6 <= len(user_name) <= 24):
            return {"result": False, "message": "invalid username length"}
    
        if not(8 <= len(password) <= 24):
            return {"result": False, "message": "invalid password length"}

        user_info = self.Create_user_info(user_name, password)
        key_info = self.Create_key_info(user_name)

        # add to database
        result = self.db.Create_user(user_info, key_info)
        if result == False:
            return {"result": False, "message": "username has already been taken"}
        return {"result": True, "message": "user create successful"}
    
    def Login(self, username: str, password: str) -> dict[str, Union[str, bool]]:
        acc = self.db.Get_user_security(username)
        if acc is None:
            return {"result": False, "message": "username is not exist"}
        
        # get salt from database
        salt = b64decode(acc[0])
        
        # hash password with salt
        h = SHA256.new()
        h.update(salt + password.encode() + salt)
        h.digest()
        enc_pwd = b64encode(h.digest()).decode()
        
        # check password
        if enc_pwd != acc[1]:
            return {"result": False, "message": "password is incorrect"}
             
        # update cookie
        cookie = b64encode(urandom(32)).decode()
        self.db.Update_cookie(username, cookie)
        self.db.Update_exp(username, int(time()) + COOKIE_LIFE_LIMIT)
             
        # return cookie
        return {"result": True, "cookie": cookie}
        
    def Login_cookie(self, cookie: str) -> dict[str, Union[str, bool]]:
        # verify cookie
        res = self.Verify_cookie(cookie)
        if res["result"] == False: return res
        
        # update new cookie exp
        new_exp = time() + COOKIE_LIFE_LIMIT
        self.db.Update_exp(cookie, new_exp)
        res["message"] = "cookie had been reseted"
        
        return res
        
    def Get_user_info(self, cookie: str) -> dict[str, Union[str, bool]]:
        if (res := self.Verify_cookie(cookie))["result"] == False:
            return res 
        
        info = self.db.Get_user_info(cookie)
        return {"result": True, "user_name": info[0], "money": info[1]}
    
    def Get_own_imgs(self, cookie: str, user_name: str) -> dict[str, Union[str, bool, list[tuple[str, int]]]]:
        if (res := self.Verify_cookie(cookie))["result"] == False:
            return res

        imgs_name = self.db.Get_user_owned(user_name)
        if imgs_name is None:
            return {"result": False, "message": "username does not exist"}
        return {"result": True, "imgs_name": imgs_name}
    
    def Get_purchase_imgs(self, cookie: str) -> dict[str, Union[str, bool, list[tuple[str, int, str]]]]:
        if (res := self.Verify_cookie(cookie))["result"] == False:
            return res

        imgs_name = self.db.Get_user_purchased(cookie)
        if imgs_name is None:
            return {"result": False, "message": "username does not exist"}
        return {"result": True, "imgs_name": imgs_name}
    
    def Get_user_key(self, owner: str) -> bytes:
        enc_key, nonce, tag = (b64decode(i) for i in self.db.Get_user_key(owner))
        cipher = AES.new(self.db_key, AES.MODE_GCM, nonce=nonce)
        cipher.update(owner.encode())
        return cipher.decrypt_and_verify(enc_key, tag)
    
    def Upload_img(self, cookie: str, img: bytes, img_name: str, cost: int) -> dict[str, Union[str, bool]]:
        if (res := self.Verify_cookie(cookie))["result"] == False:
            return res 

        user_name = self.db.Get_user_info(cookie)[0]
        if self.db.Check_image_owned(img_name, user_name):
            return {"result": False, "message": "img has already existed"}

        # check cost value
        if cost < 0:
            return {"result": False, "message": "cost need to be possitive"}
        
        # encrypt img
        enc = EncryptImg(user_name.encode(), img_name.encode(), self.Get_user_key(user_name))
        enc.Run(img)
        res = enc.Get_result()
        
        # save cipher img
        img_info = (img_name, res["cipher_img"], res["nonce"], res["tag"], user_name, cost)
        self.db.Add_image(img_info)
        return {"result": True, "img_name": img_name, "message": "img upload successfully"}
        
    def Get_image(self, cookie: str, owner: str, img_name: str) -> dict[str, Union[bool, str, bytes]]:
        if (res := self.Verify_cookie(cookie))["result"] == False:
            return res 

        # verify img owned or purchased
        buyer = self.db.Get_user_info(cookie)[0]
        
        if not (buyer == owner and self.db.Check_image_owned(img_name, owner) or \
                self.db.Check_image_purchased(buyer, img_name, owner)):
            return {"result": False, "message": "user doesn't have access permission or image doesn't exist"}
        
        cipher_img, nonce, tag = self.db.Get_image(img_name, owner)
        key = b64encode(self.Get_user_key(owner)).decode()
        
        dec = DecryptImg(owner, img_name, key, nonce)
        dec.Run(cipher_img, tag)
        res = dec.Get_img()
        
        res["result"] = True
        return res
            
    def Buy_img(self, cookie: str, owner: str, img_name: str):
        if (res := self.Verify_cookie(cookie))["result"] == False:
            return res 
        buyer, buyer_money = self.db.Get_user_info(cookie)
        cost = self.db.image_table.Get_cost(img_name, owner)
        if cost is None:
            return {"result": False, "message": "Image does not exist"}
        cost = cost[0]
        
        # check image had already been purchased
        if self.db.Check_image_purchased(buyer, img_name, owner) or owner == buyer:
            return {"result": False, "message": "Image had already been purchased or owned"}

        if buyer_money < cost:
            return {"result": False, "message": f"{buyer} doesn't have enough money to process"}
        
        # add purchase to buyer table and update money
        receipt = (buyer, img_name, owner, cost)
        self.db.buyer_table.Add_purchase(receipt)
        self.db.user_table.Update_money(buyer, -cost)
        self.db.user_table.Update_money(owner, cost)
        
        return {"result": True, "message": f"Success in purchase {img_name} owned by {owner}"}
        
    def Verify_cookie(self, cookie: str) -> dict[str, str]:
        exp = self.db.Get_cookie_exp(cookie)
        if exp is None: return {"result": False, "message": "Invalid cookie request"}
        if int(time()) > exp[0]: return {"result": False, "message": "Cookie is expired"}
        return {"result": True, 'message': ''}
        
        
    def Enc_database_key(self, password: str, key: bytes = None) -> dict[str, str]:
        salt = urandom(16)
        header = urandom(16)
        key = urandom(16) if key is None else key
        
        h = SHA256.new()
        h.update(salt + password.encode())
        password = h.digest()[:16]
        
        cipher = AES.new(password, AES.MODE_GCM)
        cipher.update(header)
        enc_key, tag = cipher.encrypt_and_digest(key)
        
        json_k = ['salt', 'nonce', 'header', 'enc_key', 'tag' ]
        json_v = [b64encode(x).decode() for x in [salt, cipher.nonce, header, enc_key, tag]]
        return dict(zip(json_k, json_v))
        
    def Dec_database_key(self, config: dict[str, str], password: str) -> bytes:
        salt = b64decode(config["salt"])
        nonce = b64decode(config["nonce"])
        tag = b64decode(config["tag"])
        header = b64decode(config["header"])
        enc_key = b64decode(config["enc_key"])
        
        h = SHA256.new()
        h.update(salt + password.encode())
        password = h.digest()[:16]
        
        cipher = AES.new(password, AES.MODE_GCM, nonce=nonce)
        cipher.update(header)
        
        try:
            return cipher.decrypt_and_verify(enc_key, tag)
        except ValueError:
            return bytes()
        
    def Change_database_password(self, old_password: str, new_password: str) -> dict[str, Union[str, bool]]:
        with open(DATABASE_KEY_FILE, 'r') as f:
            config = loads(f.read())
        
        if not (key := self.Dec_database_key(config, old_password)):
            return {"result": False, "message": "incorrect password"}
        
        new_config = self.Enc_database_key(new_password, key)
        with open(DATABASE_KEY_FILE, 'w') as f:
            dump(new_config, f, indent=6)
        return {"result": True, "message": "change password success"}
        
    def Load_database_key(self, password: str, config: dict[str, str] = None) -> dict[str, Union[str, bool]]:
        if config is None:
            with open(DATABASE_KEY_FILE, 'r') as f:
                config = loads(f.read())
        
        if (key := self.Dec_database_key(config, password)):
            self.db_key = key
            return {"result": True, "message": "load key success"}
        return {"result": False, "message": "incorrect password"}
    
    def Renew_database_key(self, password: str):
        new_config = self.Enc_database_key(password)
        with open(DATABASE_KEY_FILE, 'w') as f:
            dump(new_config, f, indent=6)
        return {"result": True, "message": "Warning: old images were encrypted with old key cant be decrypted with new key."}    
        
    