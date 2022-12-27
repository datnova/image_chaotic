from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

class EncryptImg:
    def __init__(self, user: bytes, img_name: bytes, key = None) -> None:
        # init value, input value in bytes
        self.key = key if key is not None else get_random_bytes(16)
        self.nonce = get_random_bytes(12)
        self.user = user
        self.img_name = img_name
        self.cipher_img = None
        self.tag = None
        
        # init cipher
        self.cipher = AES.new(self.key, AES.MODE_GCM, nonce=self.nonce)
        self.cipher.update(self.user + self.img_name)
    
    def Run(self, img: bytes) -> None:
        self.cipher_img, self.tag = self.cipher.encrypt_and_digest(img)
        
    def Get_result(self) -> dict[str, str]: # return value in base64
        json_k = ['nonce', 'user', 'img_name', 'cipher_img', 'tag']
        json_v = [self.nonce, self.user, self.img_name, self.cipher_img, self.tag]
        json_v = map(lambda x: b64encode(x).decode('utf-8'), json_v)
        return dict(zip(json_k, json_v))

    def Get_key(self):
        return b64encode(self.key).decode("utf-8")

    def Reset(self) -> None:
        # reset value
        self.cipher_img = None
        self.tag = None
        
        # init cipher
        self.cipher = AES.new(self.key, AES.MODE_GCM, nonce=self.nonce)
        self.cipher.update(self.user + self.img_name)
    