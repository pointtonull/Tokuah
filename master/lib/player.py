import pygame
from pygame.locals import *

from cnst import *
import sprite
import sprites
import tiles

def init(g,r,n,*params):
    s = sprite.Sprite3(g,r,'player/right',(6,8,15-6,27-8)) #(0,0,19,25))#(43-14,8,28,48))
    s.rect.bottom = r.bottom
    s.rect.centerx = r.centerx
    s.groups.add('player')
    s.groups.add('solid')
    g.sprites.append(s)
    s.loop = loop
    s.vx = 0
    s.vy = 0
    s.walk_frame = 1
    s.jumping = 0
    s.facing = 'right'
    s.flash_counter = 0
    s.flash_timer = 0
    s.shooting = 0
    s.powered_up = False
    if hasattr(g.game, 'powerup'):
        s.powered_up = g.game.powerup
    s.powerup_transition = 0
    s.door_timer = None
    s.current_door = None
    s.door_pos = None
    g.player = s
    s.event = event
    s.pan = pan_screen
    s.damage = damage
    s.kill = kill
    s.god_mode = False
    s.death_counter = -1
    
    s._prev = pygame.Rect(s.rect)
    s._prev2 = pygame.Rect(s.rect)
    s.looking = False
    
    sprite.init_bounds(g,s)
    sprite.init_view(g,s)
    sprite.init_codes(g,s)
    s.no_explode = False
    
    return s
    
def event(g,s,e):
    #print 'player.event',e
    if s.door_timer != None or s.exploded > 0:
        return
    
    if e.type is USEREVENT and e.action == 'jump' and s.standing != None and s.jumping == 0 and s.vy == 0:
        sprite.stop_standing(g,s)
        #s.vy = -1.8
        s.vy = -0.5
        s.jumping = 1.4
        g.game.sfx['jump'].play()
    if e.type is USEREVENT and e.action == 'stop-jump':
        s.jumping = 0
        
    if e.type is USEREVENT and (e.action == 'up' or e.action == 'down'):
        if sprite.get_code(g,s,0,0) in DOOR_CODES:
            s.vx = 0
            s.vy = 0
            s.door_timer = DOOR_DELAY
            if s.current_door != None: # It should never be None actually...
                #print "door!"
                s.current_door.open = DOOR_DELAY
            s.image = None
            s.door_pos = s.rect.centerx/TW,s.rect.centery/TH
            #tiles.t_put(g,(x,y), 0x32)
            #tiles.t_put(g,(x,y-1), 0x22)
    if e.type is USEREVENT and e.action == 'bubble':
        if s.powered_up:
            sprites.bubble.init(g,s.rect,s,big=True)
        else:
            sprites.bubble.init(g,s.rect,s,big=False)
        s.shooting = 10
        
    if e.type is KEYDOWN and e.key == K_F10:
        powerup(g,s)
        s.god_mode = True
        
    #if e.type is KEYDOWN and e.key == K_F12:
        #1/0
        
        
