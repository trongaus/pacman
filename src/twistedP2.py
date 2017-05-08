# twistedP2.py (originally work)
# author: Taylor Rongaus
# due May 1, 2017

from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue

class DataConnection(Protocol):

    def connectionMade(self):
        print("work data connection made!!")

    def dataReceived(self, data):
        pass

class DataFactory(ClientFactory):
    def __init__(self):
        self.myconn = DataConnection()

    def buildProtocol(self, addr):
        return self.myconn

