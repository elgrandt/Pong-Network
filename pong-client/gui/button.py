import pygame
from sources.fonts import ubuntu_bold_graph_initial,ubuntu_bold_graph_pre
import add_border
import status_cur
class button:
    def __init__(self,surfaceA,surfaceB):
        self.surfaceA = surfaceA
        self.surfaceB = surfaceB
        self.surface = self.surfaceA
        self.X,self.Y = 0,0
        self.W,self.H = surfaceA.get_size()
    def set_position(self,position):
        self.X,self.Y = position
    def logic_update(self,EVENTS):
        mouse = EVENTS.get_mouse()
        mx,my = mouse.get_position()
        pressed = False
        if (mx > self.X and mx < self.X+self.W and my > self.Y and my < self.Y+self.H):
            self.surface = self.surfaceB
            status_cur.set_pointer()
            pressed = mouse.get_pressed()[0]
        else:
            self.surface = self.surfaceA
        

        self.pressed = pressed
    def graphic_update(self,SCREEN):
        SCREEN.blit(self.surface,(self.X,self.Y))
        
class text_button:
    def __init__(self,text,back1,back2,padA = 10,padB = 2,fontA = ubuntu_bold_graph_pre,fontB = ubuntu_bold_graph_initial):
        self.text = text
        
        
        textlon = fontA.render(text,0,(0,0,0))
        textlon2 = fontB.render(text,0,(0,0,0))
        
        image1 = pygame.surface.Surface((textlon.get_size()[0]+padA*2,textlon.get_size()[1]+padB*2))
        image1.fill(back1)
        image2 = pygame.surface.Surface((textlon.get_size()[0]+padA*2,textlon.get_size()[1]+padB*2))
        image2.fill(back2)
        add_border.add_border(image1)
        add_border.add_border(image2)
        
        image1.blit(textlon,(padA,padB))
        image2.blit(textlon2,((image2.get_size()[0]-textlon2.get_size()[0])/2,(textlon.get_size()[1]+padB*2-textlon2.get_size()[1])/2))
        
        self.button = button(image1,image2)
    def set_position(self,position):
        self.button.set_position(position)
    def logic_update(self,EVENTS):
        self.button.logic_update(EVENTS)
    def graphic_update(self,SCREEN):
        self.button.graphic_update(SCREEN)