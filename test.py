#coding=utf-8
import time
import mygame
from pygame.locals import *
from Player import *
import Players
import Mapper
from sys import exit

mygame.init()
screen = mygame.screen

player = Player()
players = Players.Players(1, [player])

mp = Mapper.Mapper()
mp.load("./data/map/jungle.tmx")

screen.set_mapper(mp)
screen.set_viewer(player)

lastClock = time.clock() * 1000
while 1:
    for event in mygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                exit(0)
          

    nowClock = time.clock() * 1000
    intervalClock = nowClock - lastClock
    lastClock = nowClock

    players.update()
    player.update(intervalClock)
    screen.scroll()

    screen.fill((0, 0, 0))
    mp.draw(screen)
    player.draw(screen)
    mygame.display.update()
