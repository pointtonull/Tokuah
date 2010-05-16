#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""Este es el modúlo que controla la acción de los sapos"""

from cnst import sign, CODE_FROG_TURN, CODE_FROG_JUMP
import pygame
import sprite
import tiles
import player

class Frog(sprite.Sprite3):
    def __init__(self, game, rect, name, vx, *args):
        sprite.Sprite3(self, game, rect, 'frog/walk-left-0', (16, 8, 36, 38))
        self.rect.bottom = rect.bottom
        self.rect.centerx = rect.centerx
        self.groups.add('solid')
        self.groups.add('enemy')
        self.hit_groups.add('player')
        self.hit = hit
        game.sprites.append(self)
        self.next_frame = 12

        self.frame = 0
        self.vx = vx * 2
        self.vy = 0
        self.jumping = False
        self.walking = not s.jumping
        self._prev = None

        self.strength = 3
        self.vy_jump = 0

        self.standing = None

        self.game = game

    def loop(self):
        sprite.apply_gravity(self.game, self)
        sprite.apply_standing(self.game, self)

        if self.walking:
            if self._prev != None:
                if (self.rect.x == self._prev.x or sprite.get_code(game, self,
                        sign(self.vx), 0) == CODE_FROG_TURN):
                    self.vx = - self.vx
                    self.next_frame = 1

            if (self.standing != None and sprite.get_code(game, self,
                    sign(self.vx), 1) == CODE_FROG_JUMP):
                #s.vy_jump = -4.0
                self.vy_jump = - 3.6 * 1.22
                if (sprite.get_code(self.game, self, sign(self.vx) * 2, 1)
                        == CODE_FROG_JUMP):
                    #s.vy_jump = -6.5
                    self.vy_jump = - 6.0 * 1.22
                    if (sprite.get_code(game, self, sign(self.vx) * 3, 1)
                         == CODE_FROG_JUMP):
                        #s.vy_jump = -8.5
                        self.vy_jump = - 8.1 * 1.22

                self.jumping = True
                self.walking = False
                self.next_frame = 20
                if self.vx > 0:
                    self.image = 'frog/prejump-right'
                elif self.vx < 0:
                    self.image = 'frog/prejump-left'

            self._prev = pygame.Rect(self.rect)

            self.rect.x += self.vx
            self.rect.y += self.vy
        else:
            self._prev = pygame.Rect(self.rect)
            if (self.next_frame <= 0):
                if (self.standing != None):
                    self.walking = True
                    self.jumping = not s.walking
                    self.next_frame = 1
                vx = self.vx * 1.8
                self.rect.x += sprite.myinc(self.game.frame, vx)
                self.rect.y += sprite.myinc(self.game.frame, self.vy)

        self.next_frame -= 1
        if self.next_frame == 0:
            if self.jumping:
                sprite.stop_standing(self.game, self)
                self.vy = self.vy_jump
                if self.vx > 0:
                    self.image = 'frog/jump-right'
                elif self.vx < 0:
                    self.image = 'frog/jump-left'
            else:
                self.next_frame = 6
                self.frame += 1
                if self.frame > 4:
                    self.frame = 0
                if self.vx > 0:
                    self.image = 'frog/walk-right-' + str(self.frame)
                elif self.vx < 0:
                    self.image = 'frog/walk-left-' + str(self.frame)

    def hit(self, a, b):
        player.damage(self, game, b)
