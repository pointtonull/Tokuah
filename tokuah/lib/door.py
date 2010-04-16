import pygame
from pygame.locals import *

from cnst import *

import sprite
import player

def init(g,r,n,hidden = False,*params):
    s = sprite.Sprite3(g,r,'door-1',(0,0,16,24)) #3
    s.rect.centerx = r.centerx
    s.rect.centery = r.centery - (24 - 16) / 2
    s.loop = loop
    s.hit = sprite_hit
    s.frame = 0
    s.open = None
    s.hit_groups.add('player')
    s.hidden = hidden
    if hidden:
        s.image = None
    #s.hit = hit
    g.sprites.insert(0,s)
    return s

def loop(g,s):
    if s.hidden:
        s.image = None
        return
    if s.open > 0:
        s.image = 'door-open'
        s.open -= 1
        return
    elif (s.frame % 256) > 192:
        s.image = 'door-2'
    else:
        s.image = 'door-1'
    s.open = None
    s.frame += 1

def sprite_hit(g,a,b):
    b.current_door = a
        
def hit(g,pos,b):
    
    cx,cy = pos
    
    import sprite
    #n_code = sprite.get_code(g,a,1,0)
    dx = 1
    while g.data[2][cy][cx+dx] in DOOR_CODES: dx += 1
    n_code = g.data[2][cy][cx+dx]
    
    if n_code == 0: return
    
    layer = g.data[2]
    
    w,h = g.size
    xx,yy = cx,cy
    for y in xrange(0,h):
        for x in xrange(0,w):
            if layer[y][x] in DOOR_CODES and layer[y][x-1] == n_code:
                xx,yy = x,y
    
    #t = g.layer[yy][xx]
    rect = pygame.Rect(xx*TW,yy*TH,TW,TH)
    s = b
    s.rect.centerx = rect.centerx
    s.rect.bottom = rect.bottom
    if s.standing != None:
        sprite.stop_standing(g,s)
    
    sprite.init_bounds(g,s)
    sprite.init_view(g,s)
    sprite.init_codes(g,s)
    s.prev = pygame.Rect(s.rect)
    s._prev = pygame.Rect(s.rect)
    
    g.status = 'transition'
    
    g.game.sfx['door'].play()
