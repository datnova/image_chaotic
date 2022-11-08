# Cipher image with hybrid chaotic
## Install requirments
$ pip install -r requirements.txt

## Cipher
```python
from HybridChaotic.Cipher import Cipher
import numpy as np

img = [[[1,  2,  3 ], [4,  5,  6 ], [7,  8,  9 ]],
       [[10, 11, 12], [13, 14, 15], [16, 17, 18]],
       [[19, 20, 21], [22, 23, 24], [25, 26, 27]]]

origin_img = np.array(img)

c = Cipher(3, 5, 3.52, 0.4)
enc_img = c.Encrypt(origin_img)
dec_img = c.Decrypt(enc_img)

assert np.array_equal(origin_img, dec_img)
```
