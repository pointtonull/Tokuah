import pygame
from pygame.locals import *

from cnst import *

import sprite

def init(g, r, n, vx, vy):

    x = r.centerx/TW
    y = r.centery/TH
    code = g.data[2][y][x]
    min_x = x
    max_x = x

    for dx in xrange(1, 4):
        if g.data[2][y][x + dx] != code:
            break
        max_x = x + dx

    for dx in xrange(-1, -4, -1):
        if g.data[2][y][x+dx] != code:
            break
        min_x = x + dx

    iy = y
    for ix in xrange(min_x, max_x + 1):
        if (ix,iy) in g.codes:
            return

    w = (max_x - min_x + 1) * TW
    h = TH
    r = pygame.Rect(min_x * TW, iy * TH, w, h)

    s = sprite.Sprite3(g, r, 'platform/%d' % (max_x - min_x + 1), (0, 0, w, h))
    s.groups.add('solid')
    s.hit_groups.add('player')
    s.hit = hit
    g.sprites.append(s)
    s.loop = loop

    s.vx = vx * 2
    s.vy = vy * 2

    s._prev = None
    s.carrying = []

    return s


def loop(g, s):
    #check if we hit a wall...
    if s._prev != None:
        if (s.rect.x == s._prev.x
            or sprite.get_code(g, s, sign(s.vx), 0) == CODE_PLATFORM_TURN):
            s.vx = -s.vx
        if (s.rect.y == s._prev.y
            or sprite.get_code(g, s, 0, sign(s.vy)) == CODE_PLATFORM_TURN):
            s.vy = -s.vy

    s._prev = pygame.Rect(s.rect)

    s.rect.x += s.vx
    s.rect.y += s.vy

    for b in s.carrying:
        b.rect.x += s.vx
        b.rect.y += s.vy


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
