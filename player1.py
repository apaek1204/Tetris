#!/usr/bin/python2.7

'''player1.py
	Acts as client player
'''

'''Im expecting them to play at the same time
And they should send packets with score, level, alive, sendline as values
And update as necessary'''

from twisted.internet.protocol import Factory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
import tetris

'''Data Connection class
	Send data from player 1 to player 2
'''

class DataConnection(Protocol):
	def __init__(self):
		self.P1Queue = DeferredQueue()
	def connectionMade(self):
		tetris.main()
class DataConnectionFactory(Factory):
	def __init__(self):
		self.myconn = DataConnection()
	def buildProtocol(self, addr):
		return self.myconn

def main():
	reactor.listenTCP(40016, DataConnectionFactory())
	reactor.run()

if __name__ == "__main__":
	main()
