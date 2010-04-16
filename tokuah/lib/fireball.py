import pygame
from pygame.locals import *

import sprite
import capsule
import player

def init(g,r,p, big=False):
    s = sprite.Sprite3(g,r,'fireball',(0,0,16,16))
    s.big = big
    if p.facing == 'left':
        s.rect.centerx = r.x + 34 - 27
        s.rect.centery = r.y + 83 - 62
    else:
        s.rect.centerx = r.right - 34 + 27
        s.rect.centery = r.y + 83 - 62
    s.groups.add('solid')
    s.groups.add('enemy')
    s.hit_groups.add('player')
    s.hit = hit
    g.sprites.insert(0,s)
    s.loop = loop
    s.life = 600
    s.strength = 1
    s.standing = None

    s.bounces = 3
    
    s.vx = 0.2 
    if p.facing == 'left':
        s.vx = -0.2

    s.vx += p.vx
    s.vy = 0
    
    #g.game.sfx['bubble'].play()
    
    return s

def loop(g,s):
    sprite.apply_gravity(g,s)
    sprite.apply_standing(g,s)

    if s.bounces > 0 and s.standing:
        sprite.stop_standing(g,s)
        s.vy = -s.bounces * 0.75
        s.bounces -= 1
        if s.bounces == 0:
            s.vx = 0

    s.rect.x += sprite.myinc(g.frame,s.vx)
    s.rect.y += sprite.myinc(g.frame,s.vy)

    s.life -= 1
    if s.life == 0:
        s.active = False

def hit(g,a,b):
    player.damage(g,b)
