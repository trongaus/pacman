# twistedP2.py (originally work)
# author: Taylor Rongaus
# due May 1, 2017

from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue

class DataConnection(Protocol):

    def connectionMade(self):
        print("twistedP1 data connection made!!")

    def dataReceived(self, data):
        print("got data")

class DataFactory(ClientFactory):
   
    def __init__(self):
        self.myconn = DataConnection()
        print("twistedP1 data connection initialized")

    def buildProtocol(self, addr):
        return self.myconn

