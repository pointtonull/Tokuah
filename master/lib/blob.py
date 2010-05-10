import pygame
from pygame.locals import *

import sprite
import player

from cnst import *

def init(g, r, n, *params):
    s = sprite.Sprite3(g, r, 'blob', (0, 0, 30, 30))
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

    s.next_jump = 0

    s._prev = pygame.Rect(s.rect)
    s.strength = 3
    
    s.standing = None
    return s
    
def loop(g, s):
    #print 'loop'
    sprite.apply_gravity(g, s)
    sprite.apply_standing(g, s)

    #print s.vy

    if s.next_jump == 0 and s.standing:
        s.vy = - 12.0
        s.next_jump = FPS * 2
        sprite.stop_standing(g, s)
    if s.next_jump > 0:
        s.next_jump -= 1
    
    s._prev = pygame.Rect(s.rect)
    
    s.rect.y += sprite.myinc(g.frame,s.vy)
    

def hit(g, a, b):
    player.damage(g, b)
