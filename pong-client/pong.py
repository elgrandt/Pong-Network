import pygame
import network
from gui import server_list,events,server_connect_menu,status_cur,loading
import gui
import global_knowns 
from twisted.internet import reactor,threads
import sys
import thread
import global_knowns as gk
import elements

class game:
    def __init__(self,IOSYS):
        self.IOSYS = IOSYS
        
        self.elements = []
        
        menu_connect = server_connect_menu.server_connect()
        menu_connect.set_position((300-menu_connect.W/2,200-menu_connect.H/2))
        
        self.mc = menu_connect
        self.elements.append(menu_connect)
        
        self.STATUS = "TOCONNECT"
        
    def handleData(self,data):
	
        if (data["packet"] == global_knowns.welcome):
            self.handleStart()
        elif (data["packet"] == gk.rooms_information):
            self.update_rooms(data["rooms"])
        elif (data["packet"] == gk.extra_rooms_info):
            self.update_room_extra(data["data"])
        elif (data["packet"] == gk.element_list):
            self.updateElements(data["data"])
        elif (data["packet"] == gk.start_game):
            self.startSendMove()
        elif (data["packet"] == gk.stop_game):
            self.endSendMove()
    def logic_update(self,EVENTS):
        
        for x in range(len(self.elements)):
            self.elements[x].logic_update(EVENTS)
        if (self.STATUS == "TOCONNECT"):
            self.update_menu_connect()
        elif (self.STATUS == "CONNECTING"):
            self.update_connecting()
        elif (self.STATUS == "ROOMLIST"):
            self.update_room_list()
        elif (self.STATUS == "ERROR"):
            self.update_error_connect()
        elif (self.STATUS == "GAME"):
            self.updateGame()
            
    def graphic_update(self,SCREEN):
        for x in range(len(self.elements)):
            self.elements[x].graphic_update(SCREEN)
            
    def update_menu_connect(self):
        if (self.mc.button_connect.button.pressed):
            self.start_connect(self.mc.get_host(),self.mc.get_port())
    def start_connect(self,host,port):
        self.mc.set_loading()
        self.STATUS = "CONNECTING"
        self.reactorStart( host,port,self.IOSYS.NETWORK)
    
    def update_connecting(self):
        pass
    def reactorStart(self,GAME_IP,GAME_PORT,connection):
        if (GAME_IP == "Host"):
            GAME_IP = "localhost"
            GAME_PORT = "9999"
        reactor.connectTCP(GAME_IP, int(GAME_PORT), connection)  # @UndefinedVariable
    def handleStart(self):
        
        self.elements = []
        sl = server_list(self.IOSYS.NETWORK)
        sl.set_position((0,0))
        self.elements.append(sl)
        
        self.sl = sl
        
        
        if (self.STATUS == "CONNECTING"):
            self.STATUS = "ROOMLIST"
            
        self.get_info()
    def handleFail(self):
        if (self.STATUS == "CONNECTING"):
            self.STATUS = "ERROR"
            self.mc.set_error()
    def update_room_list(self):
        if (self.sl.end == True):
            self.STATUS = "GAME"
            self.elements = []
            self.elementManager = elements.manager(self.IOSYS.NETWORK)
            self.elements.append(self.elementManager)
    def update_error_connect(self):
        
        if (self.mc.ta.button.pressed):
            x,y = self.mc.X,self.mc.Y
            self.mc.__init__()
            self.mc.set_position((x,y))
            self.STATUS = "TOCONNECT"
    def get_info(self):
        self.IOSYS.NETWORK.protocol.sendData({"packet":gk.get_rooms_information})
    def update_rooms(self,data):
        self.sl.update(data)
    def update_room_extra(self,data):
        if (self.STATUS == "ROOMLIST"):
            self.sl.update_extra(data)
    def updateGame(self):
        pass
    def updateElements(self,data):
        if (self.STATUS == "GAME"):
            self.elementManager.updateElements(data)
    def startSendMove(self):
        self.elementManager.startSend()
    def stopSendMove(self):
        self.elementManager.stopSend()
class iosys:
    def __init__(self):
        #OUTPUT
        self.SCREEN = pygame.display.set_mode((600,400))
        #INPUT
        self.EVENTS = events.events()
        #LOGIC
        self.GAME = game(self)
        #NETWORK
        self.NETWORK = network.gameClientFactory(self.GAME)
        #CLOCK   
        self.CLOCK = pygame.time.Clock()
        
        #ON
        self.ON = True
        
    def updating(self):
        if (True):  
            
            self.SCREEN.fill((255,255,255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitGame()
            self.EVENTS.update_keyboard(pygame.key.get_pressed())
            self.EVENTS.update_mouse(pygame.mouse.get_pos(),pygame.mouse.get_pressed())
            
            self.GAME.logic_update(self.EVENTS)
            self.GAME.graphic_update(self.SCREEN)
            
            status_cur.update()
            pygame.display.update()
        reactor.callLater(1./40,self.updating)# @UndefinedVariable
        
    def quitGame(self):
        reactor.stop()# @UndefinedVariable
        pygame.quit()
def main():
    pygame.init()
    io = iosys()
    io.updating()
    
    reactor.run()# @UndefinedVariable
    
main()
