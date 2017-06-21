#coding=utf-8
import mygame
from Obj import *

class Player(Obj):
    def __init__(self):
        Obj.__init__(self)
        self.tex, self.pic_size = self.load_pic8("./res/pic/jackal.png")
    def update(self, clock):
        pass
    def draw(self, screen):
        screen.blit(self.tex[0], (10, 10)) 
