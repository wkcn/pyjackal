#coding=utf-8

MaxFPS = 60
FrameClock = 1000 / MaxFPS

def Normalize(clock):
    return clock * MaxFPS / 1000.0

def print_bits(mask):
    rows, cols = mask.shape[:2]
    print (rows, cols)
    for r in range(rows):
        for c in range(cols):
            if mask[r,c]:
                print 1,
            else:
                print 0,
        print ""

