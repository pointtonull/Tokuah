from pygame.locals import *

SW,SH = 320,240
TW,TH = 16,16
FPS = 60
IROTATE = 64
#FPS = 10

TITLE = "Barbie Seahorse Adventures" #"Barbie Seahorse Adventures" #"Bubble Kong" # #"The Volcanic Rollercoaster Ride!"

SCALE2X = False  #use the scale2x scaler to make things look hi-res
LOWRES = False #keep it in 320x240 mode
FULL = True #

#INIT_BORDER = 100
#DEINIT_BORDER = 200
INIT_BORDER = TW*2
DEINIT_BORDER = TW*8


# Input for keyboard:
JUMP_KEYS = (K_SPACE, K_LCTRL, K_RCTRL, K_z)
BUBBLE_KEYS = (K_LALT, K_RALT, K_x)
LEFT_KEYS = (K_LEFT,)
RIGHT_KEYS = (K_RIGHT,)
UP_KEYS = (K_UP,)
DOWN_KEYS = (K_DOWN,)
MENU_KEYS = (K_RETURN,)
EXIT_KEYS = (K_ESCAPE,)

# Input for joystick/gamepad: (indexing start at zero)
JUMP_BUTTONS = (0,)
BUBBLE_BUTTONS = (1,)
HORIZONTAL_AXIS = (0,)
VERTICAL_AXIS = (1,)
MENU_BUTTONS = ()
EXIT_BUTTONS = ()

#Codes and codes and more codes!
CODE_BOUNDS = 0x13
CODE_PARROT_TURN = 0x22
CODE_PLATFORM_TURN = 0x34
CODE_FIREGUY_TURN = 0x39
CODE_FROG_TURN = 0x42
CODE_FROG_JUMP = 0x43
CODE_ROBO_TURN = 0x59
CODE_DOOR = 0x60
CODE_DOOR_AUTO = 0x61
CODE_DOOR_HIDDEN = 0x62
DOOR_CODES = [CODE_DOOR,CODE_DOOR_AUTO,CODE_DOOR_HIDDEN]
CODE_BROBO_TURN = 0x6A
CODE_BOUNDS = 0x70
CODE_EXIT = 0x88
CODE_SHOOTBOT_TURN = 0x99
CODE_BOSS_TURN = 0xA1
CODE_BOSS_PHASE2_BLOCK = 0xA2

# Various constants:
DOOR_DELAY = 20 # Delay when going through a door

#HACK: to have this function handy without a bunch of module.sign () blah blah
def sign(v):
    if v < 0: return -1
    if v > 0: return 1
    return 0
    
#HACK: some code to find out who's printing out trash
#import sys
#sys.stdout = None
    
