import pygame
from pygame.locals import *

from cnst import *

import sprite
        
def t_init(g,r,n,hit_groups,hit,*params):
    t = sprite.Sprite(r,n)
    for grp in hit_groups: t.hit_groups.add(grp)
    def _hit(g,a,b):
        return hit(g,a,b,*params)
    t.hit = _hit
    t.standable = 0
    if len(params) > 0:
        t.standable = params[0]
    g.layer[r.centery/TH][r.centerx/TW] = t
    return t

# tile that takes up half the space it normally would, and is on the left side
def tl_init(g,r,n,hit_groups,hit,*params):
    t = t_init(g,r,n,hit_groups,hit,*params)
    t.rect.w = t.rect.w / 2
    return t

# same as tl_init, but on the right side
def tr_init(g,r,n,hit_groups,hit,*params):
    t = tl_init(g,r,n,hit_groups,hit,*params)
    t.rect.x += t.rect.w
    #print t.rect
    return t

def tile_to_sprite(g,s):
    import tiles
    x,y = s.rect.centerx/TW,s.rect.centery/TH
    tiles.t_put(g,(x,y),0)
    
    g.sprites.append(s)