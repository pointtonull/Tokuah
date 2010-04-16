import pygame
from pygame.locals import *

from cnst import *

import sprites
import sprite
import player

import math
import random

def init(g,r,n,*params):
    s = sprite.Sprite3(g,r,'boss/left-0',(27,62,75,39)) #3
    #s.rect.bottom = r.bottom
    s.rect.centery = r.centery
    s.rect.centerx = r.centerx
    #s.groups.add('solid')
    s.groups.add('boss')
    #s.groups.add('enemy')
    s.hit_groups.add('capsule')
    s.hit = hit
    g.sprites.append(s)
    s.loop = loop
    g.boss = s
    
    s.vx = -0.7
    s.vy = 0

    s.auto_gc = False

    s.phase = 1
    s.phase_frames = 0

    s.taking_damage = 0

    s.dying = None
    s.dead = False

    s.drop = 120 
    
    s.facing = 'right'
    if s.vx < 0:
        s.facing = 'left'
    
    s._prev = None # pygame.Rect(s.rect)
    s.strength = 6

    #s.standing = None
    return s
    
def loop(g,s):
    #if s.dying == None: s.dying = 1
    if s.dying != None:
        s.image = 'boss/%s-%d'%(s.facing,(g.frame/(FPS/8))%8)
        if s.dying % 15 == 0:
            g.game.sfx['boss_explode'].play()
        if s.dying % 15 > 10:
            s.image = 'boss/%s-damage-%d'%(s.facing,(g.frame/(FPS/8))%8)
        s.dying += 1
        
        mid_frame = FPS*3/2
        end_frame = FPS*6/2
        
        if s.dying == mid_frame:
            # explode
            g.game.sfx['pop'].play()
            for n in xrange(0,128):
                r = pygame.Rect(random.randint(s.rect.left,s.rect.right),random.randint(s.rect.top,s.rect.bottom),1,1)
                s2 = bub_init(g,r)
                
        if s.dying >= mid_frame:
            s.image = None
        #if s.dead:
        #    s.active = False
        if s.dying > end_frame:
            s.dead = True
            #s.active = False
        #if s.dying % 30 == 15:
        return
            
    #sprite.apply_gravity(g,s)
    
    #if s._prev != None:
        #if s.rect.x == s._prev.x or sprite.get_code(g,s,sign(s.vx),0) == CODE_PARROT_TURN:
    if sprite.get_code(g,s,sign(s.vx),0) == CODE_BOSS_TURN:
        s.vx = -s.vx
    #s._prev = pygame.Rect(s.rect)

    if s.phase == 2:
        if s.phase_frames == 240 + 32:
            s.vy = 0
            s.vx = 1.2

    if s.vx > 0: s.facing = 'right'
    else:        s.facing = 'left'

    s.rect.x += sprite.myinc(g.frame, s.vx)
    s.rect.y += sprite.myinc(g.frame, s.vy)
    
    s.image = 'boss/%s-%d'%(s.facing,(g.frame/(FPS/8))%8)
    if s.taking_damage > 0:
        if s.taking_damage % 20 > 10:
            s.image = 'boss/%s-damage-%d'%(s.facing,(g.frame/(FPS/8))%8)
        s.taking_damage -= 1

    s.phase_frames += 1

    if s.drop == 0:
        if s.vy == 0: # this is to prevent the boss from bombing you when it's
                      # flying up to the second phase
            sprites.fireball.init(g,s.rect,s)
        if s.phase == 1:
            s.drop = 120
        if s.phase == 2:
            s.drop = 90
    s.drop -= 1
    
    #sprite.check_standing(g,s)
    

def hit(g,a,b):
    g.game.sfx['boss_explode'].play()
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
    #player.damage(g,b)
    #print 'youve been spikeys!'

def bub_init(g,r):
    s = sprite.Sprite3(g,r,'big-bubble', (0,0,16,16))

    s.rect.centerx = r.centerx
    s.rect.centery = r.centery
    g.sprites.append(s)
    s.loop = bub_loop
                    
    v = random.randint(8,32)
    a = random.randint(0,360)*6.28/360
    s.vx = math.sin(a)*v
    s.vy = math.cos(a)*v
    s.frame = random.randint(0,FPS*2)
    return s
    
def bub_loop(g,s):
    s.vx *= 0.98
    s.vy *= 0.98
    s.rect.x += sprite.myinc(g.frame,s.vx)
    s.rect.y += sprite.myinc(g.frame,s.vy)
    s.frame += 1
    if s.frame >= FPS*2:
        s.active = False
        if random.randint(0,3) == 1:
            g.game.sfx['pop'].play()
