#coding=utf-8
from scipy.misc import imread, imsave
import matplotlib.pyplot as plt
import numpy as np

heady = 60

def read_stage(mid):
    pic = imread("Jackal-Stage%d.png" % mid)[heady:-8,:,:]
    rows, cols, tu = pic.shape
    gr = rows // 32
    gc = cols // 32
    if gr * 32 != rows or gc * 32 != cols:
        raise Exception("Error Ratio", gr * 32, rows, gc * 32, cols)

read_stage(6)
