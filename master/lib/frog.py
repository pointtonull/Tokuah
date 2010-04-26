#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""Este es el modúlo que controla la acción de los sapos"""

from cnst import sign, CODE_FROG_TURN, CODE_FROG_JUMP
import pygame
import sprite
import tiles
import player

def init(g, r, n, vx, *params):
    s = sprite.Sprite3(g, r, 'frog/walk-left-0', (8, 4, 18, 19)) #(1,1,22,22))
    s.rect.bottom = r.bottom
    s.rect.centerx = r.centerx
    s.groups.add('solid')
    s.groups.add('enemy')
    s.hit_groups.add('player')
    s.hit = hit
    g.sprites.append(s)
    s.loop = loop
    s.next_frame = 12

    s.frame = 0
    s.vx = vx
    s.vy = 0
    s.jumping = False
    s.walking = not s.jumping
    s._prev = None

    s.strength = 3
    s.vy_jump = 0

    s.standing = None
    return s

def loop(g,s):
    sprite.apply_gravity(g, s)
    sprite.apply_standing(g, s)

    if s.walking:
        if s._prev != None:
            if (s.rect.x == s._prev.x
                or sprite.get_code(g,s,sign(s.vx),0) == CODE_FROG_TURN):
                s.vx = -s.vx
                s.next_frame = 1

        if (s.standing != None
        and sprite.get_code(g, s, sign(s.vx), 1) == CODE_FROG_JUMP):
            #s.vy_jump = -4.0
            s.vy_jump = -1.8
            if sprite.get_code(g, s, sign(s.vx) * 2, 1) == CODE_FROG_JUMP:
                #s.vy_jump = -6.5
                s.vy_jump = -2
                if sprite.get_code(g, s, sign(s.vx) * 3, 1) == CODE_FROG_JUMP:
                    #s.vy_jump = -8.5
                    s.vy_jump = -2.2

            s.jumping = True
            s.walking = False
            s.next_frame = 20
            if s.vx > 0:
                s.image = 'frog/prejump-right'
            elif s.vx < 0:
                s.image = 'frog/prejump-left'

        s._prev = pygame.Rect(s.rect)

        s.rect.x += s.vx * 1
        s.rect.y += s.vy
    else:
        s._prev = pygame.Rect(s.rect)
        if (s.next_frame <= 0):
            if (s.standing != None):
                s.walking = True
                s.jumping = not s.walking
                s.next_frame = 1
            #s.vx*1
            vx = s.vx * 1.5
            s.rect.x += sprite.myinc(g.frame, vx)
            s.rect.y += sprite.myinc(g.frame, s.vy)

    s.next_frame -= 1
    if s.next_frame == 0:
        if s.jumping:
            sprite.stop_standing(g,s)
            s.vy = s.vy_jump
            if s.vx > 0:
                s.image = 'frog/jump-right'
            elif s.vx < 0:
                s.image = 'frog/jump-left'
        else:
            s.next_frame = 6
            s.frame += 1
            if s.frame > 4:
                s.frame = 0
            if s.vx > 0:
                s.image = 'frog/walk-right-' + str(s.frame)
            elif s.vx < 0:
                s.image = 'frog/walk-left-' + str(s.frame)

def hit(g,a,b):
    player.damage(g, b)
