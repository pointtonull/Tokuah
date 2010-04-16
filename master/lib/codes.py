import pygame
from pygame.locals import *

from cnst import *

import sprites
import init

def _pass(*params): pass

INIT_CODES = {
0x00    :[_pass,],
0x10    :[sprites.player.init,],
0xA0    :[sprites.boss.init,],
}

CODES = {
#numerical codes for magic uses?
0x00    :[_pass,],
0x01    :[_pass,],
0x02    :[_pass,],
0x03    :[_pass,],
0x04    :[_pass,],
0x05    :[_pass,],
0x06    :[_pass,],
0x07    :[_pass,],
0x08    :[_pass,],
0x09    :[_pass,],
0x0A    :[_pass,],
0x0B    :[_pass,],
0x0C    :[_pass,],
0x0D    :[_pass,],
0x0E    :[_pass,],
0x0F    :[_pass,],

#player related (16 codes)
#0x10 ...
#0x13 ...

#parrot related (8 codes)
0x20    :[sprites.parrot.init,1],
0x21    :[sprites.parrot.init,-1],
0x22    :[_pass,], # CODE_PARROT_TURN

#spikey related (8 codes)
0x28    :[sprites.spikey.init,],

# platform related (8 codes)
0x30    :[sprites.platform.init,1,0],
0x31    :[sprites.platform.init,0,-1],
0x32    :[sprites.platform.init,-1,0],
0x33    :[sprites.platform.init,0,1],
0x34    :[_pass,], # CODE_PLATFORM_TURN

# fireguy related (8 codes)

0x38    :[sprites.fireguy.init,],
0x39    :[_pass,], # CODE_FIREGUY_TURN

# frog related (8 codes)
0x40    :[sprites.frog.init,1],
0x41    :[sprites.frog.init,-1],
0x42    :[_pass,], # CODE_FROG_TURN
0x43    :[_pass,], # CODE_FROG_JUMP

# panda related (8 codes)
0x48    :[sprites.panda.init,'left',],
0x49    :[sprites.panda.init,'right',],

#fally related (8 codes)
0x50    :[sprites.tiles_basic.fally_init,],

# robo related (8 codes)
0x58    :[sprites.robo.init,],
0x59    :[_pass,], # CODE_ROBO_TURN

#door related 
0x60    :[sprites.door.init,], # CODE_DOOR (press shoot/up to be transported)
0x61    :[_pass,], # CODE_DOOR_AUTO (you are instantly transported)
0x62    :[sprites.door.init,True], # CODE_DOOR_HIDDEN (hidden regular door)

# brobo related
0x68    :[sprites.brobo.init,'left'],
0x69    :[sprites.brobo.init,'right'],
0x6A    :[_pass,], #CODE_BROBO_TURN

#level related
0x70    :[_pass,], #CODE_BOUNDS
0x78    :[init.init_bkgr,], # bkgr initializer
0x79    :[init.init_bkgr_scroll,0,6], #bkgr scrolly magic stuff
0x80    :[init.init_music,], # music ..
0x88    :[_pass,], #CODE_EXIT

# blob related (8 codes)
0x90    :[sprites.blob.init,],

# shootbot (8 codes)
0x98    :[sprites.shootbot.init,],
0x99    :[_pass,], # CODE_SHOOTBOT_TURN

# boss related
0xA1    :[_pass,],
0xA2    :[_pass,],
}



def c_init(g,pos,n):
    x,y = pos
    if n not in INIT_CODES and n not in CODES:
        print 'undefined code:',x,y,'0x%2x'%n
        return
    if n not in INIT_CODES: return
    v = INIT_CODES[n]
    return v[0](g,pygame.Rect(x*TW,y*TH,TW,TH),n,*v[1:])

def c_run(g,pos,n):
    x,y = pos
    if n not in INIT_CODES and n not in CODES:
        print 'undefined code:',x,y,'0x%2x'%n
        return
    if n not in CODES: return
    v = CODES[n]
    return v[0](g,pygame.Rect(x*TW,y*TH,TW,TH),n,*v[1:])
