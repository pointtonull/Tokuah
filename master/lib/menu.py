import os

import pygame
from pygame.locals import *

from pgu import engine

import data

from cnst import *

import levels

class Menu(engine.State):
    def __init__(self,game):
        self.game = game
        
    def init(self):
        self.font = self.game.font
        self.bkgr = pygame.image.load(data.filepath(os.path.join('bkgr','2.png')))
        
        self.cur = 0
        self.game.lcur = 0
        self.levels = levels.LEVELS
        
        self.items = [
            ('play the game!','start'),
            ('select <L>','play'),
            ('help','help'),
            ('credits','credits'),
            ('quit','quit'),
            ]
        self.rects = []
        
        self.frame = 0
        
        self.logo = pygame.image.load(data.filepath(os.path.join('title.png')))
        
    def debug_mode(self):
        self.levels = []
        for fname in os.listdir(data.filepath('levels')):
            if fname[0]=='.': continue
            self.levels.append((fname,fname.replace('.tga','')))
        self.levels.sort()
        levels.LEVELS = self.levels
        #print levels.LEVELS

        
    def paint(self,screen):
        x = self.frame%(self.bkgr.get_width())
        screen.blit(self.bkgr,(-x,0))
        screen.blit(self.bkgr,(-x+self.bkgr.get_width(),0))
        
        
        
        #x,y = 0,4
        x,y = 0,0
        
        #fnt = self.game.fonts['title']
        #c =(0,0,0)
        #text = TITLE
        #img = fnt.render(text,1,c)
        #screen.blit(img,((SW-img.get_width())/2,y))
        
        screen.blit(self.logo,((SW-self.logo.get_width())/2,y))
        #y += 48
        y = 132
        
        fnt = self.font
        
        text = 'high: %05d'%self.game.high
        c = (0x00,0x00,0x00)
        img = fnt.render(text,1,c)
        x = (SW-img.get_width())/2
        screen.blit(img,(x+1,y+1))
        c = (0xff,0xff,0xff)
        img = fnt.render(text,1,c)
        screen.blit(img,(x,y))
        #y += 36
        y += 24
        
        x = 90
        for n in xrange(0,len(self.items)):
            text,value = self.items[n]
            text = text.replace('L',self.levels[self.game.lcur][1])
            c = (0x00,0x00,0x00)
            img = fnt.render(text,1,c)
            x = (SW-img.get_width())/2
            screen.blit(img,(x+1,y+1))
            c = (0xff,0xff,0xff)
            if n == self.cur: c = (0xaa,0xaa,0xaa)
            img = fnt.render(text,1,c)
            screen.blit(img,(x,y))
            #y += 24
            y += 12
            
            
        text = 'www.imitationpickles.org'
        c = (0x00,0x00,0x00)
        img = fnt.render(text,1,c)
        x = (SW-img.get_width())/2
        y = SH-(img.get_height()+4)
        screen.blit(img,(x+1,y+1))
        c = (0xff,0xff,0xff)
        img = fnt.render(text,1,c)
        screen.blit(img,(x,y))

            
        self.game.flip()
        
    def update(self,screen):
        return self.paint(screen)
    
    def loop(self):
        self.game.music_play('title')
        self.frame += 1
            
    def event(self,e):
        if e.type is USEREVENT and e.action == 'down':
            self.cur = (self.cur+1)%len(self.items)
            self.repaint()
        elif e.type is USEREVENT and e.action == 'up':
            self.cur = (self.cur-1+len(self.items))%len(self.items)
            self.repaint()
        elif e.type is USEREVENT and e.action == 'left':
            self.game.lcur = (self.game.lcur-1+len(self.levels))%len(self.levels)
            self.cur = 1
            self.repaint()
        elif e.type is USEREVENT and e.action == 'right':
            self.game.lcur = (self.game.lcur+1)%len(self.levels)
            self.cur = 1
            self.repaint()
        elif e.type is USEREVENT and e.action == 'exit':
            return engine.Quit(self.game)
        elif e.type is USEREVENT and (e.action == 'menu' or e.action == 'jump'):
            text,value = self.items[self.cur]
            if value == 'start':
                self.game.init_play()
                self.game.lcur = 0
                import level
                l =  level.Level(self.game,None,self)
                return Transition(self.game,l)
            elif value == 'play':
                self.game.init_play()
                import level
                l =  level.Level(self.game,None,self)
                return Transition(self.game,l)
            elif value == 'quit':
                return engine.Quit(self.game)
            elif value == 'credits':
                return Transition(self.game,Credits(self.game,self))
            elif value == 'help':
                return Transition(self.game,Help(self.game,self))
        elif e.type is KEYDOWN and e.key == K_d:
            self.debug_mode()
    
