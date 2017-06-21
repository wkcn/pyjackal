#coding=utf-8
import time
import mygame
from pygame.locals import *
from Player import *

mygame.init()
screen = mygame.screen

player = Player()
screen.set_viewer(player)

lastClock = time.clock() * 1000
while 1:
    for event in mygame.event.get():
        if event.type == QUIT:
            exit()

    nowClock = time.clock() * 1000
    intervalClock = nowClock - lastClock
    lastClock = nowClock

    player.update(intervalClock)
    screen.fill((0, 0, 0))
    player.draw(screen)
    mygame.display.update()
