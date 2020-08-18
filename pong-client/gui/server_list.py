import pygame
import add_border
import area_movil
from sources.fonts import ubuntu_bold_graph_initial,ubuntu_bold_graph_pre
import button
import status_cur
import global_knowns as gk
import thread

class room_info:
    def __init__(self):
        self.with_info = False
        self.title = ""
        self.startText = ""
        self.time = ""
        
        self.X = 0
        self.Y = 0
        self.color = 200,200,255
    def set_title(self,title):
        self.title = title
    def set_start(self,start):
        if (start):
            self.startText = "Juego en curso"
        else:
            self.startText = "Juego no comenzado"
    def set_time(self,seconds,minutes):
        if (seconds < 10):
            add = "0"
        else:
            add = ""
        self.time = str(minutes) + ":" + add + str(seconds)
    def set_color(self,color):
        self.color = color
    def set_position(self,position):
        self.X,self.Y = position
    def logic_update(self,EVENTS):
        pass
    def graphic_update(self,SCREEN):
        surface = pygame.surface.Surface((185,400))
        surface.fill(self.color)
        
        textTitle = ubuntu_bold_graph_initial.render(self.title,0,(0,0,0))
        
        d = (surface.get_size()[0]-textTitle.get_size()[0])/2
        
        surface.blit(textTitle,(d,20))
        
        textStart = ubuntu_bold_graph_initial.render(self.startText,0,(0,0,0))
        
        d = (surface.get_size()[0]-textStart.get_size()[0])/2
        
        surface.blit(textStart,(d,50))
        
        textTime = ubuntu_bold_graph_initial.render(self.time,0,(0,0,0))
        d = (surface.get_size()[0]-textTime.get_size()[0])/2
        
        surface.blit(textTime,(d,80))
        
        SCREEN.blit(surface,(self.X,self.Y))
class server_option:
    def __init__(self):
        self.room_name = ""
        self.room_color = (200,200,200)
        self.room_players = 0
        self.room_max_players = 0
        self.X = 0
        self.Y = 0
        self.H = 20
        self.W = 370
        self.surface = pygame.surface.Surface((self.W,self.H))
        self.selected = False
        self.clicked = False
        self.ID = 0
        
        self.name = ""
    def set_position(self,position):
        self.X,self.Y = position
    def update(self,data):
        self.name = data["name"]
        self.room_color = data["color"]
        self.room_players = data["players"]
        self.room_max_players = data["max players"]
        self.ID = data["ID"]
    def logic_update(self,EVENTS):
        mouse = EVENTS.get_mouse()
        mx,my = mouse.get_position()
        pressed = mouse.get_pressed()
        surface = pygame.surface.Surface((self.W,self.H))
        
        clicked = False
        if (mx > self.X and mx < self.X+self.W and my > self.Y and my < self.Y+self.H):
            if (pressed[0]):
                clicked = True
                self.clicked = True
            status_cur.set_pointer()
            font = ubuntu_bold_graph_initial
            surface.fill((150,255,150))
            
        else:
            font = ubuntu_bold_graph_pre
            surface.fill((100,255,100))
        self.clicked = clicked
        if (self.selected):
            surface.fill((255,100,100))
            
        add_border.add_border(surface)
        
        text_name = font.render(self.name,0,(0,0,0))
        
        text_players = font.render(str(self.room_players)+"/"+str(self.room_max_players),0,(0,0,0))
        
        server_color = pygame.surface.Surface((16,16))
        server_color.fill(self.room_color)
        
        surface.blit(text_name,(5,(self.H-text_name.get_size()[1])/2))
        surface.blit(text_players,(250,(self.H-text_name.get_size()[1])/2))
        surface.blit(server_color,(self.W-18,2))
        
        self.surface = surface
        
        
    def graphic_update(self,SCREEN):
        SCREEN.blit(self.surface,(self.X,self.Y))
        
