import pygame
from pygame.locals import *

import sprite
import player
from cnst import *

def init(g,r,n,*params):
    s = sprite.Sprite3(g,r,'robo-left',(0,0,15,18))
    s.rect.bottom = r.bottom
    s.rect.centerx = r.centerx
    s.groups.add('solid')
    s.groups.add('enemy')
    s.hit_groups.add('player')
    s.hit = hit
    g.sprites.append(s)
    s.loop = loop

    s.x = float(s.rect.x)
    s.y = float(s.rect.y)
    
    s.vx = 0.0
    s.vy = 0.0
    
    s._prev = pygame.Rect(-1,-1,0,0) #pygame.Rect(s.rect)
    s.strength = 3
    
    s.standing = None
    return s
    
def loop(g,s):
    sprite.apply_gravity(g,s)
    sprite.apply_standing(g,s)
    
    #if s.rect.x == s._prev.x:
    #    s.vx = -s.vx
    #s._prev = pygame.Rect(s.rect)

    if g.player.rect.centerx > s.rect.centerx:
        s.vx += 0.05
    elif g.player.rect.centerx < s.rect.centerx:
        s.vx -= 0.05

    if s.vx > 0.0:
        s.image = 'robo-right'
    elif s.vx < 0.0:
        s.image = 'robo-left'

    if sprite.get_code(g,s,sign(s.vx),0) == CODE_ROBO_TURN:
        s.vx = 0.0

    s.vx = min(2.0, s.vx)
    s.vx = max(-2.0, s.vx)

    s.rect.x += sprite.myinc(g.frame, s.vx)
    s.rect.y += sprite.myinc(g.frame, s.vy)
    
def hit(g,a,b):
    player.damage(g,b)
    #print 'youve been spikeys!'
    pass
