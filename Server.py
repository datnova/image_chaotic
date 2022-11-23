from json import dump, load
from os import mkdir, walk
from os.path import exists, join
from pathlib import Path

from numpy import asarray
from PIL import Image

from HybridChaotic.Cipher import Cipher, Generate_key

KEYS_FILE = "keys.json"

class Server:
    def __init__(self, imgs_dir: str, keys_file: str, ip: str, port = 5555) -> None:
        self.imgs_dir = self.Check_imgs_locate(imgs_dir)
        self.keys = self.Load_keys(keys_file)
        self.ip = ip
        self.port = port
    
    ### check is imgs dir exist
    def Check_imgs_locate(self, imgs_dir: str) -> str:
        if not Path(imgs_dir).exists():
            raise NotADirectoryError(f"{imgs_dir} is not exist!")
        return imgs_dir
    
    ### load keys from json file
    def Load_keys(self, keys_file: str) -> dict[str, tuple[int, int, float, float]]:
        # if there is not init keys file exist
        if keys_file is None: return dict()
        
        # check is file exist
        if not exists(keys_file):
            raise FileExistsError(f"{keys_file} is not exist")

        # open and read keys
        with open(keys_file, 'r') as f:
            return load(f)
    
    ### save keys to file json
    def Save_keys(self) -> None:
        with open(KEYS_FILE, "w") as f:
            dump(self.keys, f)
        
    ### get cipher from user name and if not it will create one and save it
    def Get_user_cipher(self, user_name) -> Cipher:
        key = self.keys.get(user_name)
        if key is None:
            cipher = Cipher()
            # set new key for user
            self.keys[user_name] = cipher.Get_init_value()
            return cipher
        return Cipher(key[0], key[1], key[2], key[3])  
    
    ### save img to user folder
    def Save_img(self, user_name: str, imgs: list[set[str, Image.Image]]) -> None:
        # specify user folder
        self.Add_user(user_name)
        user_folder = join(self.imgs_dir, user_name)

        # save imgs to folder
        for img_name, img in imgs:
            # convert img to numpy array
            print(img_name)
            img = asarray(img)
            
            # encrypt array img
            cipher = self.Get_user_cipher(user_name)
            img = cipher.Encrypt(img)            
            
            # convert array back to img and save it
            img = Image.fromarray(img)
            img.save(join(user_folder, img_name))
    
    ### get all img locate from user folder
    def Get_imgs_name(self, user_name: str):
        # get user folder
        user_folder = join(self.imgs_dir, user_name)

        # check is folder exist and then return
        if not Path(user_folder).exists(): return list()
        return next(walk(user_folder), (None, None, []))[2]
    
    ### get img from user folder
    def Load_img(self, user_name: str) -> dict[str, Image.Image]:
        # get all imgs locate
        imgs_name = self.Get_imgs_name(user_name)
        user_folder = join(self.imgs_dir, user_name)

        # load imgs from folder and decrypt img
        res = dict()
        for img_name in imgs_name:
            # load img
            img = Image.open(join(user_folder, img_name))
            
            # convert img to numpy array
            img = asarray(img)
            
            # encrypt array img
            cipher = self.Get_user_cipher(user_name)
            img = cipher.Decrypt(img)            
            
            # convert array back to img and save it
            img = Image.fromarray(img)
            res[img_name] = img

        # return all decrypt imgs
        return res
    
    ### Add user
    def Add_user(self, user_name: str) -> None:
        # check is key existed
        if self.keys.get(user_name) is None:
            self.keys[user_name] = Generate_key()
        
        # create user folder
        user_folder = join(self.imgs_dir, user_name)
        try:
            mkdir(user_folder)
        except FileExistsError:
            print(f"User {user_name} is already existed")

