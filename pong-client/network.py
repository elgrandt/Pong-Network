from twisted.internet.protocol import Protocol, Factory, ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor, error

import json
import base64
import global_knowns

class pongClient(LineReceiver):  
    def __init__(self, factory,game):
        self.factory = factory
        self.game = game
    def connectionMade(self):
        print "Info: connetion enablished\n"
        self.game.handleStart()     
    def lineReceived(self, data):

        self.game.handleData(json.loads(base64.b64decode(data)))
    def sendData(self, data):
        self.sendLine(base64.b64encode(json.dumps(data)))
class gameClientFactory(ClientFactory):
    def __init__(self,game):
        self.protocol  =  pongClient(self,game)
        self.game = game
    def startedConnecting(self, connector):
        print "Info: Connecting to server ..."
    def buildProtocol(self, addr):
        return self.protocol
    def clientConnectionFailed(self, connector, reason):
        errorMsg = reason.getErrorMessage().split(':')
        print 'Info: Unable to connect to server: ' + errorMsg[1] + errorMsg[2], 'An error occured'
        self.game.handleFail()
    def clientConnectionLost(self, connector, reason):
        print reason.getErrorMessage()
        try:
            reactor.stop()# @UndefinedVariable
            print "Info: Disconnected from server"
        except error.ReactorNotRunning:
            pass


