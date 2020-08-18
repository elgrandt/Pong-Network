from twisted.internet import reactor,threads

import random
import global_knowns
import pygame
import math

import connection
import os

def randomcolor():
    return random.randrange(256),random.randrange(256),random.randrange(256)
def sd(data,length):
    if (len(data) > length):
        data = data[0:length]
    elif(len(data) < length):
        while (len(data) < length):
            data += " "
    return data

class time:
    def __init__(self,s,m):
        self.seconds = s
        self.minutes = m
    def advance(self):
        if (self.seconds == 59):
            self.seconds = 0
            self.minutes += 1
        else:
            self.seconds += 1
    def get_js(self):
        return {"seconds":self.seconds,"minutes":self.minutes}
class ball:
    def __init__(self,color,position,ID):
        self.color = color
        self.x,self.y = position
        self.status = "PLAYING"
        self.angle = 30
        self.speed = 20
        self.RADIUS = 10
        self.ID = ID
    def run(self):
        self.status = "PLAYING"
    def update(self,SKIP):
        
        if (self.status == "PLAYING"):  
            x = self.x
            y = self.y
            
            x += math.sin(math.radians(self.angle)) * self.speed * SKIP
            y += math.cos(math.radians(self.angle)) * self.speed * SKIP
            
            if (y > 400-self.RADIUS or y < self.RADIUS):
                self.angle = 180 - self.angle
            elif (x > 600-self.RADIUS or x < self.RADIUS):
                self.angle = self.angle + (180-self.angle)*2
            else:
                self.x = x
                self.y = y
    def get_code(self):
        return {"object":global_knowns.ball,"color":self.color,"radius":self.RADIUS,"x":self.x,"y":self.y}
class bar:
    def __init__(self,position,color,ID):
        self.WIDTH = 10
        self.HEIGHT = 50
        self.x,self.y = position
        self.speed = 5
        self.ID = ID
        self.color = color
    def move_down(self):
        self.y += self.speed
    def move_up(self):
        self.y -= self.speed
    def update(self,SKIP):
        pass
    def get_code(self):
        return {"object":global_knowns.bar,"color":self.color,"width":self.WIDTH,"height":self.HEIGHT,"x":self.x,"y":self.y}
class player:
    def __init__(self,name,color,index,barId):
        self.name = name
        self.color = color
        self.points = 0
        self.index = index
        self.status = "CONNECTED"
        self.barId = barId
    def score(self):
        self.points+=1
    def get_points(self):
        return self.points
class join_button:
    def __init__(self,position,ID):
        self.x,self.y = position
        self.ID = ID
    def update(self,SKIP):
        pass
    def get_code(self):
        return {"object":global_knowns.join_button,"ID":self.ID,"x":self.x,"y":self.y}
