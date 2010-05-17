#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import pygame
import sprite
import player

class Panda(sprite.Sprite3):
    def __init__(game, rect, name, facing, *args):
        sprite.Sprite3.__init__(game, rect, 'panda-%s' % (facing),
            (0, 0, 40, 86))
        self.rect.bottom = r.bottom
        self.rect.centerx = r.centerx
        self.groups.add('solid')
        self.groups.add('enemy')
        self.hit_groups.add('player')
        self.hit = hit
        game.sprites.append(self)
        self.loop = loop

        self.vx = 0
        self.vy = 0

        self._prev = pygame.Rect(s.rect)
        self.strength = 90000

        self.standing = None

    def loop(self):
        self.apply_gravity()
        self.apply_standing()

        if self.rect.x == self._prev.x:
            self.vx = - self.vx
            self._prev = pygame.Rect(self.rect)

        self.rect.x += self.vx
        self.rect.y += sprite.myinc(self.game.frame, self.vy)


    def hit(self, a, b):
        player.damage(game, b)
