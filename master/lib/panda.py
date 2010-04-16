import pygame
from pygame.locals import *

import sprite
import player

def init(g,r,n,facing,*params):
    s = sprite.Sprite3(g,r,'panda-%s' % (facing),(0,0,31,45))
    s.rect.bottom = r.bottom
    s.rect.centerx = r.centerx
    s.groups.add('solid')
    s.groups.add('enemy')
    s.hit_groups.add('player')
    s.hit = hit
    g.sprites.append(s)
    s.loop = loop
    
    s.vx = 0
    s.vy = 0
    
    #s._prev = pygame.Rect(s.rect)
    s.strength = 30000
    
    s.standing = None
    return s
    
def loop(g,s):
    sprite.apply_gravity(g,s)
    sprite.apply_standing(g,s)
    
    #if s.rect.x == s._prev.x:
        #s.vx = -s.vx
    #s._prev = pygame.Rect(s.rect)
    
    s.rect.x += s.vx
    s.rect.y += sprite.myinc(g.frame,s.vy)
    
    

def hit(g,a,b):
    player.damage(g,b)
    #print 'youve been spikeys!'
    pass
