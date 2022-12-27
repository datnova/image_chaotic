from base64 import b64decode
from Crypto.Cipher import AES
from typing import Union

class DecryptImg:
    def __init__(self, user: str, img_name: str, key: str, nonce: str) -> None:
        # init value, input value in base64 except image name and user name
        self.key = b64decode(key)
        self.nonce = b64decode(nonce)
        self.user = user.encode()
        self.img_name = img_name.encode()
        self.img = None
        
        # init cipher
        self.cipher = AES.new(self.key, AES.MODE_GCM, nonce=self.nonce)
        self.cipher.update(self.user + self.img_name)
    
    def Run(self, cipher_img: str, tag: str) -> bool:
        # input cipher image and tag in base64
        try:
            cipher_img = b64decode(cipher_img)
            tag = b64decode(tag)
            self.img = self.cipher.decrypt_and_verify(cipher_img, tag)
            return True
        except (ValueError, KeyError):
            return False
        
    def Get_img(self) -> dict[str, Union[bytes, None]]:
        return {
            "owner": self.user, 
            "img_name": self.img_name, 
            "image": self.img
        }
        