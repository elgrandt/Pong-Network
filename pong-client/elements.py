import global_knowns
import pygame
from gui import button
from sources import fonts
import json

class manager:
    def __init__(self,NETWORK):
        self.elements = []
        self.buttons = []
        self.NETWORK = NETWORK
        
        self.send = False
    def updateElements(self,elements):
        self.elements = elements
        
    def graphic_update(self,SCREEN):
        self.butsIds = []
        for x in range(len(self.elements)):
            self.getSurface(self.elements[x],SCREEN)
        for x in range(len(self.buttons)-1,-1,-1):
            bien = False
            for y in range(len(self.butsIds)):
                if (self.buttons[x]["ID"] == self.butsIds[y]):
                    bien = True
            if (not(bien)):
                del self.buttons[x]
        for x in range(len(self.buttons)):
            self.buttons[x]["button"].graphic_update(SCREEN)
    def logic_update(self,EVENTS):
	
        for x in range(len(self.buttons)):
            self.buttons[x]["button"].logic_update(EVENTS)
        for x in range(len(self.buttons)):
            if (self.buttons[x]["button"].button.pressed):
                self.NETWORK.protocol.sendData({"packet":global_knowns.button_pressed,"button":self.buttons[x]["ID"]})
        if (self.send):
            UP = EVENTS.get_keyboard()[pygame.K_UP]
            DOWN = EVENTS.get_keyboard()[pygame.K_DOWN]
            SPACE = EVENTS.get_keyboard()[pygame.K_SPACE]
            
            data = {"UP":UP,"DOWN":DOWN,"SPACE":SPACE}
            packet = {"packet":global_knowns.events,"data":data}
           
            self.NETWORK.protocol.sendData(packet)
    def getSurface(self,element,SCREEN):
        packet = element["object"]
        
        if (packet == global_knowns.ball):
            self.drawBall(element,SCREEN)
        elif (packet == global_knowns.bar):
            self.drawBar(element,SCREEN)
        elif (packet == global_knowns.join_button):
            if (not(self.buttonExist(element["ID"]))):
                but = button.text_button("Join", (200,200,200), (100,200,100), 5,2,fonts.ubg_30,fonts.ubg_35)
                but.set_position((element["x"],element["y"]))
                
                self.buttons.append({"ID":element["ID"],"button":but})
            self.butsIds.append(element["ID"])
    def drawBall(self,element,SCREEN):
        color = element["color"]
        POS = int(element["x"]),int(element["y"])
        RADIUS = int(element["radius"])
	print color,POS,RADIUS
        pygame.draw.circle(SCREEN,color,POS,RADIUS)
    def drawBar(self,element,SCREEN):
        color = element["color"]
        POS = element["x"],element["y"]
        DIM = element["width"],element["height"]
        surface = pygame.surface.Surface(DIM)
        surface.fill(color)
        SCREEN.blit(surface,POS)
    def buttonExist(self,ID):
        for x in range(len(self.buttons)):
            if (self.buttons[x]["ID"] == ID):
                return True
        return False
    def startSend(self):
        self.send = True
    def stopSend(self):
        self.send = False
