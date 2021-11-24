'''
====== Legal notices

Copyright (C) 2013 - 2021 GEATEC engineering

This program is free software.
You can use, redistribute and/or modify it, but only under the terms stated in the QQuickLicense.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY, without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the QQuickLicense for details.

The QQuickLicense can be accessed at: http://www.qquick.org/license.html

__________________________________________________________________________


 THIS PROGRAM IS FUNDAMENTALLY UNSUITABLE FOR CONTROLLING REAL SYSTEMS !!

__________________________________________________________________________

It is meant for training purposes only.

Removing this header ends your license.
'''

import socket as sc
import json as js

address = 'localhost', 50012
socketType = sc.AF_INET, sc.SOCK_STREAM
maxNrOfConnectionRequests = 5
maxMessageLength = 1024

class SocketWrapper:
    def __init__ (self, clientSocket):
        self.clientSocket = clientSocket

    def send (self, anObject):
        buffer = bytes (f'{js.dumps (anObject):<{maxMessageLength}}', 'ascii')

        totalNrOfSentBytes = 0

        while totalNrOfSentBytes < maxMessageLength:
            nrOfSentBytes = self.clientSocket.send (buffer [totalNrOfSentBytes:])

            if not nrOfSentBytes:
                self.raiseConnectionError ()
                
            totalNrOfSentBytes += nrOfSentBytes

    def recv (self):
        totalNrOfReceivedBytes = 0
        receivedChunks = []

        while totalNrOfReceivedBytes < maxMessageLength:
            receivedChunk = self.clientSocket.recv (maxMessageLength - totalNrOfReceivedBytes)

            if not receivedChunk:
                self.raiseConnectionError ()

            receivedChunks.append (receivedChunk)
            totalNrOfReceivedBytes += len (receivedChunk)
            
        return js.loads (b''.join (receivedChunks) .decode ('ascii'))

    def raiseConnectionError (self):
        raise RuntimeError ('Socket connection broken')