class server_list:
    def __init__(self,NETWORK):
        self.NETWORK = NETWORK
        self.rooms_area = area_movil.area_movil()
        self.rooms_area.set_surface_dimensions((400,370))
        self.rooms_area.set_position((0,0))
        self.rooms_area.enableA(15)
        self.rooms_area.disableB()
        self.options = []
        self.X = 0
        self.Y = 0
        self.surface = pygame.surface.Surface((600,400))
        
        self.room_info = room_info()
        self.room_info.set_position((415,0))
        
        self.buttonRefresh = button.text_button("Actualizar", (100,100,255), (255,100,100), 5)
        w = self.buttonRefresh.button.surfaceA.get_size()[0]
        self.buttonRefresh.set_position((200-w/2,370))
        self.buttonConnect = button.text_button("Conectar", (100,100,255),(255,100,100), 5)
        w = self.buttonConnect.button.surfaceA.get_size()[0]
        self.buttonConnect.set_position((400+185/2-w/2,345))
        
        self.selected = 0
        """
        d = []
        for x in range(30):
            d.append({"name":"Room "+str(x+1),"color":(255,100,100),"players":2,"max players":2})
        self.update(d)
        """
        self.lselected = False
        
        self.end = False
    def set_position(self,position):
        self.X,self.Y = position
    def update_extra(self,data):

        time = data["time"]
        start = data["start"]
        self.room_info.set_start(start)
        self.room_info.set_time(time["seconds"], time["minutes"])
    def update(self,data):
        opciones = []
        for x in range(len(data)):
            server = server_option()
            server.set_position((10,x*24+10))
            server.update(data[x])
            opciones.append(server)
        self.options = opciones   
    def graphic_update(self,SCREEN):
        self.surface.fill((100,100,255))
        
        add_border.add_border(self.surface)
        surfaceServers = pygame.surface.Surface((450,20+24*len(self.options)))
        surfaceServers.fill((100,100,255))
        for x in range(len(self.options)):
            self.options[x].graphic_update(surfaceServers)
       
        self.rooms_area.set_surface(surfaceServers)
        
        
        self.rooms_area.graphic_update(self.surface)
        
        pygame.draw.line(self.surface,(0,0,0),(0,400),(600,400))
        surfaceButtons = pygame.surface.Surface((600,30))
        surfaceButtons.fill((255,255,100))
        add_border.add_border(surfaceButtons)
        
        self.room_info.graphic_update(self.surface)
        
        self.surface.blit(surfaceButtons,(0,400))
        self.buttonConnect.graphic_update(self.surface)
        self.buttonRefresh.graphic_update(self.surface)
        
        add_border.add_border(self.surface)
        SCREEN.blit(self.surface,(self.X,self.Y))
    def logic_update(self,EVENTS):
        if (len(self.options) > 1):
            for x in range(len(self.options)):
                EVENTS.generate_relative((self.X,self.Y-self.rooms_area.yElevacion))
                self.options[x].logic_update(EVENTS)
                EVENTS.delete_relative()
                if (self.options[x].clicked):
                    self.selected = x
                    
            
            for x in range(len(self.options)):
                if (x != self.selected):
                    self.options[x].selected = False
            self.options[self.selected].selected = True
            self.room_info.set_title(self.options[self.selected].name)
            self.room_info.set_color(self.options[self.selected].room_color)
        if (self.selected != self.lselected):
            self.room_info.with_info = False
            self.room_info.__init__()
            self.room_info.set_position((415,0))
            
            ID = self.options[self.selected].ID
            self.takeExtra(ID)
        EVENTS.generate_relative((self.X,self.Y))
        self.rooms_area.logic_update(EVENTS)
        self.room_info.logic_update(EVENTS)
        self.buttonConnect.logic_update(EVENTS)
        self.buttonRefresh.logic_update(EVENTS)
        EVENTS.delete_relative()

        self.lselected = self.selected
        
        if (self.buttonConnect.button.pressed):
            self.connectRoom(self.options[self.selected].ID)
            self.end = True
    def takeExtra(self,room):
        self.NETWORK.protocol.sendData({"packet":gk.extra_rooms_info,"room":room})
    def connectRoom(self,room):
        self.NETWORK.protocol.sendData({"packet":gk.join_game,"room":room})
