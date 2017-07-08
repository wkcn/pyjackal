#coding=utf-8
from pygame.locals import *
import pygame
import ScreenBox
from scipy.misc import imread, imsave
import numpy as np

class image:
    resource = {}
    @staticmethod
    def load(filename):
        if filename not in image.resource:
            #image.resource[filename] = pygame.image.load(filename).convert_alpha() 
            im = pygame.image.load(filename)#.convert_alpha() 
            w, h = im.get_size()
            tw = int(w * r)
            th = int(h * r)
            image.resource[filename] = pygame.transform.smoothscale(im, (tw, th)).convert_alpha()
        return image.resource[filename]

class FakeMixerMusic:
    def load(self, name):
        pass
    def play(self, times = 0):
        pass
class FakeMixer:
    music = FakeMixerMusic()
    def init(self):
        pass
    def set_num_channels(self, w):
        pass
    def get_num_channels(self):
        return 0
    class CSound:
        def play(self):
            pass
    def Sound(self, name):
        return FakeMixer.CSound()

w, h = 256, 224
r = ScreenBox.ScreenBox.RATIO
tw = int(w * r)
th = int(h * r)
origin_screen_size = (w, h)
target_screen_size = (tw, th)
screen = None
screenNow = None
def init():
    global screen, screenNow
    pygame.init()
    screen_size = origin_screen_size
    screenNow = ScreenBox.ScreenBox(pygame.display.set_mode(target_screen_size, DOUBLEBUF, 32))
    #screenNow = ScreenBox.ScreenBox(pygame.display.set_mode(screen_size, DOUBLEBUF | FULLSCREEN, 32))
    #screen = pygame.Surface(origin_screen_size, flags=SRCALPHA, depth=32)
    screen = screenNow

    pygame.display.set_caption("Jackal")

class display:
    @staticmethod
    def update(win = None):
        if win == None:
            pygame.display.update()
            return
        r = ScreenBox.ScreenBox.RATIO
        nwin = [int(round(t * r)) for t in win]
        pygame.display.update(nwin)

sub_resource = {}
def load_sub_img(filename, siz):
    f, d = siz
    if filename not in sub_resource:
        im = pygame.image.load(filename) 
        pw, ph = im.get_size()
        w = pw // f
        h = ph // d
        ra = ScreenBox.ScreenBox.RATIO
        tw = int(w * ra)
        th = int(h * ra)
        #mask = [[pygame.mask.from_surface(im.subsurface((w * c, h * r), (w, h))) for c in range(f)] for r in range(d)]
        try:
            tex = [[pygame.transform.smoothscale(im.subsurface((w * c, h * r), (w,h)), (tw, th)).convert_alpha() for c in range(f)] for r in range(d)]
        except:
            tex = [[pygame.transform.scale(im.subsurface((w * c, h * r), (w,h)), (tw, th)).convert_alpha() for c in range(f)] for r in range(d)]
        sub_resource[filename] = (tex, (w,h))
    return sub_resource[filename]

sub_mask = {}
def load_sub_mask(filename, siz):
    f, d = siz
    if filename not in sub_mask:
        im = imread(filename)
        ph, pw, t = im.shape
        w = pw // f
        h = ph // d
        if t < 4:
            b = np.ones((w,h)).astype(np.bool)
        else:
            b = (im[:,:,3] != 0)
        sub_mask[filename] = [[b[(r*h):(r+1)*h, (c*w):(c+1)*w] for c in range(f)] for r in range(d)] 
    return sub_mask[filename]

grid_resource = {}
def load_grid_img(filename, siz):
    w, h = siz
    if filename not in grid_resource:
        im = pygame.image.load(filename) 
        pw, ph = im.get_size()
        f = pw // w
        d = ph // h
        ra = ScreenBox.ScreenBox.RATIO
        tw = int(w * ra)
        th = int(h * ra)
        #color = (255,162,0)
        #mask = [[pygame.mask.from_threshold(im.subsurface((w * c, h * r), (w, h)), color) for c in range(f)] for r in range(d)]

        '''
        mask = mask[4][5]
        siz = mask.get_size()
        for y in range(siz[1]):
            for x in range(siz[0]):
                print ((mask.get_at((x,y)))),
            print "" 
        fewaf
        '''
        try:
            tex = [[pygame.transform.smoothscale(im.subsurface((w * c, h * r), (w,h)), (tw, th)).convert_alpha() for c in range(f)] for r in range(d)]
        except:
            tex = [[pygame.transform.scale(im.subsurface((w * c, h * r), (w,h)), (tw, th)).convert_alpha() for c in range(f)] for r in range(d)]
        grid_resource[filename] = (tex, (f,d))
    return grid_resource[filename]

grid_mask = {}
def load_grid_mask(filename, siz, colors = []):
    w, h = siz
    if filename not in grid_mask:
        im = imread(filename)
        ph, pw, t = im.shape
        f = pw // w
        d = ph // h
        if t < 4:
            b = np.ones((w,h)).astype(np.bool)
        else:
            b = (im[:,:,3] != 0)
        for color in colors:
            bm = (im[:,:,0] == color[0]) & (im[:,:,1] == color[1]) & (im[:,:,2] == color[2])
            b &= (~bm)
        grid_mask[filename] = [[b[(r*h):(r+1)*h, (c*w):(c+1)*w] for c in range(f)] for r in range(d)] 
    return grid_mask[filename]


def smoothscale(im, siz):
    r = ScreenBox.ScreenBox.RATIO
    tw = int(siz[0] * r)
    th = int(siz[1] * r)
    return pygame.transform.smoothscale(im, (tw, th)).convert_alpha()

try:
    pygame.mixer.init()
    pygame.mixer.set_num_channels(pygame.mixer.get_num_channels())
    mixer = pygame.mixer
except:
    mixer = FakeMixer()

#display = pygame.display
time = pygame.time
font = pygame.font
transform = pygame.transform
event = pygame.event
key = pygame.key
