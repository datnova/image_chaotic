from HybridChaotic.Encrypt import EncryptImg
from HybridChaotic.Decrypt import DecryptImg
from Crypto.Util.number import getPrime
from random import uniform, random
import numpy as np

MIN_LAMBDA = 3.52
MAX_LAMBDA = 4
BIT_PRIME = 256

def Generate_key() -> tuple[int, int, float, float]:
	return tuple([						\
     	getPrime(BIT_PRIME),			\
		getPrime(BIT_PRIME),			\
		uniform(MIN_LAMBDA, MAX_LAMBDA),\
		random()])

class Cipher:
	def __init__(self, p = None, q = None, l = None, x = None, len_mantissa = 5) -> None:
		temp_key = Generate_key()
		self.p = p if p is not None else temp_key[0]
		self.q = q if q is not None else temp_key[1]
		self.l = l if l is not None else temp_key[2]
		self.x = x if x is not None else temp_key[3]
		self.len_mantissa = len_mantissa

	def Get_init_value(self) -> tuple[int, int, int, int]:
		return self.p, self.q, self.l, self.x

	def Encrypt(self, img: np.ndarray) -> np.ndarray:
		enc = EncryptImg(self.p, self.q, self.l, self.x, self.len_mantissa)
		return enc.Run(img)

	def Decrypt(self, img: np.ndarray) -> np.ndarray:
		dec = DecryptImg(self.p, self.q, self.l, self.x, self.len_mantissa)
		return dec.Run(img)
