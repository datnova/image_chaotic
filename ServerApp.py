from DataBase import DataBase
from Crypto.Hash import SHA256
from os import urandom
from base64 import b64encode, b64decode
from time import time
from CipherImg.Decrypt import DecryptImg
from CipherImg.Encrypt import EncryptImg

COOKIE_LIFE_LIMIT = 3600 * 24

class ServerApp:
    def __init__(self, database_dir: str):
        self.db = DataBase(database_dir)
    
    def Create_user(self, username: str, password: str) -> dict[str, str | bool]:
        if not (8 <= len(username) <= 24):
            return {"result": False, "message": "invalid username length"}
        
        if not(8 <= len(password) <= 24):
            return {"result": False, "message": "invalid password length"}

        # generate random salt
        salt = urandom(8)

        # hash password with salt
        h = SHA256.new()
        h.update(password.encode() + salt)
        
        # convert to base64
        salt = b64encode(salt).decode()
        enc_pwd = b64encode(h.digest()).decode()
        
        # get new cookie and exp time
        cookie = b64encode(urandom(32)).decode()
        exp = int(time()) + COOKIE_LIFE_LIMIT
        
        # add to database
        result = self.db.Create_user(username, enc_pwd, salt, cookie, exp)
        if result == False:
            return {"result": False, "message": "Username has already been taken"}

        return {"result": True, "message": "create user success"}
    
    def Login(self, username: str, password: str) -> dict[str, str | bool]:
        acc = self.db.Get_user_security(username)
        if acc is None:
            return {"result": False, "message": "username is not exist"}
        
        # get salt from database
        salt = b64decode(acc[0])
        
        # hash password with salt
        h = SHA256.new()
        h.update(password.encode() + salt)
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
        
    def Login_cookie(self, cookie: str) -> dict[str, str | bool]:
        # verify cookie
        res = self.Verify_cookie(cookie)
        if res["result"] == False: return res
        
        # update new cookie exp
        new_exp = time() + COOKIE_LIFE_LIMIT
        self.db.Update_exp(cookie, new_exp)
        res["message"] = "cookie had been reseted"
        
        return res
        
    def Get_user_info(self, cookie: str) -> dict[str, str | bool]:
        if (res := self.Verify_cookie(cookie))["result"] == False:
            return res 
        
        info = self.db.Get_user_info(cookie)
        return {"result": True, "user_name": info[0], "money": info[1]}
    
    def Get_own_img(self, cookie: str, user_name: str) -> dict[str, str | bool]:
        if (res := self.Verify_cookie(cookie))["result"] == False:
            return res
        
        imgs_name = self.db.Get_user_own(user_name)
        return {"result": True, "imgs_name": imgs_name}
    
    def Upload_img(self, cookie: str, img: bytes, img_name: str, cost: int) -> dict[str, str | bool]:
        if (res := self.Verify_cookie(cookie))["result"] == False:
            return res 

        # check cost value
        if cost < 0:
            return {"result": False, "message": "cost need to be possitive"}
        
        # encrypt img
        user_name = self.db.Get_user_info(cookie)[0]
        enc = EncryptImg(user_name.encode(), img_name.encode())
        enc.Run(img)
        res = enc.Get_result()
        key = enc.Get_key()
        
        # save cipher img
        result = self.db.Add_image(img_name, res['cipher_img'], key, res["nonce"], res["tag"], user_name, cost)
        if result == False:
            return {"result": False, "message": "img is already existed"}

        return {"result": True, "img_name": img_name, "message": "img upload successfully"}
        
    def Get_image(self, cookie: str, owner: str, img_name: str) -> dict[str, str | bytes]:
        if (res := self.Verify_cookie(cookie))["result"] == False:
            return res 

        # verify img owner or buyer
        if not (self.db.Get_user_info(cookie)[0] == owner or \
                self.Verify_buy_img(cookie, owner, img_name)):
            return {"result": False, "message": "user doesn't have access permission or image doesn't exist"}
    
        # verify img
        img_info = self.db.Get_image(owner, img_name)
        if img_info is None: 
            return {"result": False, "message": "image doesn't exist"}
        
        img_name = img_info[0].encode()
        cipher_img = b64decode(img_info[1])
        key = b64decode(img_info[2])
        nonce = b64decode(img_info[3])
        tag = b64decode(img_info[4])
        owner = owner.encode()
        
        dec = DecryptImg(owner, img_name, key, nonce)
        dec.Run(cipher_img, tag)
        res = dec.Get_img()
        
        res["result"] = True
        return res
            
    def Verify_buy_img(self, cookie: str, owner: str, img_name: str) -> bool:
        if (img_name, owner) in self.Get_user_buy(cookie):
            return True
        return False    
        
    def Buy_img(self, cookie: str, owner: str, img_name: str):
        if (res := self.Verify_cookie(cookie))["result"] == False:
            return res 
        
        if self.db.Buy_img(cookie, owner, img_name):
            return {"result": True, "message": f"successful in purchase {img_name}"}
        return {"result": False, "message": "failed to purchase {img_name}"}
        
    def Verify_cookie(self, cookie: str) -> dict[str, str]:
        exp = self.db.Get_cookie_exp(cookie)
        if exp is None: return {"result": False, "message": "Invalid cookie request"}
        if int(time()) > exp[0]: return {"result": False, "message": "Cookie is expired"}
        return {"result": True, 'message': ''}
        
    