class Transition(engine.State):
    def __init__(self,game,next):
        self.game,self.next = game,next
    
    def init(self):
        self.s1 = self.game.screen.convert()
        self.init2()
        self.frame = 0
        self.total = FPS
        self.inc = 0
        
    def init2(self):
        if hasattr(self.next,'init') and not hasattr(self.next,'_init'):
            self.next._init = 0
            self.next.init()
        self.s2 = self.game.screen.convert()
        self.next.paint(self.s2)
        

        
    def loop(self):
        #self.frame += 1
        self.inc += 1
        #if (self.inc%2) == 0: self.frame += 1
        self.frame += 1
        if self.frame == self.total:
            self.game.screen.blit(self.s2,(0,0))
            self.game.flip()
            return self.next
        
    def update(self,screen):
        return self.paint(screen)
    
    def paint(self,screen):
        f = self.frame
        t = self.total
        t2 = t/2
        
        if f < t2:
            i = self.s1
            w = max(2,SW * (t2-f) / t2)
            i = pygame.transform.scale(i,(w,SH*w/SW))
        else:
            f = t2-(f-t2)
            i = self.s2
            w = max(2,SW * (t2-f) / t2)
            i = pygame.transform.scale(i,(w,SH*w/SW))
            
        i = pygame.transform.scale(i,(SW,SH))
        
        screen.blit(i,(0,0))
        self.game.flip()
        
        
        
class Intro(engine.State):
    def __init__(self,game,next):
        self.game = game
        self.next = next
        
    def init(self):
        self.frame = FPS
        
        self.moon = pygame.image.load(data.filepath(os.path.join('intro','moon2.png'))).convert()
        self.black = self.moon.convert()
        self.black.fill((0,0,0))
        
    def update(self,screen):
        return self.paint(screen)

    def loop(self):
        self.frame += 1
        if self.frame == FPS*7:
            return Transition(self.game,Intro2(self.game,self.next))
        
    def event(self,e):
        if e.type is KEYDOWN or (e.type is USEREVENT and e.action in ('jump','bubble','menu','exit')):
            return Transition(self.game,self.next)
        
    def paint(self,screen):
        screen.fill((0,0,0))
        f = self.frame
        
        inc = FPS
        if 0 < f < inc:
            pass
        f -= inc
        
        inc = FPS*7
        if 0 < f < inc:
            
            a = 255
            if f > FPS*2:
                screen.blit(self.moon,(0,0))
                a = 255- ((f-FPS*2)*255/(FPS*2))
                self.black.set_alpha(a)
                screen.blit(self.black,(0,0))

            fnt = self.game.fonts['intro']
            x,y = 8,0
            for text in ['... July 20, 1969','man first','walked on','the moon.']:
                c = (255,255,255)
                img = fnt.render(text,1,(0,0,0))
                screen.blit(img,(x+2,y+2))
                img = fnt.render(text,1,c)
                screen.blit(img,(x,y))
                y += 36
            if f < FPS:
                a = 255-(f*255/FPS)
                self.black.set_alpha(a)
                screen.blit(self.black,(0,0))
        
        self.game.flip()
        
class Intro2(engine.State):
    def __init__(self,game,next):
        self.game = game
        self.next = next
        
    def init(self):
        self.moon = pygame.image.load(data.filepath(os.path.join('intro','moon2.png'))).convert()
        img = pygame.image.load(data.filepath(os.path.join('images','player','right.png')))
        w = 160
        self.player = pygame.transform.scale(img,(w,img.get_height()*w/img.get_width()))
        
        self.bkgr = pygame.image.load(data.filepath(os.path.join('bkgr','2.png')))
         
        self.frame = 0
         
    def loop(self):
        self.frame += 1
        if self.frame == FPS*2:
            return Transition(self.game,self.next)
    
    def event(self,e):
        if e.type is KEYDOWN or (e.type is USEREVENT and e.action in ('jump','bubble','menu','exit')):
            return Transition(self.game,self.next)
        
    def paint(self,screen):
        #screen.fill((0,0,0))
        screen.blit(self.bkgr,(0,0))
        fnt = self.game.fonts['intro']
        x,y = 8,0
        for text in ['This is','the year','of the','seahorse!']:
            c = (255,255,255)
            img = fnt.render(text,1,(0,0,0))
            screen.blit(img,(x+2,y+2))
            img = fnt.render(text,1,c)
            screen.blit(img,(x,y))
            y += 36
        screen.blit(self.player,(130,0))
            
        self.game.flip()
        
