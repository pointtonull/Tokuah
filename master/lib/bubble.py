import pygame
from pygame.locals import *

import sprite
import capsule

def init(g,r,p, big=False):
    if not hasattr(g,'bubble_count'):
        g.bubble_count = 0
    if g.bubble_count >= 3:
        return None
    g.bubble_count += 1
    #print 'new bubble', g.bubble_count
    if not big:
        s = sprite.Sprite3(g,r,'bubble',(0,0,7,7))
    else:
        s = sprite.Sprite3(g,r,'big-bubble',(0,0,16,16))
    s.big = big
    s.rect.centerx = r.centerx
    s.rect.centery = r.centery
    s.groups.add('solid')
    s.groups.add('bubble')
    s.hit_groups.add('enemy')
    s.hit = hit
    g.sprites.append(s)
    s.loop = loop
    s.life = 30
    s.strength = 1
    s.deinit = deinit
    if big: s.strength = 3
    
    s.vx = 1
    if p.facing == 'left':
        s.vx = -1
    s.vy = 0
    s.rect.centerx += s.vx*(6+s.rect.width/2)
    s.rect.centery -= 4
    
    g.game.sfx['bubble'].play()
    
    return s

def deinit(g,s):
    #print "bubble deinit"
    g.bubble_count -= 1
    
def loop(g,s):
    s.rect.x += s.vx*5
    s.life -= 1
    if s.life == 0:
        s.active = False

def hit(g,a,b): 
    a.active = False
    
    b.strength -= a.strength
    if b.strength <= 0:
        b.active = False
        code = None
        if hasattr(b,'_code'):
            code = b._code
            delattr(b,'_code')
        s = capsule.init(g,b.rect)
        if code != None:
            s._code = code
    else:
        g.game.sfx['hit'].play()
        
    #print 'bubble hit!'
