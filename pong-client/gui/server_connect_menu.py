import pygame
import input_text
import button
import add_border
import surface_gf
from sources.fonts import ubuntu_bold_graph_initial
import loading

class server_connect:
    def __init__(self):
        self.W = 320
        self.H = 170
        
        
        input_host = input_text.text_input()
        input_host.set_numbers_and_letters()
        input_host.text = "localhost"
        input_host.set_position(((self.W-input_host.W)/2,30))
        input_host.set_background((255,255,255))
        input_host.set_alpha_states(0.9,1)
        input_host.set_show_text("Host")
        surfaceHost = surface_gf.surface_gf(ubuntu_bold_graph_initial.render("Host:",0,(0,0,0)) , ((self.W-input_host.W)/2+10,10)  )
        self.host = input_host
        
        input_port = input_text.text_input()
        input_port.set_numbers_and_letters()
        input_port.set_position(((self.W-input_port.W)/2,90))
        input_port.set_background((255,255,255))
        input_port.set_alpha_states(0.9, 1)
        input_port.set_show_text("Port")
        self.port = input_port
        surfacePort = surface_gf.surface_gf( ubuntu_bold_graph_initial.render("Port:",0,(0,0,0)) , ((self.W-input_port.W)/2+10,70) )
        button_connect = button.text_button("Conectar", (100,200,100), (200,100,100), 10)
        button_connect.set_position(((self.W-button_connect.button.W)/2,140))
        
        self.elements = []
        
        self.button_connect = button_connect
        
        self.elements.append(input_host)
        self.elements.append(input_port)
        self.elements.append(button_connect)
        self.elements.append(surfaceHost)
        self.elements.append(surfacePort)
        
        self.X = 0
        self.Y = 0
        self.STATUS = "CONNECT"
    def set_position(self,position):
        self.X,self.Y = position
    def logic_update(self,EVENTS):
        EVENTS.generate_relative((self.X,self.Y))
        for x in range(len(self.elements)):
            self.elements[x].logic_update(EVENTS)
        EVENTS.delete_relative()
        
                
    def graphic_update(self,SCREEN):
        surface = pygame.surface.Surface((self.W,self.H),pygame.SRCALPHA,32)
        surface.convert_alpha()
        background = pygame.surface.Surface((self.W,self.H))
        background.fill((50,50,255))
        background.set_alpha(200)
        
        for x in range(len(self.elements)):
            self.elements[x].graphic_update(surface)
    
        
        add_border.add_border(surface)
        
        
        SCREEN.blit(background,(self.X,self.Y))
        SCREEN.blit(surface,(self.X,self.Y))
    def get_host(self):
        return self.host.text
    def get_port(self):
        return self.port.text
    def set_loading(self):
        self.elements = []
        load = loading.loading()
        load.set_position((self.W/2-load.W/2,self.H/2-load.H/2))
        self.elements.append(load)
    def set_error(self):
        self.elements = []
        surfaceError = ubuntu_bold_graph_initial.render("No se puede conectar",0,(0,0,0))
        element = surface_gf.surface_gf( surfaceError, (self.W/2-surfaceError.get_size()[0]/2 , 60) )
        
        buttonTryAgain = button.text_button("Intentar denuevo", (100,200,100), (200,100,100), 10)
        buttonTryAgain.set_position(((self.W- buttonTryAgain.button.W)/2,140))
        
        self.elements.append(element)
        self.elements.append(buttonTryAgain)
        
        self.ta = buttonTryAgain
        self.STATUS = "TA"