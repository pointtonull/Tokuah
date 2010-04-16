import pygame
from pygame.locals import *

import sprite
import player
from cnst import *

import random

def init(g,r,n,*params):
    s = sprite.Sprite3(g,r,'fireguy-right-0',(0,0,14,23))
    s.rect.bottom = r.bottom
    s.rect.centerx = r.centerx
    s.groups.add('solid')
    s.groups.add('enemy')
    s.hit_groups.add('player')
    s.hit = hit
    g.sprites.append(s)
    s.loop = loop

    s.moving = 0
    #s.idling = 240
    s.idling = random.randint(120,240)

    s.frame = 0

    s.facing = 'right'
    
    s.vx = 0
    s.vy = 0
    
    s._prev = pygame.Rect(s.rect)
    s.strength = 3
    
    s.standing = None
    return s
    
def loop(g,s):
    sprite.apply_gravity(g,s)
    sprite.apply_standing(g,s)
    
    if s.moving and s.rect.x == s._prev.x or sprite.get_code(g,s,sign(s.vx),0) == CODE_FIREGUY_TURN:
        s.vx = -s.vx
        if s.vx < 0:
            s.facing = 'left'
        else:
            s.facing = 'right'
    s._prev = pygame.Rect(s.rect)
    
    s.rect.x += s.vx
    s.rect.y += s.vy

    if s.idling > 0:
        if s.idling % 120 > 60:
            s.facing = 'left'
        else:
            s.facing = 'right'
        s.idling -= 1
        if s.idling == 0:
            s.moving = 90
            #if g.game.random % 2 == 0:
            if random.randint(0,1):
                s.vx = -1
                s.facing = 'left'
            else:
                s.vx = 1
                s.facing = 'right'
    elif s.moving > 0:
        s.moving -= 1
        if s.moving == 0:
            s.idling = 240
            s.vx = 0
    else:
        s.idling = 240
        
    s.image = 'fireguy-%s-%s' % (s.facing, (s.frame / 5) % 2)
    s.frame += 1

def hit(g,a,b):
    player.damage(g,b)
    #print 'youve been spikeys!'
    pass
