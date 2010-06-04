import pygame
from pygame.locals import *

from cnst import *

import tiles_basic
from spritesng.tile import Tile, Tile_left, Tile_rigth, tile_to_sprite

# NOTE: If you add new tiles, use Tile for regular tiles.
#       Tile_left and Tile_rigth are for tiles that take up only half of the
#       16x16 tile, on the left or right side respectively.

TILES = {
#general purpose tiles
    0x00: [Tile,        [], None],
    0x01: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x02: [Tile,        ['solid'],  tiles_basic.hit_breakable, 1, 1, 1, 1],
    0x03: [Tile,        ['player'], tiles_basic.hit_fire],
    0x04: [Tile,        [], None], #black background tile
    0x05: [Tile,        [], None], #exit sign
    0x10: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x11: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0x12: [Tile,        ['solid'],  tiles_basic.hit_fally, 1, 1, 1, 1],
    0x14: [Tile,        ['bubble'], tiles_basic.hit_replace, 0x15],
    0x15: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x21: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],

#powerups and bonus items ...
    0x08: [Tile,        ['player'], tiles_basic.hit_power], #power-up
    0x0C: [Tile,        ['player'], tiles_basic.hit_life], #extra-life
    0x18: [Tile,        ['player'], tiles_basic.hit_item, 100], #points
    0x1A: [Tile,        ['player'], tiles_basic.hit_item, 250], #points
    0x1C: [Tile,        ['player'], tiles_basic.hit_item, 500], #points
    0x1E: [Tile,        ['player'], tiles_basic.hit_item, 1000], #points
    0x28: [Tile,        ['player'], tiles_basic.hit_coin], #coin

#jungle tiles (0x40...)
    0x40: [Tile_rigth,  ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0x41: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0x42: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0x43: [Tile_left,   ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0x44: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0x45: [Tile_rigth,  ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0x54: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0x55: [Tile_left,   ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0x64: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0x65: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0x70: [Tile_rigth,  ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0x71: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0x72: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0x73: [Tile_left,   ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0x74: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0x75: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],

#dirt floor set
    0x47: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x48: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x49: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x57: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x58: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x59: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x67: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x68: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x69: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x77: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x78: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x79: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],

#dirt floor set #2
    0x4A: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x4B: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x4C: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x5A: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x5B: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x5C: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x6A: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x6B: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x6C: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x7A: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x7B: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x7C: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],

#volcano tiles (0x80...)
    0x80: [Tile_rigth,  ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0x81: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0x82: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0x83: [Tile_left,   ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0x84: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0x85: [Tile_rigth,  ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0x94: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0x95: [Tile_left,   ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0xa4: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0xa5: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0xb0: [Tile_rigth,  ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0xb1: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0xb2: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0xb3: [Tile_left,   ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0xb4: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0xb5: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],

# volcano cave set
    0x87: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x88: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x89: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x97: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x98: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0x99: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0xA7: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0xA8: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0xA9: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0xB7: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0xB8: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0xB9: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],

#moon tiles (0xC0...)
    0xc0: [Tile_rigth,  ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0xc1: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0xc2: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0xc3: [Tile_left,   ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0xc4: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0xc5: [Tile_rigth,  ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0xd4: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0xd5: [Tile_left,   ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0xe4: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0xe5: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0xf0: [Tile_rigth,  ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0xf1: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0xf2: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0xf3: [Tile_left,   ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0xf4: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],
    0xf5: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 0, 0, 0],

# moon cave set
    0xC7: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0xC8: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0xC9: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0xD7: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0xD8: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0xD9: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0xE7: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0xE8: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0xE9: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0xF7: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0xF8: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
    0xF9: [Tile,        ['solid'],  tiles_basic.hit_block, 1, 1, 1, 1],
}


TANIMATE = [
#(starting_tile, animated list of frames incs),

# powerup
    (0x08,
        (0, ) * 23 +
        (1, ) * 3 +
        (2, ) * 3 +
        (3, ) * 3
    ),

# extra life
    (0x0C,
        (0, ) * 7 +
        (1, ) * 3 +
        (2, ) * 3 +
        (0, ) * 17
    ),

# veggies
    (0x18,
        (1, ) * 2 +
        (0, ) * 63
    ),

# points
    (0x1A,
        (0, ) * 16 +
        (1, ) * 2 +
        (0, ) * 49
    ),
    (0x1C,
        (0, ) * 33 +
        (1, ) * 2 +
        (0, ) * 30
    ),
    (0x1E, 
        (0, ) * 48 +
        (1, ) * 2 +
        (0, ) * 14
    ),

# coin
    (0x28,
        (0, ) * 4 +
        (1, ) * 4 +
        (2, ) * 4 +
        (3, ) * 4 +
        (4, ) * 4 +
        (5, ) * 4 +
        (6, ) * 4 +
        (7, ) * 4
    ),

# door
    (0x30,
        (0, ) * 1 +
        (1, ) * 45
    ),
]

TREPLACE = [
#(tile_to_replace, replace_with)
    (0x10, 0x00),
    (0x11, 0x00),
    (0x14, 0x00),
    (0x20, 0x00),
]

def t_put(game, pos, name):
    x, y = pos
    if name not in TILES:
        Tile(game, pygame.Rect(x * TW, y * TH, TW, TH), name, [], None)
        return
    v = TILES[name]
    v[0](game, pygame.Rect(x * TW, y * TH, TW, TH), name, *v[1:])
