#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import pygame
from pygame.locals import *

from cnst import *

from spritesng import Player, Boss, Parrot, Spikey, Platform, Fireguy, Frog
from spritesng import Panda, Robo, Door, Brobo, Blob, Shootbot
import tiles_basic
from init import init_bkgr, init_bkgr_scroll, init_music

def _pass(*params):
    pass

INIT_CODES = {
    0x00    :[_pass],
    0x10    :[Player],
    0xA0    :[Boss],
}

CODES = {
#numerical codes for magic uses?
    0x00    :[_pass],
    0x01    :[_pass],
    0x02    :[_pass],
    0x03    :[_pass],
    0x04    :[_pass],
    0x05    :[_pass],
    0x06    :[_pass],
    0x07    :[_pass],
    0x08    :[_pass],
    0x09    :[_pass],
    0x0A    :[_pass],
    0x0B    :[_pass],
    0x0C    :[_pass],
    0x0D    :[_pass],
    0x0E    :[_pass],
    0x0F    :[_pass],

#player related (16 codes)
#0x10 ...
#0x13 ...

#parrot related (8 codes)
    0x20    :[Parrot, 1],
    0x21    :[Parrot, -1],
    0x22    :[_pass,], # CODE_PARROT_TURN

#spikey related (8 codes)
    0x28    :[Spikey],

# platform related (8 codes)
    0x30    :[Platform, 1, 0],
    0x31    :[Platform, 0, -1],
    0x32    :[Platform, -1, 0],
    0x33    :[Platform, 0, 1],
    0x34    :[_pass], # CODE_PLATFORM_TURN

# fireguy related (8 codes)

    0x38    :[Fireguy],
    0x39    :[_pass], # CODE_FIREGUY_TURN

# frog related (8 codes)
    0x40    :[Frog, 1],
    0x41    :[Frog, -1],
    0x42    :[_pass], # CODE_FROG_TURN
    0x43    :[_pass], # CODE_FROG_JUMP

# panda related (8 codes)
    0x48    :[Panda, 'left'],
    0x49    :[Panda, 'right'],

#fally related (8 codes)
    0x50    :[tiles_basic.fally_init],

# robo related (8 codes)
    0x58    :[Robo],
    0x59    :[_pass], # CODE_ROBO_TURN

#door related 
    0x60    :[Door], # CODE_DOOR (press shoot/up to be transported)
    0x61    :[_pass], # CODE_DOOR_AUTO (you are instantly transported)
    0x62    :[Door, True], # CODE_DOOR_HIDDEN (hidden regular door)

# brobo related
    0x68    :[Brobo, 'left'],
    0x69    :[Brobo, 'right'],
    0x6A    :[_pass], #CODE_BROBO_TURN

#level related
    0x70    :[_pass], #CODE_BOUNDS
    0x78    :[init_bkgr], # bkgr initializer
    0x79    :[init_bkgr_scroll, 0, 6], #bkgr scrolly magic stuff
    0x80    :[init_music], # music ..
    0x88    :[_pass], #CODE_EXIT

# blob related (8 codes)
    0x90    :[Blob],

# shootbot (8 codes)
    0x98    :[Shootbot],
    0x99    :[_pass], # CODE_SHOOTBOT_TURN

# boss related
    0xA1    :[_pass],
    0xA2    :[_pass],
}


def c_init(g, pos, n):
    x, y = pos
    if n not in INIT_CODES:
        if n not in CODES:
            print 'undefined code:', x, y, '0x%2x' % n
        return
    v = INIT_CODES[n]
    return v[0](g, pygame.Rect(x * TW, y * TH, TW, TH), n, *v[1:])

def c_run(g, pos, n):
    x, y = pos
    if n not in CODES:
        if n not in INIT_CODES:
            print 'undefined code:', x, y, '0x%2x' % n
        return
    v = CODES[n]
    return v[0](g, pygame.Rect(x * TW, y * TH, TW, TH), n, *v[1:])
