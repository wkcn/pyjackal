#coding=utf-8
import mygame
import pygame
import math
import numpy as np
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

TURNING_CLOCK = 50
SHAKING_CLOCK = 60

class Obj(object):
    mapper = None
    def __init__(self, filename, pos):
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
        self.tex, self.mask, self.pic_size = self.load_pic8(filename)
        #print_bits(self.mask[0])
        #print ("====")
        self.moveto(pos)
    def load_pic8(self, filename):
        tex, pic_size = mygame.load_sub_img(filename, (4, 2))
        masko = mygame.load_sub_mask(filename, (4, 2))
        res = [None for _ in range(8)]
        mask = [None for _ in range(8)]
        for r in range(2):
            for c in range(4):
                d = DIRS8[r][c]
                res[d] = tex[r][c]
                mask[d] = masko[r][c]
        return res, mask, pic_size
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

    def moveto(self, pos):
        self.realPos[0] = self.tarPos[0] = pos[0] * 32
        self.realPos[1] = self.tarPos[1] = pos[1] * 32
    @property
    def realx(self):
        return self.realPos[0]
    @property
    def realy(self):
        return self.realPos[1]
    @realx.setter
    def realx(self, value):
        self.realPos[0] = value
    @realy.setter
    def realy(self, value):
        self.realPos[1] = value
    def running(self):
        return self.realPos[0] != self.tarPos[0] or self.realPos[1] != self.tarPos[1]
    def througed(self, v):
        tx = int(self.tarPos[0] + v[0])
        ty = int(self.tarPos[1] + v[1])
        ix = (tx) // 32
        iy = (ty) // 32
        # 9 GRIDS
        gr = np.zeros((32 * 3, 32 * 3)).astype(np.bool)
        mm = np.zeros((32 * 3, 32 * 3)).astype(np.bool)
        for ax in [-1,0,1]:
            nx = ix + ax
            if nx < 0 or nx >= Obj.mapper.width:
                continue
            for ay in [-1,0,1]:
                ny = iy + ay
                if ny < 0 or ny >= Obj.mapper.height:
                    continue
                tid = Obj.mapper.tids[ny][nx] 
                gr[(ay+1)*32:(ay+2)*32, (ax+1)*32:(ax+2)*32] = Obj.mapper.mask[tid]
        dx = tx - ix * 32
        dy = ty - iy * 32
        w, h = self.pic_size
        min_x = (dx + 32)
        min_y = (dy + 32)
        max_x = min(min_x + w, 32 * 3)
        max_y = min(min_y + h, 32 * 3)
        mx = max_x - min_x
        my = max_y - min_y
        bb = gr[min_y:max_y, min_x:max_x] & self.mask[self.dir][:my, :mx]
        nb = np.sum(bb)
        return nb < 16

    def go_dir(self, d):
        if self.dir != d:
            self.change_dir(d)
        else:
            # moveto
            self.want_to_move = True
            if not self.running():
                bv = DIRS8_V[self.dir]
                if self.througed(bv):
                    self.tarPos[0] += bv[0]
                    self.tarPos[1] += bv[1]
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
