#coding=utf-8

class ScreenBox:
    RATIO = 3.0
    SCROLL_LRGRID = 6
    SCROLL_UDGRID = 5
    GRID_SIZE = 40
    SCROLL_UP = 0
    SCROLL_DOWN = 0
    SCROLL_LEFT = 0
    SCROLL_RIGHT = 0
    def __init__(self, surface):
        self.surface = surface
        self.display_x = 200
        self.display_y = 0
        self.boxW, self.boxH = self.surface.get_size()
        SCROLL_LRSIZE = self.SCROLL_LRGRID * self.GRID_SIZE
        SCROLL_UDSIZE = self.SCROLL_UDGRID * self.GRID_SIZE
        self.SCROLL_UP = SCROLL_UDSIZE
        self.SCROLL_LEFT = SCROLL_LRSIZE
        self.SCROLL_DOWN = self.boxH - SCROLL_UDSIZE 
        self.SCROLL_RIGHT = self.boxW - SCROLL_LRSIZE 
        self.player = 0
        self.last_rx = 0
        self.last_ry = 0
        self.mapData = 0
        self.min_dx = 0
        self.min_dy = 0
        self.max_dx = 0
        self.max_dy = 0
    def set_viewer(self, player):
        self.player = player
        self.last_rx = self.player.realx
        self.last_ry = self.player.realy
        dx = self.player.realx - self.boxW / 2
        dy = self.player.realy - self.boxH / 2
        self.display_x = min(max(self.min_dx, dx), self.max_dx)
        self.display_y = min(max(self.min_dy, dy), self.max_dy)
    def set_mapdata(self, mapData):
        self.mapData = mapData
        self.max_dx = max(0, self.mapData.Width * self.GRID_SIZE - self.boxW)
        self.max_dy = max(0, self.mapData.Height * self.GRID_SIZE - self.boxH + 80)
    def fill(self, color):
        self.surface.fill(color)
    def blit(self, pic, pos):
        x,y = pos
        x -= self.display_x
        y -= self.display_y
        px, py = pic.get_size()
        if self.is_in_box((x,y)) or self.is_in_box((x+px,y)) or self.is_in_box((x,y+py)) or self.is_in_box((x+px,y+py)):
            r = ScreenBox.RATIO
            self.surface.blit(pic, (x * r, y * r))
    def blit_fix(self, pic, pos):
        r = ScreenBox.RATIO
        x, y = pos
        self.surface.blit(pic, (x * r, y * r))
        #self.surface.blit(pic, pos)
    def is_in_box(self, pos):
        if pos[0] > 0 and pos[1] > 0:
            if pos[0] < self.boxW and pos[1] < self.boxH:
                return True
        return False
    def scroll(self):
        dx = self.player.realx - self.display_x
        dy = self.player.realy - self.display_y
        if dx < self.SCROLL_LEFT:
            if self.player.realx < self.last_rx:
                self.display_x = max(self.display_x - (self.last_rx - self.player.realx), self.min_dx)
        elif dx > self.SCROLL_RIGHT:
            if self.player.realx > self.last_rx:
                self.display_x = min(self.display_x + (self.player.realx - self.last_rx), self.max_dx)
        if dy < self.SCROLL_UP:
            if self.player.realy < self.last_ry:
                self.display_y = max(self.display_y - (self.last_ry - self.player.realy), self.min_dy)
        elif dy > self.SCROLL_DOWN:
            if self.player.realy > self.last_ry:
                self.display_y = min(self.display_y + (self.player.realy - self.last_ry), self.max_dy)
        self.last_rx = self.player.realx
        self.last_ry = self.player.realy


def RS(siz):
    # 原图片大小
    r = ScreenBox.RATIO
    tw = siz[0] // r
    th = siz[1] // r
    return (tw, th)

def TS(w, h):
    r = ScreenBox.RATIO
    tw = int(w * r) 
    th = int(h * r) 
    return (tw, th)
