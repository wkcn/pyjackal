#coding=utf-8
from scipy.misc import imread, imsave
import matplotlib.pyplot as plt
import numpy as np

sx,sy = 10,25
w, h  = 32,32
fw, fh = 4,2
lw, lh = 1,1

pic = imread("NES - Jackal Top Gunner - Jackal Squad.png")
rows, cols, t = pic.shape
if t == 3:
    pic = np.dstack([pic, np.ones((rows, cols)) * 255])
print (pic.shape)
b = (pic[:,:,0] == 32) & (pic[:,:,1] == 200) & (pic[:,:,2] == 248)
pic[b, :] = 0

res = np.zeros((h * fh, w * fw, 4))
for r in range(fh):
    for c in range(fw): 
        tx = sx + (w + lw) * c
        ty = sy + (h + lh) * r
        tmp = pic[ty:ty+h, tx:tx+w, :]
        res[r*h:(r+1)*h, c*w:(c+1)*w, :] = tmp 

res /= 255.0
plt.imshow(res)
plt.show()
imsave("jackal.png", res)

