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
DIRS_D = math.sqrt(2.0) / 2.0
DIRS8_V = [(0.0, -DIRS_C), (-DIRS_D, -DIRS_D), (-DIRS_C, 0.0), (-DIRS_D, DIRS_D), (0.0, DIRS_C), (DIRS_D, DIRS_D), (DIRS_C, 0.0), (DIRS_D, -DIRS_D)]

TURNING_CLOCK = 70
SHAKING_CLOCK = 70

class Obj(object):
    mapper = None
    def __init__(self, filename, num_dir = 8):
        self.realPos = [0, 0]
        self.tarPos = [0, 0]
        self.realy_shake = 0
        self.dir = 1
        self.turning_clock = 0 
        self.moving_clock = 0
        self.shaking_clock = 0
        self.v = 0.6
        self.can_move = True
        self.want_to_move = False
        self.num_dir = num_dir
        self.load_tex(filename)
    def load_tex(self, filename):
        self.tex, self.mask, self.pic_size = self.load_pic(filename, self.num_dir)

    def load_pic(self, filename, dirnum):
        if dirnum == 8:
            grid = (2, 4)
        else:
            grid = (1, dirnum)
        tex, pic_size = mygame.load_sub_img(filename, grid)
        masko = mygame.load_sub_mask(filename, grid)
        res = [None for _ in range(dirnum)]
        mask = [None for _ in range(dirnum)]
        if dirnum == 8:
            for r in range(grid[0]):
                for c in range(grid[1]):
                    d = DIRS8[r][c]
                    res[d] = tex[r][c]
                    mask[d] = masko[r][c]
        else:
            d = 0
            for r in range(grid[0]):
                for c in range(grid[1]):
                    res[d] = tex[r][c]
                    mask[d] = masko[r][c]
                    d += 1
            res = res[:d] * (8 // d)
            mask = mask[:d] * (8 // d)
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
        rpos = (pos[0] * 32, pos[1] * 32)
        self.real_moveto(rpos)
    def real_moveto(self, rpos): 
        self.realPos[0] = self.tarPos[0] = rpos[0] - self.pic_size[0] // 2
        self.realPos[1] = self.tarPos[1] = rpos[1] - self.pic_size[1] // 2
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
    @property
    def center_x(self):
        return self.realx + self.pic_size[0] // 2
    @property
    def center_y(self):
        return self.realy + self.pic_size[1] // 2
    @property
    def x(self):
        return int(self.center_x // 32)
    @x.setter
    def x(self, value):
        self.tarPos[0] = value * 32 - self.pic_size[0] // 2
    @property
    def y(self):
        return int(self.center_y // 32)
    @y.setter
    def y(self, value):
        self.tarPos[1] = value * 32 - self.pic_size[1] // 2
    def running(self):
        return self.realPos[0] != self.tarPos[0] or self.realPos[1] != self.tarPos[1]
    def througed(self, v):
        # next center position
        tx = int(self.center_x + v[0])
        ty = int(self.center_y + v[1])
        ix = (tx) // 32
        iy = (ty) // 32
        # offset
        dx = tx - ix * 32
        dy = ty - iy * 32
        # 9 GRIDS
        gr = np.zeros((32 * 3, 32 * 3)).astype(np.bool) # ground mask
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
        w, h = self.pic_size
        # left top position
        rx = dx - w // 2 + 32
        ry = dy - h // 2 + 32
        # ignored parts
        qx = max(0, -rx)
        qy = max(0, -ry)
        # bounding border
        min_x = max(0, rx)
        min_y = max(0, ry)
        max_x = min(rx + w, 32 * 3)
        max_y = min(ry + h, 32 * 3)
        mx = max_x - min_x
        my = max_y - min_y
        bb = gr[min_y:max_y, min_x:max_x] & self.mask[self.dir][qy:my + qy, qx:mx + qx]
        nb = np.sum(bb & mygame.get_dir_mask(self.dir, (w,h))[qy:my + qy, qx:mx + qx])
        return nb < 8

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
                    return True
                else:
                    return False
        return True 
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
