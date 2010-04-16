'''Game main module.

Contains the entry point used by the run_game.py script.

Feel free to put all your game code here, or in other modules in this "lib"
directory.
'''

import sys
import os

import pygame
from pygame.locals import *

from pgu import timer
from pgu import engine

from cnst import *
import data

class Input:
    def __init__(self):
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        
class Sound:
    def __init__(self,fname):
        self.sound = None
        if pygame.mixer.get_init():
            try:
                self.sound = pygame.mixer.Sound(fname)
            except:
                pass

    def play(self):
        if self.sound:
            self.sound.stop()
            self.sound.play()

class Game(engine.Game):
    def init_play(self):
        self.score = 0
        self.high = 0
        self.lives = 2
        self.coins = 0
        self.powerup = False
        
    def init(self):
        self.random = 0
        
        self.init_play()
        self.lcur = 0

        self.scale2x = SCALE2X
        if '-scale2x' in sys.argv:
            self.scale2x = not self.scale2x
        self.lowres = LOWRES
        if '-lowres' in sys.argv:
            self.lowres = not self.lowres

        sw,sh = SW,SH
        if not self.lowres:
            sw,sh = sw*2,sh*2
        mode = 0
        if FULL: mode |= FULLSCREEN
        if '-full' in sys.argv:
            mode ^= FULLSCREEN
        self.screen = pygame.display.set_mode((sw,sh),mode)
        pygame.display.set_caption(TITLE)
        self.timer = timer.Timer(FPS)
        #self.timer = timer.Speedometer()

        pygame.joystick.init()
        joy_count = pygame.joystick.get_count()
        for joynum in range(joy_count):
            joystick = pygame.joystick.Joystick(joynum)
            joystick.init()
            
        self.input = Input()
        
        if not self.lowres:
            self._screen = self.screen
            self.screen = self._screen.convert().subsurface(0,0,SW,SH)
            
        pygame.font.init()
        
        f_main = data.filepath(os.path.join('fonts','04B_20__.TTF'))
        f_scale = 0.35
        #f_main = data.filepath(os.path.join('fonts','04B_25__.TTF'))
        #f_scale = 0.75
        #f_main = data.filepath(os.path.join('fonts','04B_11__.TTF'))
        #f_scale = 0.67
        
        self.fonts = {}
        self.fonts['intro'] = pygame.font.Font(f_main,int(36*f_scale))
        #self.fonts['intro2'] = pygame.font.Font(data.filepath(os.path.join('fonts','vectroid.ttf')),72)

        #self.fonts['title'] = pygame.font.Font(data.filepath(os.path.join('fonts','vectroid.ttf')),32)
        self.fonts['help'] = pygame.font.Font(f_main,int(24*f_scale))
        
        self.font = self.fonts['menu'] = pygame.font.Font(f_main,int(24*f_scale))
        
        self.fonts['level'] = pygame.font.Font(f_main,int(24*f_scale))
        
        self.fonts['pause'] = pygame.font.Font(f_main,int(36*f_scale))
        
        import level
        level.pre_load()
        
        try:
            
            
            if '-nosound' in sys.argv: 1/0
            
            # stop crackling sound on some windows XP machines.
            if os.name == 'posix' or 1:
                try:
                    pygame.mixer.pre_init(44100,-16,2, 1024*3)
                except:
                    pygame.mixer.pre_init()
            else:
                pygame.mixer.pre_init()

            
            pygame.mixer.init()
        except:
            print 'mixer not initialized'
        
        self._music_name = None
        
        self.sfx = {}
        for name in ['bubble','capsule','coin','hit','item','powerup',
            'pop','jump','explode','door','fally','boss_explode']:
            self.sfx[name] = Sound(data.filepath(os.path.join('sfx','%s.wav'%name)))
        
    def tick(self):
        r = self.timer.tick()
        if r != None: print r
        
    def flip(self):
        if not self.lowres:
            
            if self.scale2x:
                tmp = pygame.transform.scale2x(self.screen)#,(SW*2,SH*2))
                self._screen.blit(tmp,(0,0))
            else:
                # test version of pygame ..
                # if 1.8.x
                # pygame.transform.scale(self.screen,(SW*2,SH*2),self._screen)
                # else
                tmp = pygame.transform.scale(self.screen,(SW*2,SH*2))
                self._screen.blit(tmp,(0,0))
                
            # silly TV effect ...
            if '-tv' in sys.argv:
                for y in xrange(0,SH*2,2):
                    self._screen.fill((0,0,0),(0,y,SW*2,1))
            
        pygame.display.flip()
        
    def music_play(self,name,n=-1):
        if self._music_name == name: return
        self._music_name = name
        
        if not pygame.mixer.get_init(): return
        
        for ext in ['wav','ogg']:
            fname = data.filepath(os.path.join('music','%s.%s'%(name,ext)))
            ok = False
            try:
                #print fname
                pygame.mixer.music.load(fname)
                if len(name) == 1 or name == 'death':
                    pygame.mixer.music.set_volume(0.4)
                elif name == 'lvlwin':
                    pygame.mixer.music.set_volume(0.6)
                else:
                    pygame.mixer.music.set_volume(0.65)
                pygame.mixer.music.play(n)
                ok = True
            except:
                #import traceback; traceback.print_exc()
                pass
            if ok: break
        
    def event(self,e):
        # The keys, buttons and axis for the input can be changed in cnst.py

        self.random += 1 + self.random % 100 # this will generate pseudo random numbers

        event = None
        action = None
        if (e.type == KEYDOWN and e.key in JUMP_KEYS) or \
           (e.type == JOYBUTTONDOWN and e.button in JUMP_BUTTONS):
            action = 'jump'
        elif (e.type == KEYUP and e.key in JUMP_KEYS) or \
             (e.type == JOYBUTTONUP and e.button in JUMP_BUTTONS):
            action = 'stop-jump'
        elif e.type == KEYDOWN and e.key in BUBBLE_KEYS or \
            (e.type == JOYBUTTONDOWN and e.button in BUBBLE_BUTTONS):
            action = 'bubble'
        elif e.type == KEYDOWN or e.type == KEYUP:
            if e.type == KEYDOWN:
                value = True
            else:
                value = False
            if e.key in LEFT_KEYS:
                self.input.left = value
                if value: self.input.right = False
                action = 'left'
            if e.key in RIGHT_KEYS:
                self.input.right = value
                if value: self.input.left = False
                action = 'right'
            if e.key in UP_KEYS:
                self.input.up = value
                if value: self.input.down = False
                action = 'up'
            if e.key in DOWN_KEYS:
                self.input.down = value
                if value: self.input.up = False
                action = 'down'
            if e.type == KEYUP:
                action = None
        elif e.type == JOYAXISMOTION:
            if e.axis in HORIZONTAL_AXIS:
                if e.value < -0.6:
                    action = 'left'
                    self.input.left = True
                if e.value > -0.4:
                    self.input.left = False
                if e.value > 0.6:
                    action = 'right'
                    self.input.right = True
                if e.value < 0.4:
                    self.input.right = False
            if e.axis in VERTICAL_AXIS:
                if e.value < -0.6:
                    action = 'up'
                    self.input.up = True
                if e.value > -0.4:
                    self.input.up = False
                if e.value > 0.6:
                    action = 'down'
                    self.input.down = True
                if e.value < 0.4:
                    self.input.down = False
        if e.type is KEYDOWN and e.key in EXIT_KEYS:
            action = 'exit'
        elif e.type is JOYBUTTONDOWN and e.button in EXIT_BUTTONS:
            action = 'exit'
        elif e.type is KEYDOWN and e.key in MENU_KEYS:
            action = 'menu'
        elif e.type is JOYBUTTONDOWN and e.button in MENU_BUTTONS:
            action = 'menu'
        
        if action != None:
            event = pygame.event.Event(USEREVENT, action=action)

            self.fnc('event', event)
            return True
            
        if e.type is QUIT: 
            self.state = engine.Quit(self)
            return 1
        
        #if e.type is KEYDOWN and e.key == K_ESCAPE:
            #self.state = engine.Quit(self)
            #return 1
            
        
        if e.type is KEYDOWN and e.key == K_F4: #K_F12:
            
            try:
                dname = '.'
                if not os.path.exists(dname):
                    return
            except:
                return
            try:
                n = 1
                while n < 1000:
                    fname = os.path.join(dname,'shot%03d.bmp'%n)
                    if not os.path.exists(fname): break
                    n += 1
                self.flip()
                pygame.image.save(self._screen,fname)
                return 1
            except:
                pass



def main():
    #print "Hello from your game's main()"
    #print data.load('sample.txt').read()
    
    fname = None #data.filepath(os.path.join('levels','test.tga'))
    for v in sys.argv:
        if '.tga' in v:
            fname = v
            
    g = Game()
    g.init()
    import menu
    l = l2 = menu.Menu(g)
    #l = menu.Intro(g,l2)
    if fname != None:
        import level
        l = level.Level(g,fname,engine.Quit(g))
        
    g.run(l)
    pygame.quit()
