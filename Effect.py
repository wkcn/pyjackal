#coding=utf-8
from Obj import *

class Effect(Obj):
    def __init__(self, filename, num_dir = 1):
        Obj.__init__(self, filename, num_dir)
        self.dead = False