class Prompt(engine.State):
    def __init__(self,game,text,yes,no):
        self.game = game
        self.text = text
        self.yes = yes
        self.no = no
        
    def init(self):
        self.font = self.game.fonts['pause']
        self.bkgr = self.game.screen.convert()
        
    def event(self,e):
        if e.type is KEYDOWN and e.key == K_y:
            return self.yes
        if e.type is KEYDOWN and e.key == K_n:
            return self.no
        
    def paint(self,screen):
        screen.blit(self.bkgr,(0,0))
        text = self.text
        fnt = self.font
        c = (255,255,255)
        img = fnt.render(text,1,(0,0,0))
        x,y = (SW-img.get_width())/2,(SH-img.get_height())/2
        screen.blit(img,(x+2,y+2))
        img = fnt.render(text,1,c)
        screen.blit(img,(x,y))
        self.game.flip()
        
        
class Pause(engine.State):
    def __init__(self,game,text,next):
        self.game = game
        self.text = text
        self.next = next
        
    def init(self):
        self.font = self.game.fonts['pause']
        self.bkgr = self.game.screen.convert()
        
    def event(self,e):
        if e.type is KEYDOWN or (e.type is USEREVENT and e.action in ('jump','bubble','menu','exit')):
            return self.next
        
    def paint(self,screen):
        screen.blit(self.bkgr,(0,0))
        text = self.text
        fnt = self.font
        c = (255,255,255)
        img = fnt.render(text,1,(0,0,0))
        x,y = (SW-img.get_width())/2,(SH-img.get_height())/2
        screen.blit(img,(x+2,y+2))
        img = fnt.render(text,1,c)
        screen.blit(img,(x,y))
        self.game.flip()
        
            

class Credits(engine.State):
    def __init__(self,game,next):
        self.game = game
        self.next = next
        
    def init(self):
        self.frame = 0
        
        self.bkgr = pygame.image.load(data.filepath(os.path.join('bkgr',"5.png"))).convert()
        
    def update(self,screen):
        return self.paint(screen)
        pass

    def loop(self):
        self.frame += 1
        #if self.frame == FPS*7:
            #return Transition(self.game,Intro2(self.game,self.next))
        
    def event(self,e):
        if e.type is KEYDOWN or (e.type is USEREVENT and e.action in ('jump','bubble','menu','exit')):
            return Transition(self.game,self.next)
        
    def paint(self,screen):
        x = self.frame%(self.bkgr.get_width())
        screen.blit(self.bkgr,(-x,0))
        screen.blit(self.bkgr,(-x+self.bkgr.get_width(),0))

        fnt = self.game.fonts['help']
        x,y = 8,10
        for text in [
            'Core Team',
            '',
            'philhassey - director, code, levels',
            'trick - tiles, sprites',
            'pekuja - code, levels',
            'tim - music, levels',
            'DrPetter - backgrounds, sfx',
            '',
            'Also thanks to:',
            'fydo (level), Lerc (gfx), Tee (level)',
            ]:
            c = (255,255,255)
            img = fnt.render(text,1,(0,0,0))
            x = (SW-img.get_width())/2
            screen.blit(img,(x+2,y+2))
            img = fnt.render(text,1,c)
            screen.blit(img,(x,y))
            y += 20
        self.game.flip()



class Help(engine.State):
    def __init__(self,game,next):
        self.game = game
        self.next = next
        
    def init(self):
        self.frame = 0
        
        self.bkgr = pygame.image.load(data.filepath(os.path.join('bkgr',"5.png"))).convert()
        
    def update(self,screen):
        return self.paint(screen)
        pass

    def loop(self):
        self.frame += 1
        #if self.frame == FPS*7:
            #return Transition(self.game,Intro2(self.game,self.next))
        
    def event(self,e):
        if e.type is KEYDOWN or (e.type is USEREVENT and e.action in ('jump','bubble','menu','exit')):
            return Transition(self.game,self.next)
        
    def paint(self,screen):
        x = self.frame%(self.bkgr.get_width())
        screen.blit(self.bkgr,(-x,0))
        screen.blit(self.bkgr,(-x+self.bkgr.get_width(),0))

        fnt = self.game.fonts['help']
        x,y = 8,10
        for text in [
            'Help',
            '',
            'Use your arrow keys to',
            'move the seahorse.',
            'Button 1 - Jump',
            'Button 2 - Shoot',
            '',
            'Enemies take 3 shots unless',
            'you are powered up!  You can',
            'ride enemy bubbles.',
            ]:
            c = (255,255,255)
            img = fnt.render(text,1,(0,0,0))
            x = (SW-img.get_width())/2
            screen.blit(img,(x+2,y+2))
            img = fnt.render(text,1,c)
            screen.blit(img,(x,y))
            y += 20
        self.game.flip()





