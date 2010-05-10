import pygame
from pygame.locals import *

#import random

import sprite

def init(g, r):
    s = sprite.Sprite3(g, r, 'captured-generic', (0, 0, 32, 32))

    s.rect.centerx = r.centerx
    s.rect.centery = r.centery
    s.hit_groups.add('player')
    s.groups.add('capsule')
    s.hit = hit
    g.sprites.append(s)
    s.loop = loop

    s.life = 300

    s.vx = (g.game.random % 05) / 10.0 - 0.5 #random.random() - 0.5
    s.vy = -1.0
    s.x = float(s.rect.x)
    #s.y = float(s.rect.y)

    s.carrying = []
    s.prev = pygame.Rect(s.rect)

    g.game.sfx['capsule'].play()

    return s

def loop(g,s):
    s.vx += (g.game.random % 100) / 1000.0 - 0.05
    s.vx = max(-0.25, min(0.25, s.vx))
    s.x += s.vx

    dx = int(s.x - s.rect.x)

    dy = sprite.myinc(g.frame, s.vy)

    s.rect.x += dx
    s.rect.y += dy

    if s.life == 0:
        die(g, s)
    s.life -= 1

    for b in s.carrying:
        b.rect.x += dx
        b.rect.y += dy


def die(g, s):
    g.game.sfx['pop'].play()
    s.active = False

    for b in s.carrying:
        sprite.stop_standing(g, b)


def hit(g, a, b):
    if not hasattr(b, 'standing'):
        return

    r = a.rect
    aprev = a.prev
    cur = b.rect
    prev = b.prev

    if prev.bottom <= aprev.top and cur.bottom > r.top:
        cur.bottom = r.top
        b.standing = a
        if b not in a.carrying:
            a.carrying.append(b)
