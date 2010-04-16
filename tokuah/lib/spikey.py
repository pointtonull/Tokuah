import pygame
from pygame.locals import *

import sprite
import player

def init(g,r,n,*params):
    s = sprite.Sprite3(g,r,3,(0,0,16,16))
    s.rect.bottom = r.bottom
    s.rect.centerx = r.centerx
    s.groups.add('solid')
    s.hit_groups.add('player')
    s.hit = hit
    g.sprites.append(s)
    s.loop = loop
    
    s.vx = 1
    s.vy = 1
    
    s._prev = pygame.Rect(s.rect)
    s.strength = 3
    
    s.standing = None
    return s
    
def loop(g,s):
    sprite.apply_gravity(g,s)
    sprite.apply_standing(g,s)
    
    if s.rect.x == s._prev.x:
        s.vx = -s.vx
    s._prev = pygame.Rect(s.rect)
    
    s.rect.x += s.vx*1
    s.rect.y += s.vy
    
    

def hit(g,a,b):
    player.damage(g,b)
    #print 'youve been spikeys!'
    pass
