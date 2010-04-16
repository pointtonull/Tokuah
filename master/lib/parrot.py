import pygame
from pygame.locals import *

from cnst import *

import sprite
import player

def init(g,r,n,vx,*params):
    s = sprite.Sprite3(g,r,'parrot/left-0',(0,3,24,10)) #3
    #s.rect.bottom = r.bottom
    s.rect.centery = r.centery
    s.rect.centerx = r.centerx
    s.groups.add('solid')
    s.groups.add('enemy')
    s.hit_groups.add('player')
    s.hit = hit
    g.sprites.append(s)
    s.loop = loop
    
    s.vx = vx
    s.vy = 0
    
    s.facing = 'right'
    if s.vx < 0:
        s.facing = 'left'
    
    s._prev = None # pygame.Rect(s.rect)
    s.strength = 3

    #s.standing = None
    return s
    
def loop(g,s):
    #sprite.apply_gravity(g,s)
    
    if s._prev != None:
        if s.rect.x == s._prev.x or sprite.get_code(g,s,sign(s.vx),0) == CODE_PARROT_TURN:
            s.vx = -s.vx
            if s.vx > 0: s.facing = 'right'
            else:        s.facing = 'left'
    s._prev = pygame.Rect(s.rect)
    
    s.rect.x += s.vx*1
    s.rect.y += s.vy
    
    s.image = 'parrot/%s-%d'%(s.facing,(g.frame/(FPS/8))%4)
    
    #sprite.check_standing(g,s)
    

def hit(g,a,b):
    player.damage(g,b)
    #print 'youve been spikeys!'
