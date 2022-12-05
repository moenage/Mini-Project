from socket import *

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

    while True:
        (clientSocket, address) = mySocket.accept()

        sentence = clientSocket.recv(1024).decode()

        # 400 Bad Request Checker
        if not sentence:
            clientSocket.sendall("HTTP/1.1 400 Bad Request\n" + sentence)
            break

        sent_partition = sentence.partition('/test.html')

        # 404 File not found error checkers
        if(sent_partition[1] == "/test.html"):
            print("1")
            if(sent_partition[2][0] != " "):
                print("2")
                clientSocket.sendall(("HTTP/1.1 404 Not Found\n" + sentence).encode())
                break
        elif(sent_partition[1] != "/test.html"):
            print("3")
            clientSocket.sendall(("HTTP/1.1 404 Not Found\n" + sentence).encode())
            break

        clientSocket.sendall(("HTTP/1.1 200 OK\n" + testFile_html).encode())

        clientSocket.close()
        
    mySocket.close()


main()