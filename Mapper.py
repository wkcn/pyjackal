#coding=utf-8
import mygame
import pytmx 
from Defines import *

GROUND_COLORS = [(255,162,0), (198,113,0)]
class Mapper:
    def __init__(self):
        self.tex = []
        self.mask = [] # value is 1 if it's an obstacle
        self.mapping = dict()
        self.width = 0
        self.height = 0
        self.tids = None
        self.player = None # TODO: Multi Players
        self.effects = []
    def load(self, filename):
        print ("Loading Map: %s" % filename)
        self.tiled_map = pytmx.TiledMap(filename)
        self.load_map_tex(self.tiled_map)
        print ("Loading Map OK :-)")
    def load_map_tex(self, m):
        layer = self.tiled_map.layers[0]
        self.width = layer.width
        self.height = layer.height
        self.tids = [[0 for _ in range(layer.width)] for _ in range(layer.height)]
        for x, y, img in layer.tiles():
            name, pos, _ = img
            if (name, pos) in self.mapping:
                tid = self.mapping[(name, pos)]
            else:
                r = pos[1] // 32
                c = pos[0] // 32
                gim, siz = mygame.load_grid_img(name, (32, 32))
                gmask = mygame.load_grid_mask(name, (32, 32), GROUND_COLORS)
                tex = gim[r][c]
                mask = gmask[r][c]
                tid = len(self.tex)
                self.tex.append(tex)
                self.mask.append(mask)
        
                #print ("=====", (r,c))
                #print_bits(mask)

            self.tids[y][x] = tid
    def update(self, clock):
        new_effects = []
        for e in self.effects:
            e.update(clock)
            if not e.dead:
                new_effects.append(e)
        self.effects = new_effects
    def draw(self, screen):
        px = self.player.x
        py = self.player.y
        min_y = max(0, py - 8)
        max_y = min(self.height, py + 9)
        min_x = max(0, px - 8)
        max_x = min(self.width, px + 9)
        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                tid = self.tids[y][x]
                tex = self.tex[tid]
                screen.blit(tex, (x * 32, y * 32))
        for e in self.effects:
            e.draw(screen)
    def get_tex(self, img):
        return None
    def set_viewer(self, player):
        self.player = player

if __name__ == "__main__":
    mp = Mapper()
    mp.load("./data/map/jungle.tmx")
