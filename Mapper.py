#coding=utf-8
import mygame
import pytmx 

class Mapper:
    def __init__(self):
        self.tex = []
        self.mapping = dict()
        self.width = 0
        self.height = 0
    def load(self, filename):
        print ("Loading Map: %s" % filename)
        self.tiled_map = pytmx.TiledMap(filename)
        self.load_map_tex(self.tiled_map)
        print ("Loading Map OK :-)")
    def load_map_tex(self, m):
        layer = self.tiled_map.layers[0]
        self.width = layer.width
        self.height = layer.height
        self.tids = [[0] * layer.width] * layer.height
        for x, y, img in layer.tiles():
            name, pos, _ = img
            if (name, pos) in self.mapping:
                tid = self.mapping[(name, pos)]
            else:
                r = pos[1] // 32
                c = pos[0] // 32
                gim, siz = mygame.load_grid_img(name, (32, 32))
                tex = gim[r][c]
                tid = len(self.tex)
                self.tex.append(tex)
            self.tids[y][x] = tid
    def update(self, clcok):
        pass
    def draw(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                tid = self.tids[y][x]
                tex = self.tex[tid]
                screen.blit(tex, (x * 32, y * 32))
    def get_tex(self, img):
        return None

if __name__ == "__main__":
    mp = Mapper()
    mp.load("./data/map/jungle.tmx")
