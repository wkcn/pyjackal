#coding=utf-8
import mygame

'''
107
2 6
345

1076
2345
'''

DIRS8 = [[1,0,7,6], [2,3,4,5]]

class Obj:
    def __init__(self):
        self.realPos = [0, 0]
    def load_pic8(self, filename):
        tex, pic_size = mygame.load_sub_img(filename, (4, 2))
        res = [None for _ in range(8)]
        for r in range(2):
            for c in range(4):
                res[DIRS8[r][c]] = tex[r][c]
        return res, pic_size
    @property
    def realx(self):
        return self.realPos[0]
    @property
    def realy(self):
        return self.realPos[1]
