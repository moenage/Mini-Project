from socket import *

def createSocket(hostName, portNumber):

    mySocket = socket(AF_INET, SOCK_STREAM)
    mySocket.bind((hostName, portNumber))
    return mySocket



def main():
    print('Hello World')

    # Stores the test.html into a string so we can send to the browser as a request
    testFile = open('test.html')
    testFile_html = testFile.read()
    testFile.close()

    # Here is the ip address and port number used
    hostName = "127.0.0.1" #Local Host IP
    portNumber = 371 # For CMPT 371 :)

    mySocket = createSocket(hostName, portNumber)

    mySocket.listen(1)

    while True:
        (clientSocket, address) = mySocket.accept()

        # sentence = clientSocket.recv(1024).decode()

        # clientsocket.send(sentence.encode())

        clientSocket.sendall(("HTTP/1.1 200 OK\n" + testFile_html).encode())

        clientSocket.close()



main()