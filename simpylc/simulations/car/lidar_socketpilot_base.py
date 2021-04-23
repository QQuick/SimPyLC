import socket as sc

class LidarSocketpilotBase:
    address = '', 50008
    socketType = sc.AF_INET, sc.SOCK_STREAM
    maxNrOfConnectionRequests = 5
    maxMessageLength = 256

    def send (self, message):
        buffer = bytes (f'{message:<{self.maxMessageLength}}', 'ascii')

        totalNrOfSentBytes = 0

        while totalNrOfSentBytes < self.maxMessageLength:
            nrOfSentBytes = self.clientSocket.send (buffer [totalNrOfSentBytes:])

            if not nrOfSentBytes:
                self.raiseConnectionError ()
                
            totalNrOfSentBytes += nrOfSentBytes

    def recv (self):
        totalNrOfReceivedBytes = 0
        receivedChunks = []

        while totalNrOfReceivedBytes < self.maxMessageLength:
            receivedChunk = self.clientSocket.recv (self.maxMessageLength - totalNrOfReceivedBytes)

            if not receivedChunk:
                self.raiseConnectionError ()

            receivedChunks.append (receivedChunk)
            totalNrOfReceivedBytes += len (receivedChunk)
            
        return b''.join (receivedChunks) .decode ('ascii')

    def raiseConnectionError (self):
        raise RuntimeError ('Socket connection broken')
