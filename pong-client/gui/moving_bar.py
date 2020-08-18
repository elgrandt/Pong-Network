
import pygame
import add_border

class moving_bar:
    def __init__(self):
        #setting backgrounds
        self.set_background((255,255,255))
        self.set_bar_background((0,0,0))
        #setting border
        self.set_border((0,0,0))
        #setting size
        self.set_dimensions((30,300))
        #setting size
        self.set_scale(1.0/4.0)
        #setting grid
        self.set_grid(1.0/8.0)
        #setting position 
        self.position = 0
        #setting X and Y
        self.set_position((0,0))
        #for the mouse saving
        self.mY = 0
        #saving if move
        self.moving = False
        #default mode
        self.mode = 0
        #the grid
        self.grid = False
    def set_vertical_mode(self):
        self.mode = 1
    def set_horizontal_mode(self):
        self.mode = 0
    def set_dimensions(self,dimensions):
        self.W, self.H = dimensions
        self.surface = pygame.surface.Surface((self.W,self.H))
    def set_border(self,border):
        self.border = border
    def set_background(self,background):
        self.background = background
    def set_bar_background(self,bar_background):
        self.bar_background = bar_background
    def set_scale(self,scale):
        self.scale = scale
    def set_grid(self,grid):
        self.grid = grid
    def set_position(self,pos):
        self.X,self.Y = pos
    def enableGrid(self):
        self.grid = True
    def disableGrid(self):
        self.grid = False
    def get_position(self):
        neto = self.position / (1.0-self.scale)
        return neto
    def foc(self,EVENTS):
        if (self.mode == 0):
            mx,my = EVENTS.get_mouse().get_position()
            return (mx > self.X and mx < self.X + self.W and my > self.Y and my < self.Y + self.H)
        else:
            my,mx = EVENTS.get_mouse().get_position()
            return (mx > self.Y and mx < self.Y + self.W and my > self.X and my < self.X + self.H)
    def update_bar_position(self,EVENTS):
        mx,my = EVENTS.get_mouse().get_position()
        if (self.mode == 0):
            position = float(my - self.Y)/float(self.H) - self.scale/2.0
        else:
            position = float(mx - self.X)/float(self.H) - self.scale/2.0
        if (position < 0):
            position = 0
        elif (position > 1.0-self.scale):
            position = 1.0-self.scale
        
        if (self.grid):
            position /= self.grid
            position = int(position)
            position *= self.grid
        
        self.position = position
    def logic_update(self,EVENTS):
        mouse = EVENTS.get_mouse()
        #creating the surface
        surface = pygame.surface.Surface((self.W,self.H))
        surface.fill(self.background)
        
        selection = pygame.surface.Surface((self.W,self.H*self.scale))
        selection.fill(self.bar_background)
        surface.blit(selection,(0,self.position*self.H))
        
        
        pressed = mouse.get_pressed()[0]
        if (self.foc(EVENTS)):
            if (pressed):
                self.moving = True
        if (not(pressed)):
            self.moving = False
        if (self.moving):     
            self.update_bar_position(EVENTS)
            
        surface = add_border.add_border(surface, (0,0,0))
        self.surface = surface
        
        self.pressed_aux = pressed
    def graphic_update(self,SCREEN):
        if (self.mode == 0):
            SCREEN.blit(self.surface,(self.X,self.Y))
        else:
            SCREEN.blit(pygame.transform.rotate(self.surface,90),(self.X,self.Y))