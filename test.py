#coding=utf-8
import time
import mygame
from pygame.locals import *
from Player import *
import Players
import Mapper
import Obj
from sys import exit

mygame.init()
screen = mygame.screen

player = Player()
player.moveto((3, 89))
players = Players.Players(1, [player])

mp = Mapper.Mapper()
mp.load("./data/map/jungle.tmx")
mp.set_viewer(player)
Obj.Obj.mapper = mp

screen.set_mapper(mp)
screen.set_viewer(player)

default_font = "arial"
font = mygame.font.SysFont(default_font, 20)


cntClock = 0
cntFrame = 0
cntNetwork = 0
lastClock = time.clock() * 1000
NowFPS = 0

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
    mp.update(intervalClock)
    screen.scroll()

    screen.fill((0, 0, 0))
    mp.draw(screen)
    player.draw(screen)

    text_surface = font.render(u"FPS: %3.f" % NowFPS, True, (255, 0, 0))
    screen.blit_fix(text_surface, (0, 0))
    mygame.display.update()

    cntClock += intervalClock
    cntFrame += 1
    if cntClock >= 1000:
        fps = cntFrame * 1000.0 / cntClock
        NowFPS = fps
        cntClock = 0
        cntFrame = 0
    
