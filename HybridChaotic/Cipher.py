from HybridChaotic.Encrypt import EncryptImg
from HybridChaotic.Decrypt import DecryptImg
from Crypto.Util.number import getPrime
from random import uniform, random
import numpy as np

class Cipher:
	def __init__(self, p = None, q = None, l = None, x = None, len_mantissa = 3) -> None:
		self.p = p if p is not None else getPrime(256)
		self.q = q if q is not None else getPrime(256)
		self.l = l if l is not None else uniform(3.52, 4)
		self.x = x if x is not None else random()
		self.len_mantissa = len_mantissa

	def get_init_value(self) -> tuple[int, int, int, int]:
		return p, q, l, x

	def Encrypt(self, img: np.ndarray) -> np.ndarray:
		enc = EncryptImg(self.p, self.q, self.l, self.x, self.len_mantissa)
		return enc.Run(img)

	def Decrypt(self, img: np.ndarray) -> np.ndarray:
		dec = DecryptImg(self.p, self.q, self.l, self.x, self.len_mantissa)
		return dec.Run(img)
