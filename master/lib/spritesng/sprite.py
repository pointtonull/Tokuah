#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import pygame
from pygame.locals import *
from decoradores import Deprecated
from cnst import *

class Sprite:

    def __init__(self, rect, name):
        self.rect = pygame.Rect(rect)
        self.pos = rect.centerx / TH, rect.centery / TW
        self.image = name
        self.shape = pygame.Rect(0, 0, TW, TH)
        self.exploded = 0

        self.hit_groups = set()
        self.hit = None
        self.groups = set()

        # needed for gravity to work / not work ... :)
        self.standing = None
        self.active = True
        self.deinit = deinit
        self.auto_gc = True


class Sprite2(Sprite):

    def __init__(self, game, rect, name):
        Sprite.__init__(self, rect, name)
        img = game.images[n]
        self.rect.w = self.shape.w = img.get_width()
        self.rect.h = self.shape.h = img.get_height()


class Sprite3(Sprite):

    def __init__(self, game, rect, name, shape):
        shape = pygame.Rect(shape)
        Sprite.__init__(self, rect, name)
        self.shape.x = shape.x
        self.shape.y = shape.y
        self.rect.w = self.shape.w = shape.w
        self.rect.h = self.shape.h = shape.h
        self.game = game


    def apply_gravity(self):
        if self.standing != None:
            self.vy = 0
            return
        self.vy += 0.2 * 2
        self.vy = min(self.vy, 6 * 2)


    def apply_standing(self):
        if self.standing == None:
            return

        if not self.standing.active:
            self.stop_standing()
            return

        a = self.rect
        b = self.standing.rect
        a.bottom = b.top

        if a.left > b.right or a.right < b.left:
            self.stop_standing()
            self.rect.y += 1 #throw on a bit o' gravity
            return


    def stop_standing(self):
        if hasattr(self.standing,'carrying'):
            if self in self.standing.carrying:
                self.standing.carrying.remove(self)
        self.standing = None


    def get_code(self, ix,iy):
        #dx,dy get taken down to their signed component
        dx = sign(ix)
        dy = sign(iy)
        rect = self.rect
        x = [rect.left, rect.centerx, rect.right][dx + 1]
        y = [rect.top, rect.centery, rect.bottom][dy + 1]
        x = (x + dx) / TW + dx * max(0, abs(ix) - 1)
        y = (y + dy) / TH + dy * max(0, abs(iy) - 1)
        if x < 0 or y < 0 or x >= self.game.size[0] or y >= self.game.size[1]:
            return 0
        else:
            return self.game.data[2][y][x]


    def init_bounds(self, game):
        x = self.rect.centerx / TW
        y = self.rect.centery / TH

        min_x = x
        min_y = y
        max_x = x
        max_y = y

        while game.data[2][y][min_x] != CODE_BOUNDS:
            min_x -= 1
        while game.data[2][y][max_x] != CODE_BOUNDS:
            max_x += 1
        while game.data[2][min_y][x] != CODE_BOUNDS:
            min_y -= 1
        while game.data[2][max_y][x] != CODE_BOUNDS:
            max_y += 1

        min_x += 1
        min_y += 1

        game.bounds = pygame.Rect(min_x * TW, min_y * TH, (max_x - min_x) * TW,
            (max_y - min_y) * TH)

        game.view.w = min(SW, game.bounds.w)
        game.view.h = min(SH, game.bounds.h)


    def init_view(self, game):
        game.view.centerx = self.rect.centerx
        game.view.centery = self.rect.centery
        self.pan_screen(game)


    def init_codes(self, game):
        game.view.clamp_ip(game.bounds)
        border = game.get_border(INIT_BORDER)
        game.run_codes(border)


    def myinc(self, speed):
        returns = 0
        s = sign(speed)
        returns = int(speed)
        speed -= returns
        speed = abs(speed)
        c = 37 #an arbitrary prime number
        n = int(self.game.frame * c * speed) % c < int(c * speed)
        returns += s * n
        return returns


    def get_code(self, ix,iy):
        #dx,dy get taken down to their signed component
        dx = sign(ix)
        dy = sign(iy)

        rect = self.rect
        x = (rect.left, rect.centerx, rect.right)[dx + 1]
        y = (rect.top, rect.centery, rect.bottom)[dy + 1]
        x = (x + dx) / TW + dx * max(0, abs(ix) - 1)
        y = (y + dy) / TH + dy * max(0, abs(iy) - 1)
        if x < 0 or y < 0 or x >= self.game.size[0] or y >= self.game.size[1]:
            return 0
        return self.game.data[2][y][x]

@Deprecated(DEPRECATED)
def apply_gravity(g, s):
    if s.standing != None:
        s.vy = 0
        return
    s.vy += 0.2 * 2
    s.vy = min(s.vy, 6 * 2)

@Deprecated(DEPRECATED)
def apply_standing(g,s):
    if s.standing == None: return
    if not s.standing.active:
        stop_standing(g, s)
        return

    a,b = s.rect, s.standing.rect
    a.bottom = b.top

    if a.left > b.right or a.right < b.left:
        stop_standing(g, s)
        s.rect.y += 1 #throw on a bit o' gravity
        return

@Deprecated(DEPRECATED)
def stop_standing(g,s):
    if hasattr(s.standing,'carrying'):
        if s in s.standing.carrying:
            s.standing.carrying.remove(s)
    s.standing = None

@Deprecated(DEPRECATED)
def deinit(g,s):
    if hasattr(s,'standing'):
        stop_standing(g,s)

@Deprecated(DEPRECATED)
def init_bounds(g,s):
    x,y = s.rect.centerx/TW,s.rect.centery/TH
    min_x,min_y,max_x,max_y = x,y,x,y
    while g.data[2][y][min_x] != CODE_BOUNDS: min_x -= 1
    while g.data[2][y][max_x] != CODE_BOUNDS: max_x += 1
    while g.data[2][min_y][x] != CODE_BOUNDS: min_y -= 1
    while g.data[2][max_y][x] != CODE_BOUNDS: max_y += 1
    min_x += 1
    min_y += 1
    g.bounds = pygame.Rect(min_x*TW,min_y*TH,(max_x-min_x)*TW,(max_y-min_y)*TH)

    g.view.w = min(SW,g.bounds.w)
    g.view.h = min(SH,g.bounds.h)

    #if g.bounds.w < SW:
        #print 'uh oh, g.bounds.w < SW',g.bounds.w
    #if g.bounds.h < SH:
        #print 'uh oh, g.bounds.h < SH',g.bounds.h

@Deprecated(DEPRECATED)
def init_view(g,s):
    g.view.centerx = s.rect.centerx
    g.view.centery = s.rect.centery
    s.pan(g,s)

@Deprecated(DEPRECATED)
def init_codes(g,s):
    g.view.clamp_ip(g.bounds)
    border = g.get_border(INIT_BORDER)
    g.run_codes(border)

@Deprecated(0)
def sign(v):
    if v < 0: return -1
    if v > 0: return 1
    return 0
