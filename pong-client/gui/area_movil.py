'''
Created on Dec 19, 2013

@author: ariel
'''
#imports
import pygame
import moving_bar
from sources.fonts import Calibri

class area_movil:
    def __init__(self):
        self.elements = []
        self.positionX = 0
        self.positionY = 0
        
        self.set_surface_dimensions((200,400))
        self.set_position((0,0))
        
        self.wA = 0
        self.wB = 0
        
        self.disableA()
        self.disableB()
        
        self.enableA(5)
        self.disableB()
        
        self.xElevacion = 0
        self.yElevacion = 0
    def set_position(self,position):
        self.X,self.Y = position
    def set_surface(self,surface):
        self.surface = surface
        W,H = self.surface.get_size()
       
        if (self.barA):
            self.elements[self.get_element("Bar A")][1].set_scale(float(self.H)/float(H))
        if (self.barB):
            self.elements[self.get_element("Bar B")][1].set_scale(float(self.W)/float(W))
    def get_element(self,name):
        for x in range(len(self.elements)):
            if (self.elements[x][0] == name):
                return x
    def enableA(self,w = 10):
        valor = self.get_element("Bar A")
        if (valor != None):
            del self.elements[valor]
        self.barA = True
        self.wA = w
        bar = moving_bar.moving_bar()
        bar.set_background((255,255,255))
        bar.set_border((0,0,0))
        bar.set_bar_background((0,0,255))
        bar.set_dimensions((w,self.H))
        bar.set_position((self.W,self.wB))
        
        self.elements.append(["Bar A",bar])
    def enableB(self,w = 10):
        valor = self.get_element("Bar B")
        if (valor != None):
            del self.elements[valor]
            
        self.barB = True
        self.wB = w
        bar = moving_bar.moving_bar()
        
        bar.set_background((255,255,255))
        bar.set_border((0,0,0))
        bar.set_bar_background((0,0,255))
     
        bar.set_dimensions((w,self.W))
        bar.set_vertical_mode()
        bar.set_position((0,0))
        
        if (self.barA == True):
            self.enableA(self.wA)
            
        self.elements.append(["Bar B",bar])
    def disableA(self):
        self.barA = False
        self.wA = 0
        try:
            del self.elements[self.get_element("Bar A")]
        except:
            pass
    def disableB(self):
        self.barB = False
        self.wB = 0
        try:
            del self.elements[self.get_element("Bar B")]
        except:
            pass

    def set_surface_dimensions(self,dimensions):
        self.W,self.H = dimensions
        self.sfinal = pygame.surface.Surface((self.W,self.H))
    def update_final_surface(self):
        tW,tH = self.surface.get_size()
        
        netaW = tW - self.W
        netaH = tH - self.H
      
        self.xElevacion = netaW * self.positionX
        self.yElevacion = netaH * self.positionY
        
        final_surface = pygame.surface.Surface((self.W,self.H),pygame.SRCALPHA, 32)
        final_surface = final_surface.convert_alpha()
        final_surface.blit(self.surface,(-self.xElevacion,-self.yElevacion))
        
        self.sfinal = final_surface
    def logic_update(self,EVENTS):
        for x in range(len(self.elements)):
            EVENTS.generate_relative((self.X,self.Y))
            self.elements[x][1].logic_update(EVENTS)
            EVENTS.delete_relative()
        if (self.barA):
           
            self.elements[self.get_element("Bar A")][1].position
            self.positionY = self.elements[self.get_element("Bar A")][1].get_position()

        else:
            self.positionY = 0
        if (self.barB):
            self.positionX = self.elements[self.get_element("Bar B")][1].get_position()
        else:
            self.positionX = 0
    def graphic_update(self,SCREEN):
        final_surface = pygame.surface.Surface((self.W+self.wA,self.H+self.wB),pygame.SRCALPHA, 32)
        final_surface = final_surface.convert_alpha()
        for x in range(len(self.elements)):
            self.elements[x][1].graphic_update(final_surface)
        
        self.update_final_surface()
        final_surface.blit(self.sfinal,(0,self.wB))
        
        SCREEN.blit(final_surface,(self.X,self.Y))
        