from base64 import b64encode
from Crypto.Cipher import AES

class DecryptImg:
    def __init__(self, user: bytes, img_name: bytes, key: bytes, nonce: bytes) -> None:
        # init value
        self.key = key 
        self.nonce = nonce
        self.user = user
        self.img_name = img_name
        self.img = None
        
        # init cipher
        self.cipher = AES.new(self.key, AES.MODE_GCM, nonce=self.nonce)
        self.cipher.update(self.user + self.img_name)
    
    def Run(self, cipher_img: bytes, tag: bytes) -> bool:
        try:
            self.img = self.cipher.decrypt_and_verify(cipher_img, tag)
            return True
        except (ValueError, KeyError):
            return False
        
    def Get_img(self) -> dict[str, str | bytes | None] | None:
        if self.img is None: 
            return None
        
        return {
            "owner": self.user.decode("utf-8"), 
            "img_name": self.img_name.decode("utf-8"), 
            "image": self.img
        }
        