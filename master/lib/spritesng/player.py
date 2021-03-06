#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import pygame
import sprite
import tiles
from pygame.locals import *
from cnst import *
from decoradores import Verbose
from spritesng.bubble import Bubble

class Player(sprite.Sprite3):

    @Verbose(VERBOSE)
    def __init__(self, game, rect, name, *args):
        sprite.Sprite3.__init__(self, game, rect, 'player/right', 
            (12, 16, 30 - 12, 54 -16))
        self.rect.bottom = rect.bottom
        self.rect.centerx = rect.centerx
        self.groups.add('player')
        self.groups.add('solid')
        game.sprites.append(self)
#        self.loop = game.loop
        self.vx = 0
        self.vy = 0
        self.walk_frame = 1
        self.jumping = 0
        self.facing = 'right'
        self.flash_counter = 0
        self.flash_timer = 0
        self.shooting = 0
        self.powered_up = False

        if hasattr(game, 'powerup'):
            self.powered_up = game.powerup

        self.powerup_transition = 0
        self.door_timer = None
        self.current_door = None
        self.door_pos = None
        game.player = self

        self.god_mode = False
        self.death_counter = -1

        self._prev = pygame.Rect(self.rect)
        self._prev2 = pygame.Rect(self.rect)
        self.looking = False

        self.init_bounds(game)
        self.init_view(game)
        self.init_codes(game)
        self.no_explode = False


    def event(self, game, event):
        #print 'player.event',e
        if self.door_timer != None or self.exploded > 0:
            return

        if (event.type is USEREVENT and event.action == 'jump'
            and self.standing != None and self.jumping == 0
            and self.vy == 0):
            self.stop_standing()

            self.vy = -6 if self.powered_up else -7.5

            self.jumping = 1.4
            self.game.game.sfx['jump'].play()

        if event.type is USEREVENT and event.action == 'stop-jump':
            self.jumping = 0

        if event.type is USEREVENT and (event.action == 'up'
            or event.action == 'down'):
            if self.get_code(0, 0) in DOOR_CODES:
                self.vx = 0
                self.vy = 0
                self.door_timer = DOOR_DELAY
                if self.current_door != None:
                    # It should never be None actually...
                    self.current_door.open = DOOR_DELAY
                self.image = None
                self.door_pos = (self.rect.centerx / TW,
                    self.rect.centery / TH)

        if event.type is USEREVENT and event.action == 'bubble':
            if self.powered_up:
                Bubble(self.game, self.rect, self, big=True)
            else:
                Bubble(self.game, self.rect, self, big=False)
            self.shooting = 10

        if event.type is KEYDOWN and event.key == K_F10:
            powerup(g, s)
            self.god_mode = True


    def loop(self):
        self._prev2 = pygame.Rect(self.rect)

        if self.death_counter > 0:
            self.groups = set()
            if not self.no_explode:
                self.exploded += 1
                if self.exploded > FPS / 2:
                    self.image = None
            else:
                self.image = None
            self.death_counter -= 1
            return
        if self.death_counter == 0:
            self.game.status = 'dead'
            return

        if self.exploded > 0:
            if self.powered_up:
                self.image = 'player/right'
            else:
                self.image = 'splayer/right'
            self.exploded -= 1
            return


        self.apply_gravity()
        self.apply_standing()

        if self.door_timer != None:
            if self.door_timer == 0:
                x, y = self.door_pos
                import door
                door.hit(g, (x, y), s)
                self.door_timer = None
            else:
                self.door_timer -= 1
                return

        inpt = self.game.game.input

        #check if we hit the ceiling
        if not self.jumping and self.vy < 0 and self.rect.y == self._prev.y:
            self.vy = 0

        if self.jumping:
            self.vy -= self.jumping
            self.jumping = max(0, self.jumping - 0.2)

        inc = 1.0
        mx = 4
        if inpt.right and self.vx < mx:
            self.vx += inc
            self.facing = 'right'
        elif not inpt.right and self.vx > 0:
            self.vx -= inc

        if inpt.left  and self.vx > -mx:
            self.vx -= inc
            self.facing = 'left'
        elif not inpt.left and self.vx < 0:
            self.vx += inc


        self._prev = pygame.Rect(self.rect)

        vx = self.vx
        vy = self.vy
        self.rect.x += vx
        self.rect.y += self.myinc(self.vy)

        if self.vy < 0:
            self.image = 'player/%s-jump' % (self.facing)
        elif self.shooting > 0:
            if self.shooting > 5:
                self.image = 'player/%s-shoot-1' % (self.facing)
            else:
                self.image = 'player/%s-shoot-2' % (self.facing)
            self.shooting -= 1
        elif inpt.right or inpt.left and self.standing:
            self.image = 'player/%s-walk-%s' % (self.facing,
                int(self.walk_frame))
            self.walk_frame += 0.2
            if self.walk_frame > 4:
                self.walk_frame = 1
        else:
            self.image = 'player/%s' % (self.facing)

        if self.flash_counter > 0:
            if self.flash_timer < 4:
                self.image = None
            if self.flash_timer == 0:
                self.flash_timer = 8
                self.flash_counter -= 1
            self.flash_timer -= 1

        if self.image != None:
            if self.powerup_transition > 0:
                if (self.powerup_transition % 10) > 5:
                    self.image = 's' + self.image
                self.powerup_transition -= 1
            elif not self.powered_up:
                self.image = 's' + self.image

        self.looking = False
        if inpt.up:
            self.game.view.y -= 2
            self.looking = True
        if inpt.down:
            self.game.view.y += 2
            self.looking = True

        code = self.get_code(0, 0)
        if code == CODE_EXIT:
            self.game.status = 'exit'
        if code == CODE_DOOR_AUTO:
            x = self.rect.centerx / TW
            y = self.rect.centery / TH
            import door #WTF!
            door.hit(self.game, (x, y), self)

        if hasattr(self.game, 'boss'):
            #print g.boss.phase, g.boss.phase_frames
            if self.game.boss.phase == 2 and self.game.boss.phase_frames == 60:
                for y in xrange(len(self.game.layer)):
                    for x in xrange(len(self.game.layer[y])):
                        if self.game.data[2][y][x] == CODE_BOSS_PHASE2_BLOCK:
                            tiles.t_put(g, (x, y), 0x01) # solid tile
            if self.game.boss.dead:
                self.game.status = 'exit'
                #pygame.mixer.music.load("
                #g.game.music.play('finish',1)

    def pan_screen(self, game):
        # adjust the view
        border = pygame.Rect(self.rect)
        #pad = 100
        pad = (SW / 2) - TW
        border.x -= pad
        border.w += pad * 2
        #pad = 80
        pad = (SH / 2) - TH
        if self.looking:
            pad = TH * 2
        border.y -= pad
        border.h += pad * 2

        dest = pygame.Rect(game.view)
        dest.top = min(dest.top, border.top)
        dest.right = max(dest.right, border.right)
        dest.bottom = max(dest.bottom, border.bottom)
        dest.left = min(dest.left, border.left)

        dx = dest.x - game.view.x
        dy = dest.y - game.view.y
        #mx,my = 6,6
        mx = max(2, abs(self._prev2.x - self.rect.x))
        my = max(2, abs(self._prev2.y - self.rect.y))

        if abs(dx) > mx:
            dx = sign(dx) * mx
        if abs(dy) > my:
            dy = sign(dy) * my

        game.view.x += dx
        game.view.y += dy


    def powerup(g,s):
        if not self.powered_up:
            self.powerup_transition = 100
            self.powered_up = True

            if hasattr(g.game, 'powerup'):
                g.game.powerup = True


    def damage(g, s):
        if self.god_mode:
            return

        if self.door_timer != None:
            return

        if self.powered_up:
            g.game.sfx['pop'].play()
            self.powerup_transition = 100
            self.powered_up = False
            if hasattr(g.game, 'powerup'):
                g.game.powerup = False
        elif self.powerup_transition == 0 and self.flash_counter == 0:
            self.kill(g,s)


    def kill(g, s, no_explode=False):
        if hasattr(g.game, 'powerup'):
            g.game.powerup = False
        self.flash_counter = 10
        self.no_explode = no_explode
        g.game.music_play('death', 1)
        self.death_counter = int(FPS * 2.25)
