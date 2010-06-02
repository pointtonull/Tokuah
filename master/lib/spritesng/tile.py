#!/usr/bin/env python
#-*- coding: UTF-8 -*-
from cnst import *
from pygame.locals import *
import pygame
import sprite
import tiles

class Tile(sprite.Sprite):
    def __init__(self, game, rect, name, hit_groups, hit, *args):
        sprite.Sprite.__init__(self, rect, name)

        for group in hit_groups:
            self.hit_groups.add(group)

        self.standable = 0
        if len(args) > 0:
            self.standable = args[0]

        game.layer[rect.centery / TH][rect.centerx / TW] = self

    def hit(self, a, b, *args): #WTF! (definición recursiva sin sentido)
        return hit(game, a, b, *args)

# tile that takes up half the space it normally would, and is on the left side
class Tile_left(Tile):
    def __init__(self, game, rect, name, hit_groups, hit, *args):
        Tile.__init__(self, game, rect, name, hit_groups, hit, *args)
        self.rect.w = rect.w / 2

# same as tl_init, but on the right side
class Tile_rigth(Tile):
    def __init__(self, game, rect, name, hit_groups, hit, *args):
        Tile.__init__(self, game, rect, name, hit_groups, hit, *args)
        self.rect.x += rect.w


def tile_to_sprite(game, sprite):
    x, y = sprite.rect.centerx / TW, sprite.rect.centery / TH
    tiles.t_put(game, (x, y), 0)

    game.sprites.append(sprite)