def loop(g,s):
    s._prev2 = pygame.Rect(s.rect)
    
    if s.death_counter > 0:
        s.groups = set()
        if not s.no_explode:
            s.exploded += 1
            if s.exploded > FPS/2:
                s.image = None
        else:
            s.image = None
        s.death_counter -= 1
        return
    if s.death_counter == 0:
        g.status = 'dead'
        return 
    
    if s.exploded > 0:
        if s.powered_up:
            s.image = 'player/right'
        else:
            s.image = 'splayer/right'
        s.exploded -=1 
        return
        

        
    sprite.apply_gravity(g,s)
    sprite.apply_standing(g,s)

    if s.door_timer != None:
        if s.door_timer == 0:
            x,y = s.door_pos#s.rect.centerx/TW,s.rect.centery/TH
            import door
            #door.hit(g,g.layer[y][x],s)
            door.hit(g,(x,y),s)
            #tiles.t_put(g,(x,y), 0x30)
            #tiles.t_put(g,(x,y-1), 0x20)
            s.door_timer = None
        else:
            s.door_timer -= 1
            return

    inpt = g.game.input
    
    #if s.standing: s.rect.bottom = s.standing.rect.top
    
    #check if we hit the ceiling
    if not s.jumping and s.vy < 0 and s.rect.y == s._prev.y:
        s.vy = 0
        
    # We have universal input code now (>__>)
    #move by keyboard
    #keys = pygame.key.get_pressed()
    
    if s.jumping:
        #print s.vy
        s.vy -= s.jumping
        s.jumping = max(0,s.jumping-0.2)
    
    inc = 0.5 
    mx = 2
    if inpt.right and s.vx < mx:
        s.vx += inc
        s.facing = 'right'
    elif not inpt.right and s.vx > 0:    s.vx -= inc
    if inpt.left  and s.vx > -mx:
        s.vx -= inc
        s.facing = 'left'
    elif not inpt.left and s.vx < 0:    s.vx += inc

    
    s._prev = pygame.Rect(s.rect)

    vx,vy = s.vx,s.vy
    s.rect.x += vx
    s.rect.y += sprite.myinc(g.frame,s.vy)
    
    
    #if keys[K_UP]: vy -= 1
    #if keys[K_DOWN]: vy += 1
    
    if s.vy < 0:
        s.image = 'player/%s-jump' % (s.facing)
    elif s.shooting > 0:
        if s.shooting > 5:
            s.image = 'player/%s-shoot-1' % (s.facing)
        else:
            s.image = 'player/%s-shoot-2' % (s.facing)
        s.shooting -= 1
    elif inpt.right or inpt.left and s.standing:
        s.image = 'player/%s-walk-%s' % (s.facing, int(s.walk_frame))
        s.walk_frame += 0.2
        if s.walk_frame > 4:
            s.walk_frame = 1
    else:
        s.image = 'player/%s'%(s.facing)
    if s.flash_counter > 0:
        if s.flash_timer < 4:
            s.image = None
        if s.flash_timer == 0:
            s.flash_timer = 8
            s.flash_counter -= 1
        s.flash_timer -= 1
    if s.image != None:
        if s.powerup_transition > 0:
            if (s.powerup_transition % 10) > 5:
                s.image = 's' + s.image
            s.powerup_transition -= 1
        elif not s.powered_up:
            s.image = 's' + s.image
    
    s.looking = False
    if inpt.up:
        g.view.y -= 2
        s.looking = True
    if inpt.down:
        g.view.y += 2
        s.looking = True
    
    n = sprite.get_code(g,s,0,0) 
    if n == CODE_EXIT:
        g.status = 'exit'
    if n == CODE_DOOR_AUTO:
        x,y = s.rect.centerx/TW,s.rect.centery/TH
        import door
        door.hit(g,(x,y),s)

    
    #pan_screen(g,s)
    
    #if (g.frame%FPS)==0: print 'player vy:',s.vy

    if hasattr(g, 'boss'):
        #print g.boss.phase, g.boss.phase_frames
        if g.boss.phase == 2 and g.boss.phase_frames == 60:
            for y in xrange(len(g.layer)):
                for x in xrange(len(g.layer[y])):
                    if g.data[2][y][x] == CODE_BOSS_PHASE2_BLOCK:
                        tiles.t_put(g,(x,y),0x01) # solid tile
        if g.boss.dead:
            g.status = 'exit'
            #pygame.mixer.music.load("
            #g.game.music.play('finish',1)
    
    
def pan_screen(g,s):
    # adjust the view 
    border = pygame.Rect(s.rect)
    #pad = 100
    pad = (SW/2)-TW
    border.x -= pad
    border.w += pad*2
    #pad = 80
    pad = (SH/2)-TH
    if s.looking:
        pad = TH*2
    border.y -= pad
    border.h += pad*2
    
    dest = pygame.Rect(g.view)
    dest.top = min(dest.top,border.top)
    dest.right = max(dest.right,border.right)
    dest.bottom = max(dest.bottom,border.bottom)
    dest.left = min(dest.left,border.left)
    
    dx,dy = dest.x-g.view.x,dest.y-g.view.y
    #mx,my = 6,6
    mx = max(2,abs(s._prev2.x-s.rect.x))
    my = max(2,abs(s._prev2.y-s.rect.y))
    if abs(dx) > mx: dx = sign(dx)*mx
    if abs(dy) > my: dy = sign(dy)*my
    g.view.x += dx
    g.view.y += dy
    

def powerup(g,s):
    if not s.powered_up:
        s.powerup_transition = 100
        s.powered_up = True
        if hasattr(g.game, 'powerup'):
            g.game.powerup = True
    
def damage(g,s):
    if s.god_mode: return
    
    if s.door_timer != None:
        return
    
    if s.powered_up:
        g.game.sfx['pop'].play()
        s.powerup_transition = 100
        s.powered_up = False
        if hasattr(g.game, 'powerup'):
            g.game.powerup = False
    elif s.powerup_transition == 0 and s.flash_counter == 0:
        s.kill(g,s)
        
def kill(g,s,no_explode = False):
    if hasattr(g.game, 'powerup'):
        g.game.powerup = False
    s.flash_counter = 10
    s.no_explode = no_explode
    g.game.music_play('death',1)
    s.death_counter = int(FPS*2.25)
    
