import pygame
from pygame.locals import *

from cnst import *

class Sprite:
    def __init__(self,r,n):
        self.rect = pygame.Rect(r)
        self.pos = r.centerx/TH,r.centery/TW
        self.image = n
        self.shape = pygame.Rect(0,0,TW,TH)
        self.exploded = 0
        self.loop = None
        
        self.hit_groups = set()
        self.hit = None
        self.groups = set()
        
        # needed for gravity to work / not work ... :)
        self.standing = None
        
        self.active = True
        
        self.deinit = deinit
        
        self.auto_gc = True
        
def Sprite2(g,r,n):
    s = Sprite(r,n)
    img = g.images[n]
    s.rect.w = s.shape.w = img.get_width()
    s.rect.h = s.shape.h = img.get_height()
    return s

def Sprite3(g,r,n,shape):
    shape = pygame.Rect(shape)
    s = Sprite(r,n)
    s.shape.x, s.shape.y = shape.x,shape.y
    s.rect.w = s.shape.w = shape.w
    s.rect.h = s.shape.h = shape.h
    return s

def apply_gravity(g,s):
    if s.standing != None:
        s.vy = 0 
        return
    s.vy += 0.2
    s.vy = min(s.vy,6)
    
def apply_standing(g,s):
    if s.standing == None: return
    if not s.standing.active:
        stop_standing(g,s)
        return
    a,b = s.rect,s.standing.rect
    a.bottom = b.top
    #if a.bottom != b.top or a.left > b.right or a.right < b.left:
    if a.left > b.right or a.right < b.left:
        stop_standing(g,s)
        s.rect.y += 1 #throw on a bit o' gravity
        return
        
def stop_standing(g,s):
    if hasattr(s.standing,'carrying'):
        if s in s.standing.carrying:
            s.standing.carrying.remove(s)
    s.standing = None
    
def deinit(g,s):
    if hasattr(s,'standing'):
        stop_standing(g,s)
    
    
def init_bounds(g,s):
    x,y = s.rect.centerx/TW,s.rect.centery/TH
    min_x,min_y,max_x,max_y = x,y,x,y
    while g.data[2][y][min_x] != CODE_BOUNDS: min_x -= 1
    while g.data[2][y][max_x] != CODE_BOUNDS: max_x += 1
    while g.data[2][min_y][x] != CODE_BOUNDS: min_y -= 1
    while g.data[2][max_y][x] != CODE_BOUNDS: max_y += 1
    min_x += 1
    min_y += 1
    g.bounds = pygame.Rect(min_x*TW,min_y*TH,(max_x-min_x)*TW,(max_y-min_y)*TH)
    
    g.view.w = min(SW,g.bounds.w)
    g.view.h = min(SH,g.bounds.h)
    
    #if g.bounds.w < SW:
        #print 'uh oh, g.bounds.w < SW',g.bounds.w
    #if g.bounds.h < SH:
        #print 'uh oh, g.bounds.h < SH',g.bounds.h
    
def init_view(g,s):
    g.view.centerx = s.rect.centerx
    g.view.centery = s.rect.centery
    s.pan(g,s)
    
def init_codes(g,s):
    g.view.clamp_ip(g.bounds)
    border = g.get_border(INIT_BORDER)
    g.run_codes(border)
        

    
def sign(v):
    if v < 0: return -1
    if v > 0: return 1
    return 0
    
def get_code(g,s,ix,iy):
    #dx,dy get taken down to their signed component
    dx,dy = sign(ix),sign(iy)
    r = s.rect
    x = [r.left,r.centerx,r.right][dx+1]
    y = [r.top,r.centery,r.bottom][dy+1]
    x = (x+dx)/TW + dx*max(0,abs(ix)-1)
    y = (y+dy)/TH + dy*max(0,abs(iy)-1)
    if x < 0 or y < 0 or x >= g.size[0] or y >= g.size[1]: return 0
    return g.data[2][y][x]

def myinc(f,i):
    #f - the current frame
    #i - a float to add to a number
    #returns - how much to add to your integer..
    r = 0
    s = sign(i)
    r = int(i)
    i -= r
    i = abs(i)
    c = 37 #an arbitrary prime number
    n = int(f*c*i)%c<int(c*i)
    r += s*n
    return r
