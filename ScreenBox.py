#coding=utf-8

class ScreenBox:
    RATIO = 3.0
    SCROLL_LRGRID = 3
    SCROLL_UGRID = 3
    SCROLL_DGRID = 2
    GRID_SIZE = 32
    SCROLL_UP = 0
    SCROLL_DOWN = 0
    SCROLL_LEFT = 0
    SCROLL_RIGHT = 0
    def __init__(self, surface):
        self.surface = surface
        self.display_x = 0
        self.display_y = 0
        boxW, boxH = self.surface.get_size()
        self.boxRW = boxW * 1.0 / ScreenBox.RATIO
        self.boxRH = boxH * 1.0 / ScreenBox.RATIO
        SCROLL_LRSIZE = ScreenBox.SCROLL_LRGRID * ScreenBox.GRID_SIZE
        self.SCROLL_UP = ScreenBox.SCROLL_UGRID * ScreenBox.GRID_SIZE
        self.SCROLL_LEFT = SCROLL_LRSIZE
        self.SCROLL_DOWN = self.boxRH - ScreenBox.SCROLL_DGRID * ScreenBox.GRID_SIZE 
        self.SCROLL_RIGHT = self.boxRW - SCROLL_LRSIZE 
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
        dx = self.player.realx - self.boxRW / 2.0
        dy = self.player.realy - self.boxRH / 2.0
        self.display_x = min(max(self.min_dx, dx), self.max_dx)
        self.display_y = min(max(self.min_dy, dy), self.max_dy)
    def set_mapper(self, mp):
        self.max_dx = max(0, mp.width * self.GRID_SIZE - self.boxRW)
        self.max_dy = max(0, mp.height * self.GRID_SIZE - self.boxRH)
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
            if pos[0] < self.boxRW and pos[1] < self.boxRH:
                return True
        return False
    def scroll(self):
        dx = self.player.realx - self.display_x
        dy = self.player.realy - self.display_y
        #print (dx, dy, self.SCROLL_DOWN)
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
