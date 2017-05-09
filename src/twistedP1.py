# twistedP1.py (originally work)
# author: Taylor Rongaus
# due May 1, 2017

import pickle
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue

class DataConnection(Protocol):

	def connectionMade(self):
		print("twistedP1 data connection made!!"
		return True

	def dataReceived(self, data):
		print("twistedP1 got data")
		d = pickle.loads(data)

	def sendData(self, data):
		self.transport.write(pickle.dumps(data))

class DataFactory(ClientFactory):
   
    def __init__(self):
        self.myconn = DataConnection()
        print("twistedP1 data connection initialized")

    def buildProtocol(self, addr):
        return self.myconn

