#coding=utf-8
import mygame
import math
from Defines import *

'''
107
2 6
345

1076
2345
'''

DIRS8 = [[1,0,7,6], [2,3,4,5]]

DIRS_C = 1.0
DIRS_D = 0.8
DIRS8_V = [(0.0, -DIRS_C), (-DIRS_D, -DIRS_D), (-DIRS_C, 0.0), (-DIRS_D, DIRS_D), (0.0, DIRS_C), (DIRS_D, DIRS_D), (DIRS_C, 0.0), (DIRS_D, -DIRS_D)]

TURNING_CLOCK = 40
SHAKING_CLOCK = 60

class Obj:
    def __init__(self):
        self.realPos = [0, 0]
        self.tarPos = [0, 0]
        self.realy_shake = 0
        self.dir = 1
        self.turning_clock = 0 
        self.moving_clock = 0
        self.shaking_clock = 0
        self.v = 2.0
        self.can_move = True
        self.want_to_move = False
    def load_pic8(self, filename):
        tex, pic_size = mygame.load_sub_img(filename, (4, 2))
        res = [None for _ in range(8)]
        for r in range(2):
            for c in range(4):
                res[DIRS8[r][c]] = tex[r][c]
        return res, pic_size
    def draw(self, screen):
        screen.blit(self.tex[self.dir], (self.realx, self.realy + self.realy_shake)) 
    def update(self, clock):
        self.turning_clock += clock
        not_came = False
        for i in range(2):
            if (self.realPos[i] != self.tarPos[i]):
                not_came = True
                if (self.realPos[i] < self.tarPos[i]):
                    self.realPos[i] += self.v * Normalize(clock)
                    if self.realPos[i] > self.tarPos[i]:
                        self.realPos[i] = self.tarPos[i]
                else:
                    self.realPos[i] -= self.v * Normalize(clock)
                    if self.realPos[i] < self.tarPos[i]:
                        self.realPos[i] = self.tarPos[i]
        if self.want_to_move or not_came:
            self.shaking_clock += clock
            if self.shaking_clock > SHAKING_CLOCK:
                self.realy_shake = 1 - self.realy_shake
                self.shaking_clock = 0
        self.want_to_move = False

    @property
    def realx(self):
        return self.realPos[0]
    @property
    def realy(self):
        return self.realPos[1]
    def running(self):
        return self.realPos[0] != self.tarPos[0] or self.realPos[1] != self.tarPos[1]
    def go_dir(self, d):
        if self.dir != d:
            self.change_dir(d)
        else:
            # moveto
            if not self.running():
                bv = DIRS8_V[self.dir]
                self.tarPos[0] += bv[0]
                self.tarPos[1] += bv[1]
            self.want_to_move = True
    def change_dir(self, d):
        if self.turning_clock < TURNING_CLOCK:
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
