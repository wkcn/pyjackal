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
        self.dir = 1
        self.turning_clock = 0
    def load_pic8(self, filename):
        tex, pic_size = mygame.load_sub_img(filename, (4, 2))
        res = [None for _ in range(8)]
        for r in range(2):
            for c in range(4):
                res[DIRS8[r][c]] = tex[r][c]
        return res, pic_size
    def draw(self, screen):
        screen.blit(self.tex[self.dir], (10, 10)) 
    def update(self, clock):
        self.turning_clock += clock
    @property
    def realx(self):
        return self.realPos[0]
    @property
    def realy(self):
        return self.realPos[1]
    def change_dir(self, d):
        if self.turning_clock < 40:
            return
        diff = d - self.dir
        if diff == 0:
            return
        self.turning_clock = 0
        # special
        if (self.dir == 2 and d == 6) or (self.dir == 4 and d == 0):
            self.dir = (self.dir + 7) % 8
            return
        if diff < 0:
            diff += 8
        if diff <= 4:
            self.dir = (self.dir + 1) % 8
        else:
            self.dir = (self.dir + 7) % 8
