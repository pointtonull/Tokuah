import pygame
from pygame.locals import *

import sprite
import player
#import laser

from cnst import *

def init(g,r,n,facing,*params):
    s = sprite.Sprite3(g,r,'brobo-%s-0' % (facing),(0,0,30,37))
    s.rect.bottom = r.bottom
    s.rect.centerx = r.centerx
    s.groups.add('solid')
    s.groups.add('enemy')
    s.hit_groups.add('player')
    s.hit = hit
    g.sprites.append(s)
    s.loop = loop
    s.facing = facing

    #s.shoot = 0

    if s.facing == 'left':
        s.vx = -0.3
    else:
        s.vx = 0.3
    s.vy = 0
    
    s._prev = None #pygame.Rect(-1,-1,0,0)
    s.strength = 6
    
    s.standing = None
    s.ix = 0
    return s
    
def loop(g,s):
    sprite.apply_gravity(g,s)
    sprite.apply_standing(g,s)
    
    #if s._prev != None:
        #if s.rect.x == s._prev.x or sprite.get_code(g,s,sign(s.vx),0) == CODE_BROBO_TURN:
    if (s.ix != 0 and s.rect.x == s._prev.x) or sprite.get_code(g,s,sign(s.vx),0) == CODE_BROBO_TURN:
            s.vx = -s.vx

    s._prev = pygame.Rect(s.rect)

    if s.vx > 0:
        s.facing = 'right'
    elif s.vx < 0:
        s.facing = 'left'
    s.image = 'brobo-%s-%s' % (s.facing, (g.frame/10)%2)

    
    #if s.shoot == 0:
    #    shot = laser.init(g,s.rect,s)
    #    g.sprites.append(shot)
    #    s.shoot = 60

    #s.shoot -= 1
    
    s.ix = sprite.myinc(g.frame,s.vx)
    s.rect.x += s.ix 
    s.rect.y += sprite.myinc(g.frame,s.vy)
    
    

def hit(g,a,b):
    player.damage(g,b)
    #print 'youve been spikeys!'
    pass
