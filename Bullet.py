#coding=utf-8
from Effect import *

class Bullet(Effect):
    def __init__(self):
        Effect.__init__(self, "./res/pic/effect/bullet_r.png", num_dir = 1)
        self.life = 300
        self.will_die = False
    def update(self, clock):
        Effect.update(self, clock)
        self.life -= clock
        if self.life < 0:
            if not self.will_die:
                self.load_tex("./res/pic/effect/bullet_d.png")
                self.will_die = True
            if self.life < -100:
                self.dead = True
        else:
            if not self.go_dir(self.dir):
                self.life = 0
