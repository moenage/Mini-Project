from socket import *
import time
import select

def createSocket(hostName, portNumber):

    mySocket = socket(AF_INET, SOCK_STREAM)
    mySocket.bind((hostName, portNumber))
    return mySocket

def main():
    # print('Hello World')

    # Stores the test.html into a string so we can send to the browser as a respone
    testFile = open('test.html')
    testFile_html = testFile.read()
    testFile.close()

    # Here is the ip address and port number used
    hostName = "127.0.0.1" #Local Host IP
    portNumber = 371 # For CMPT 371 :)

    mySocket = createSocket(hostName, portNumber)

    mySocket.listen(1)

    timeLeft = 5 # 5 Seconds set for timeout

    while True:

        (clientSocket, address) = mySocket.accept()

        whatReady = select.select([clientSocket], [], [], timeLeft)
        if whatReady[0]:
            sentence = clientSocket.recv(1024).decode()
        elif whatReady[0] == []: # 408 Request Timed Out
            clientSocket.sendall(("HTTP/1.1 408 Request Timed Out\n" + sentence).encode())

        GET_partition = sentence.partition('GET')
        file_partition = sentence.partition('/test.html')

        # 400 Bad Request Checker
        if (GET_partition[1] == "GET") and (GET_partition[2][0] != " "):
            clientSocket.sendall(("HTTP/1.1 400 Bad Request\n" + sentence).encode())
        elif (GET_partition[1] != "GET"):
            clientSocket.sendall(("HTTP/1.1 400 Bad Request\n" + sentence).encode())

        # 404 File not found error checkers
        elif ((file_partition[1] == "/test.html") and (file_partition[2][0] != " ")):
            clientSocket.sendall(("HTTP/1.1 404 Not Found\n" + sentence).encode())
        elif (file_partition[1] != "/test.html"):
            clientSocket.sendall(("HTTP/1.1 404 Not Found\n" + sentence).encode())

        # 200 OK
        else:
            clientSocket.sendall(("HTTP/1.1 200 OK\n" + testFile_html).encode())

        clientSocket.close()
        


main()