class game:
    def __init__(self,name,color,ID,NETWORK):
        self.name = name
        self.start = False
        self.players = []
        
        self.color = color
        self.time = time(0,2)
        self.elements = []
        self.network = NETWORK
        
        my_ball = ball((50,200,50),(300-5,200-5),0)
        
        my_button_joinA = join_button((20,190),1)
        my_button_joinB = join_button((500,190),2)
        
        self.ball = my_ball
        self.add_element(my_ball,"Ball")
        self.add_element(my_button_joinA,"Button A")
        self.add_element(my_button_joinB,"Button B")
        
        
        self.indexId = 1
        self.ID = ID
        self.max_players = 2
        self.spectators = []
    
        self.bars = []
    def add_element(self,element,name):
        self.elements.append({"element":element,"name":name})
    def get_spectators(self):
        return self.spectators
    def join_spectator(self,name,index):
        self.spectators.append({"name":name,"ID":index})
    def unjoinPlayer(self,y):
        del self.spectators[y]
    def join_player(self,name,color,index):
        if len(self.players) > 2:
            return False
        
        if (len(self.players) == 0):
            mybar = bar((20,275),(0,0,255),self.indexId)
            new_player = player(name,color,index,self.indexId)
        
        else:
            mybar = bar((870,275),(255,0,0),self.indexId)
            new_player = player(name,color,index,self.indexId)
        self.players.append(new_player)
        self.elements.append(mybar)
        
        self.indexId += 1
    def sp(self,index):
        for x in range(len(self.players)):
            if (self.players.index == index):
                return x
    def se(self,ID):
        for x in range(len(self.elements)):
            if (self.elements[x].ID == ID):
                return x
    def gp(self,ID):
        return self.elements[ self.se(ID) ]
    def gbn(self,name):
        for x in range(len(self.elements)):
            if (self.elements[x]["name"] == name):
                return x
    def disconnect_player(self,index):
        self.players[self.sp(index)].status = "DISCONNECTED"
    
    def update_players_events(self,index,keys):
        bar = self.elements[ self.se( self.players[self.sp(index)].barId ) ]
        if (keys[pygame.K_DOWN]):
            bar.y += bar.speed
        if (keys[pygame.K_UP]):
            bar.y -= bar.speed
    def logic_update(self,SKIP):
        for x in range(len(self.elements)):
            self.elements[x]["element"].update(SKIP)
    def get_codes(self,index):
        codes = []
        noButtonJoin = False
        if (self.isPlaying(index)):
            noButtonJoin = True
        for x in range(len(self.elements)):
            if (noButtonJoin and (self.elements[x]["name"] == "Button A" or self.elements[x]["name"] == "Button B")):
                continue
            codes.append(self.elements[x]["element"].get_code())
        return codes
    def get_extra_info(self):
        data = {"start":self.start,"time":self.time.get_js()}
        return data
    
    def buttonPressed(self,button_id,index):
        try:
            if (button_id == 1):
                del self.elements[ self.gbn("Button A") ]
                self.join_player_1(index)
            elif (button_id == 2):
                del self.elements[ self.gbn("Button B") ]
                self.join_player_2(index)
        except:
            pass
    def handleEvents(self,events,index):
        player = self.get_player_is(index)
        if (player != 1 and player != 2):
            return 0
        elif (player == 1):
            element = self.elements[ self.gbn("Bar A") ]["element"]
        elif (player == 2):
            element = self.elements[ self.gbn("Bar B") ]["element"]
        else:
            return 0
        
        if (events["SPACE"]):
            element.speed = 7
        else:
            element.speed = 5
        if (events["UP"] and events["DOWN"]):
            pass
        elif (events["UP"]):
            element.move_up()
        elif (events["DOWN"]):
            element.move_down()
    def add_player(self,index,side):
        self.players.append({"player":index,"side":side})
    def isPlaying(self,index):
        for x in range(len(self.players)):
            if (self.players[x]["player"] == index):
                return True
        return False
    def get_player_is(self,index):
        for x in range(len(self.players)):
            if (self.players[x]["player"] == index):
                return self.players[x]["side"]
        return 0
    def get_player(self,index):
        for x in range(len(self.players)):
            if (self.players["player"] == index):
                return x
    def join_player_1(self,index):
        barA = bar((20,200-25), (0,0,255), 1)
        
        self.add_element(barA,"Bar A")
        self.bars.append(barA)
        
        self.add_player(index,1)
        self.check_start()
        
        self.network.sendDataTo(index,{"packet":global_knowns.start_game})
    def join_player_2(self,index):
        barB = bar((600-30,200-25), (0,0,255), 2)
        
        self.add_element(barB, "Bar B")
        self.bars.append(barB)
        
        self.add_player(index,2)
        self.check_start()
        
        self.network.sendDataTo(index,{"packet":global_knowns.start_game})
    def check_start(self):
        print "check-start"
        print len(self.players)
        if (len(self.players) == 2):
            self.start_game()
    def start_game(self):
        self.ball.status = "PLAYING"
        self.ball.color = (100,100,255)
        self.ball.angle = random.randrange(360)
