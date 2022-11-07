# image cipher with hybrid chaotic
## Encryption
'''
from Encryption import HybridChaotic
import numpy as np

img = [[[1,  2,  3 ], [4,  5,  6 ], [7,  8,  9 ]],
       [[10, 11, 12], [13, 14, 15], [16, 17, 18]],
       [[19, 20, 21], [22, 23, 24], [25, 26, 27]]]
img = np.array(img)

cipher = HybridChaotic(2, 3, 3.52, 0.76)
enc_img = cipher.run(img)
'''
