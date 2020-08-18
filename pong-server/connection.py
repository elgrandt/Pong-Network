from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor

import global_knowns as gk
import base64
import json
import random

class PlayerHandler (LineReceiver):
    def __init__(self, factory,game):
        self.factory = factory
        self.name = "player"
        self.color = (random.randrange(0,255),random.randrange(100,255),random.randrange(0,255))
        self.state = "NONAME"
        self.game = game
    def connectionMade(self):
        self.factory.clients.append(self)
        print ""
        print "Info: connection from IP: " + str(self.transport.getPeer().host)
        print ">>>"
        self.name = str(self.transport.getPeer().host)
    def connectionLost(self,reason):
        clientIndex = self.factory.clients.index(self)
        del self.factory.clients[clientIndex]
        print ""
        print "Info: player "+str(clientIndex)+" disconnected";
        print ">>>"
    def sendData(self, jsonData):

        encodedData = base64.b64encode(json.dumps(jsonData))
        self.sendLine(encodedData)
    def lineReceived(self, jsonData):
        clientIndex = self.factory.clients.index(self)
        
        decodedData = json.loads((base64.b64decode(jsonData)))
        
        self.game.handleData(clientIndex,decodedData)
        
class Gamefactory(Factory):
    protocol = PlayerHandler
    def __init__(self,game):
        self.clients = []
        self.game = game
    def buildProtocol(self, addr):
        return PlayerHandler(self,self.game)      
    def sendDataTo(self,index,jsonData):
        self.clients[index].sendData(jsonData)
    def sendDataToAll(self,jsonData):
        for x in range(len(self.clients)):
            self.clients[x].sendData(jsonData)