class gameHandler:
    def __init__(self):
        self.connection = connection.Gamefactory(self)
        
        
        self.iId = 1
        self.rooms = []
        
        
        for x in range(5):
            self.add_game("Sala "+str(x+1), randomcolor())
        
        self.on = True
        
        
        
        
        threads.callMultipleInThread([(self.commands_loop,[],{})])
        
        self.loop(1)
        port = 10000
        while True:
            port-=1
            try:
                reactor.listenTCP(port, self.connection)  # @UndefinedVariable
                break
            except:
                pass
        print "Info: server has started, connected to port "+str(port)
        reactor.run() # @UndefinedVariable
        
    def add_game(self,name,color):
        self.rooms.append(game(name,color,self.iId,self.connection))
        self.iId += 1
    def get_player_room(self,index):
        for x in range(len(self.rooms)):
            room = self.rooms[x]
            for y in range(len(room.spectators)):
                spectator = room.spectators[y]
                if (spectator["ID"] == index):
                    return room.ID
        return 0
    def get_room_index_by_id(self,ID):
        for x in range(len(self.rooms)):
            if (self.rooms[x].ID == ID):
                return x
    def get_room_by_id(self,ID):
        return self.rooms[self.get_room_index_by_id(ID)]        
    def sendingData(self):
        for x in range(len(self.rooms)):
            room = self.rooms[x]
            
            for y in range(len(room.spectators)):
                spectator = room.spectators[y]
                
                roomdata = room.get_codes(spectator["ID"])
                data = {"packet":global_knowns.element_list,"data":roomdata}
                try:
                    self.connection.sendDataTo(spectator["ID"], data)
                except:
                    room.unjoinPlayer(y)
    def loop(self,SKIP = 1):
        
        self.logic_update(SKIP)
        self.sendingData()
        
        reactor.callLater(1./40,self.loop)  # @UndefinedVariable 
    def commands_loop(self):
        print "Info: commands interface started"
        while (self.on):
            command = raw_input(">>>")
            if (command == "exit"):
                self.on = False
                reactor.stop()  # @UndefinedVariable
                print "Info: reactor has been stopped"
                os.abort()
            elif (command == "rooms"):
                data = self.getRoomData()
                print "Room information "
                print "---------------------------------"
                print " Name      Players      Color    "
                print "---------------------------------"
                capacity = 0
                playing = 0
                for x in range(len(data)):
                    room = data[x]
                    print sd(room["name"],10)+"   "+sd(str(room["players"]),1)+ "/2     "+str(room["color"])
                    capacity += 2
                    playing += room["players"]
                print "---------------------------------"
                print "Rooms amount: "+str(len(data))
                print "Players playing: "+str(playing)+"/"+str(capacity)
            raw_input("\nPress enter to erase ...")
            os.system('clear')
        print "Info: commands interface has stopped"
    def logic_update(self,SKIP):
        for x in range(len(self.rooms)):
            self.rooms[x].logic_update(SKIP)
    def update_events(self,index,keys):
        for x in range(len(self.rooms)):
            for y in range(len(self.rooms[x].players)):
                if (self.rooms[x].players[y].index == index):
                    self.rooms[x].players[y].update_players_events(index,keys)
    def gr(self,ID):
        for x in range(len(self.rooms)):
            if (self.rooms[x].ID == ID):
                return x
    def handleData(self,index,data):
        if (data["packet"] == global_knowns.get_rooms_information):
            self.sendRoomData(index)
        elif (data["packet"] == global_knowns.extra_rooms_info):
            room = data["room"]
            self.handleExtraInfo(index,room)
        elif (data["packet"] == global_knowns.join_game):
            room = data["room"]
            self.handleSpectator(index,room)
        elif (data["packet"] == global_knowns.button_pressed):
            button_id = data["button"]
            room = self.get_player_room(index)
            
            self.handleButton(button_id,room,index)
        elif (data["packet"] == global_knowns.events):
            data = data["data"]
            room = self.get_player_room(index)
            self.handleEvents(data,room,index)
    def getRoomData(self):
        rooms = []
        for x in range(len(self.rooms)):
            room = {"name": self.rooms[x].name, "players": len(self.rooms[x].players), "color": self.rooms[x].color,"max players":self.rooms[x].max_players,"ID":self.rooms[x].ID}
            rooms.append(room)

        return rooms
    def sendRoomData(self,index):
        rooms = self.getRoomData()
        data = {"packet":global_knowns.rooms_information,"rooms":rooms}
        self.connection.sendDataTo(index,data)
        
    def getElementsList(self,room):
        data = self.rooms[room].get_code()
        return data
    def sendElementsList(self,room,index):
        data = {"packet":global_knowns.element_list,"data":room}
        self.connection.sendDataTo(index, data)

    def handleJoinGame(self,index,room,position,color):
        name = self.connection.clients[index].name
        color = self.connection.clients[index].color
        value = self.gr(room)
        if (value != None):
            self.rooms[ self.gr(room) ].join_player(name,color,index)
            self.sendJoinFail(index)
        else:
            self.sendJoinSuccess(index)
    def sendJoinFail(self,index):
        data = {"packet":global_knowns.room_join_result,"info":global_knowns.fail}
        self.connection.sendDataTo(index,data)
    def sendJoinSuccess(self,index):
        data = {"packet":global_knowns.room_join_result,"info":global_knowns.success}
        self.connection.sendDataTo(index,data)
    def handleExtraInfo(self,index,room):
        data = self.rooms[self.gr(room)].get_extra_info()
        info = {"packet":global_knowns.extra_rooms_info,"data":data}
        self.connection.sendDataTo(index, info)
    def handleSpectator(self,index,room):
        name = self.connection.clients[index].name
        print ""
        print "Spectator ",name," Joined to ",room
        print ">>>"
        self.rooms[ self.gr(room) ] . join_spectator(name,index)
    def handleButton(self,button_id,room,index):
        self.get_room_by_id(room).buttonPressed(button_id,index)
    def handleEvents(self,data,room,index):
        self.get_room_by_id(room).handleEvents(data,index)
def main():
    os.system('clear')
    game = gameHandler()
    print "Info: the server has been shut down"

main()
