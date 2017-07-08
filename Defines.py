#coding=utf-8

MaxFPS = 60
FrameClock = 1000 / MaxFPS

def Normalize(clock):
    return clock * MaxFPS / 1000.0
