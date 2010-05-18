#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import pygame
from pygame.locals import *

from cnst import *

import sprite
import player

import math
import random

class Boss(sprite.Sprite3):
    def __init__(self, game, rect, name, *args):
        sprite.Sprite3.__init__(self, game, rect, 'boss/left-0',
            (54, 124, 150, 78))
        self.rect.centery = rect.centery
        self.rect.centerx = rect.centerx
        self.groups.add('boss')
        self.hit_groups.add('capsule')
        self.game.sprites.append(self)
        self.game.boss = self

        self.vx = -1.4
        self.vy = 0

        self.auto_gc = False

        self.phase = 1
        self.phase_frames = 0

        self.taking_damage = 0

        self.dying = None
        self.dead = False

        self.drop = 120

        self.facing = 'right'

        if self.vx < 0:
            self.facing = 'left'

        self._prev = None
        self.strength = 6


    def loop(self):
        if self.dying != None:
            self.image = 'boss/%s-%d' % (self.facing,
                (self.game.frame / (FPS / 8)) % 8)
            if self.dying % 15 == 0:
                self.game.game.sfx['boss_explode'].play()
            if self.dying % 15 > 10:
                self.image = 'boss/%s-damage-%d' % (self.facing,
                    (self.game.frame / (FPS / 8)) % 8)
            self.dying += 1

            mid_frame = FPS * 3 / 2
            end_frame = FPS * 6 / 2

            if self.dying == mid_frame:
                # explode
                self.game.game.sfx['pop'].play()
                for n in xrange(128):
                    rect = pygame.Rect(random.randint(self.rect.left,
                        self.rect.right), random.randint(self.rect.top,
                        self.rect.bottom), 1, 1)
                    Bub(self.game, rect)

            if self.dying >= mid_frame:
                self.image = None

            if self.dying > end_frame:
                self.dead = True

            return

        if sprite.get_code(self.game, self, sign(self.vx), 0) == CODE_BOSS_TURN:
            self.vx = - self.vx

        if self.phase == 2:
            if self.phase_frames == 240 + 32:
                self.vy = 0
                self.vx = 1.2

        if self.vx > 0:
            self.facing = 'right'
        else:
            self.facing = 'left'

        self.rect.x += sprite.myinc(self.game.frame, self.vx)
        self.rect.y += sprite.myinc(self.game.frame, self.vy)

        self.image = 'boss/%s-%d' % (self.facing,
            (self.game.frame / (FPS / 8)) % 8)

        if self.taking_damage > 0:
            if self.taking_damage % 20 > 10:
                self.image = 'boss/%s-damage-%d' % (self.facing,
                (self.game.frame / (FPS / 8)) % 8)
            self.taking_damage -= 1

        self.phase_frames += 1

        if self.drop == 0:
            if self.vy == 0: # no bombing when flying up to the second phase
                Fireball(self.game, self.rect, self)
            if self.phase == 1:
                self.drop = 120
            if self.phase == 2:
                self.drop = 90
        s.drop -= 1


    def hit(self, a, b):
        self.game.game.sfx['boss_explode'].play()
        a.strength -= 1
        a.taking_damage = 60
        b.active = False
        if a.strength == 3:
            a.vy = -1
            a.vx = 0
            a.phase = 2
            a.phase_frames = 0
        if a.strength == 0:
            a.dying = 0


class Bub(sprite.Sprite3):
    def __init__(self, game, rect):
        sprite.Sprite3.__init__(self, game, rect, 'big-bubble', (0, 0, 16, 16))

        self.rect.centerx = r.centerx
        self.rect.centery = r.centery
        self.game.sprites.append(self)

        speed = random.randint(16, 64)
        angle = random.randint(0, 360) * 6.28 / 360
        self.vx = math.sin(angle) * speed
        self.vy = math.cos(angle) * speed
        self.frame = random.randint(0, FPS * 2)

    def loop(self):
        self.vx *= 0.98
        self.vy *= 0.98
        self.rect.x += sprite.myinc(self.game.frame, self.vx)
        self.rect.y += sprite.myinc(self.game.frame, self.vy)
        self.frame += 1
        if self.frame >= FPS * 2:
            self.active = False
            if random.randint(0, 3) == 1:
                self.game.game.sfx['pop'].play()
