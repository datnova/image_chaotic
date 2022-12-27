from requests import post, get, exceptions
from os.path import exists, basename
from os import mkdir
from json import load

DEFAULT_URL_API = "http://127.0.0.1:8000/"
DEFAULT_SAVE_IMG_DIR = "%userprofile%\\Pictures\\CrypoImg\\"

class App:
    def __int__(self):
        self.cookie = None
        self.username = None
        self.current_search_name = None
    
    def Signup(self, username: str, password: str, repassword: str) -> dict[str, str | bool]:
        if password != repassword:
            return {
                "result": False, 
                "message": "retype password is different from password, please check again!"
            }
        
        url = DEFAULT_URL_API + "create_account"
        datas = {"username": username, "password": password}
        return post(url=url, data=datas).json()
        
    def Login(self, username: str, password: str) -> dict[str, str | bool]:
        url = DEFAULT_URL_API + "login"
        datas = {"username": username, "password": password}
        res = get(url=url, data=datas).json()
        self.cookie = res.pop("cookie", None)
        self.username = username
        return res
        
    def Upload_img(self, img_path: str, cost: int) -> dict[str, str | bool]:
        img_name = basename(img_path)
        url = DEFAULT_URL_API + f"upload/{img_name}/{cost}"
        img = {"img": open(img_path, "rb")}
        data = {"cookie": self.cookie}
        return post(url, data=data, files=img).json()
        
    def Download_img(self, img_name: str, file_path: str, owner: str = None) -> bool | dict[str, bool | str]:
        if not (img_name and owner):
            # return {"result": False, "message": "Please enter image's name and image's owner"}
            return False
        
        owner = self.username if owner is None else owner
        url = DEFAULT_URL_API + f"download/{owner}/{img_name}"
        data = {"cookie": self.cookie}
        r = get(url, data=data)
        
        if r.status_code != 200:
            return False

        try:
            if r.json()["result"] == False:
                return False
        except exceptions.JSONDecodeError:
            with open(file_path, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)

        return True
        
    def Search_owned_imgs(self, username: str = None) -> dict[str, bool | list[tuple[str, int, str]] | str]:
        username = self.username if username is None else username
        url = DEFAULT_URL_API + f"own_imgs/{username}"
        data = {"cookie": self.cookie}
        res = get(url, data=data).json()
        return res        
    
    def Get_user_info(self) -> dict[str, str | bool | int]:
        url = DEFAULT_URL_API + "user_info"
        data = {"cookie": self.cookie}
        res = get(url, data=data).json()
        return res  
    
    def Search_purchased_imgs(self) -> dict[str, bool | list[tuple[str, int, str]] | str]:
        url = DEFAULT_URL_API + f"purchase_imgs"
        data = {"cookie": self.cookie}
        res = get(url, data=data).json()
        return res        
        
    def Purchase_img(self, img_name: str, owner: str = None):
        owner = self.current_search_name if owner is None else owner
        url = DEFAULT_URL_API + f"buy_img/{owner}/{img_name}"
        data = {"cookie": self.cookie}
        return post(url, data=data).json()
        
