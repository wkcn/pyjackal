#coding=utf-8
import mygame
from Obj import *
from Bullet import *

CLOCK_PER_SHOT = 150 
SHOT_V = 6.5

class Player(Obj):
    def __init__(self):
        Obj.__init__(self, "./res/pic/jackal.png")
        self.shot_clock = 0
    def rocket(self):
        pass
    def shot(self):
        if self.shot_clock < CLOCK_PER_SHOT:
            return
        bl = Bullet()

        bl.real_moveto((self.center_x, self.center_y))
        bl.dir = 0
        bl.v = SHOT_V

        Obj.mapper.effects.append(bl)
        self.shot_clock = 0
    def update(self, clock):
        Obj.update(self, clock)
        self.shot_clock += clock
