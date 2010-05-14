import pygame
from pygame.locals import *

from cnst import *

import sprite
import player

def init(g,r,v):
    s = sprite.Sprite2(g,r,'points/%d'%v) #3
    s.rect.centery = r.centery
    s.rect.centerx = r.centerx
    g.sprites.append(s)
    s.loop = loop
    
    s.frame = 0
    return s
    
def loop(g,s):
    #sprite.apply_gravity(g,s)
    
    s.frame += 1
    if s.frame == FPS:
        s.active = False
    

