#coding=utf-8
import time
import mygame
from pygame.locals import *
from Player import *
import Players
import Mapper

mygame.init()
screen = mygame.screen

player = Player()
screen.set_viewer(player)
players = Players.Players(1, [player])
mp = Mapper.Mapper()
mp.load("./data/map/jungle.tmx")

lastClock = time.clock() * 1000
while 1:
    for event in mygame.event.get():
        if event.type == QUIT:
            exit()

    nowClock = time.clock() * 1000
    intervalClock = nowClock - lastClock
    lastClock = nowClock

    players.update()
    player.update(intervalClock)

    screen.fill((0, 0, 0))
    mp.draw(screen)
    player.draw(screen)
    mygame.display.update()
