#coding=utf-8
import mygame
from Obj import *

class Player(Obj):
    def __init__(self):
        Obj.__init__(self)
        self.tex, self.pic_size = self.load_pic8("./res/pic/jackal.png")
    def rocket(self):
        pass
    def shot(self):
        pass
