import pygame
from pygame.locals import *

import sprite
import capsule
import player

class Fireball(sprite.Sprite3):
    def __init__(self, game, rect, parent, big=False):
        sprite.Sprite3.__init__(self, game, rect, 'fireball', (0, 0, 32, 32))
        self.big = big

        if parent.facing == 'left':
            self.rect.centerx = rect.x + 34 - 27
            self.rect.centery = rect.y + 83 - 62
        else:
            self.rect.centerx = rect.right - 34 + 27
            self.rect.centery = rect.y + 83 - 62

        self.groups.add('solid')
        self.groups.add('enemy')
        self.hit_groups.add('player')
        self.game.sprites.insert(0, self)

        self.life = 600
        self.strength = 1
        self.standing = None

        self.bounces = 3

        self.vx = 0.4
        if parent.facing == 'left':
            self.vx = -0.4

        self.vx += parent.vx
        self.vy = 0


    def loop(self):
        self.sprite.apply_gravity()
        self.sprite.apply_standing()

        if self.bounces > 0 and self.standing:
            self.stop_standing()
            self.vy = -self.bounces * 0.75
            self.bounces -= 1
            if self.bounces == 0:
                self.vx = 0

        self.rect.x += sprite.myinc(self.game.frame, self.vx)
        self.rect.y += sprite.myinc(self.game.frame, self.vy)

        self.life -= 1
        if self.life == 0:
            self.active = False

    def hit(self, a, b):
        player.damage(self.game, b)
