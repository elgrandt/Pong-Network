from twisted.internet import reactor,threads

import pygame
import network
import global_knowns
import sys
import os

def sd(data,length):
    if (len(data) > length):
        data = data[0:length]
    elif(len(data) < length):
        while (len(data) < length):
            data += " "
    return data
class pongGame:
    def __init__(self):
        self.handledRoomInfo = False
        
        self.connection = network.gameClientFactory(self)
        self.on = True
        
        GAME_IP = "localhost"
        GAME_PORT = int(raw_input("Port:"))
        threads.callMultipleInThread([(self.mainGame,[],{})])
        
        reactor.connectTCP(GAME_IP, GAME_PORT, self.connection)  # @UndefinedVariable
        reactor.run()  # @UndefinedVariable
        
    def start_connection(self):
        threads.callMultipleInThread([(self.commands_loop,[],{})])    
    def commands_loop(self):
        print "Info: starting command interface ..."
        while (self.on):
            command = raw_input(">>>")
            if (command == "exit"):
                os.abort()
            elif (command == "rooms"):
                print "getting info ..."
                self.get_rooms()
            os.system("clear")
    def mainGame(self):
        print "Info: starting main game loop"
        while (self.on):
            self.loop()
        reactor.stop()  # @UndefinedVariable
    def loop(self):
        pass
    def handleData(self,data):
        if (data["packet"] == global_knowns.rooms_information):
            self.handleRoomsInfo(data["rooms"])

    def handleRoomsInfo(self,data):
        print "\nRoom information "
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

        self.handledRoomInfo = True
    def get_rooms(self):
        self.handledRoomInfo = False
        self.connection.protocol.sendData({"packet":global_knowns.get_rooms_information})
        #while not(self.handledRoomInfo):
        #    pass
def main():
    os.system('clear')
    pongGame()
    print "Disconecting ..."

main()
