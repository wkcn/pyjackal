import mygame
from pygame.locals import *

PlayersControl = [None for _ in range(2)]
DOWN, LEFT, RIGHT, UP, ROCKET, SHOT = range(6)
PlayersControl[0] = []
PlayersControl[1] = [
        (K_DOWN, K_LEFT, K_RIGHT, K_UP, K_x, K_z)
        ]

class Players:
    def __init__(self, playersNum, players):
        self.playersNum = playersNum
        self.control = PlayersControl[playersNum]
        self.players = []
        for i in range(playersNum):
            self.players.append(players[i])

    def update(self):
        keys = mygame.key.get_pressed()
        for i in range(self.playersNum):
            p = self.players[i]
            u = [keys[k] for k in self.control[i]]
            if u[ROCKET]:
                p.rocket()
            if u[SHOT]:
                p.shot()
            if u[UP]:
                if u[LEFT]:
                    p.go_dir(1)
                    continue
                if u[RIGHT]:
                    p.go_dir(7)
                    continue
                p.go_dir(0)
                continue
            if u[DOWN]:
                if u[LEFT]:
                    p.go_dir(3)
                    continue
                if u[RIGHT]:
                    p.go_dir(5)
                    continue
                p.go_dir(4)
                continue
            if u[LEFT]:
                p.go_dir(2)
                continue
            if u[RIGHT]:
                p.go_dir(6)
                continue
