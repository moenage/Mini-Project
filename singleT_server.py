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
    # timeLeft = 0.000000000000000000000001 #Time to test 408 Request Timed Out

    while True:

        (clientSocket, address) = mySocket.accept()

        whatReady = select.select([clientSocket], [], [], timeLeft)
        if whatReady[0]:
            html_msg = clientSocket.recv(1024).decode()
            GET_partition = html_msg.partition('GET')
            file_partition = html_msg.partition('/test.html')
        elif whatReady[0] == []: # 408 Request Timed Out
            html_msg = clientSocket.recv(1024).decode()
            clientSocket.sendall(("HTTP/1.1 408 Request Timed Out\n" + html_msg).encode())
            clientSocket.close()
            continue

        # 400 Bad Request Checker
        if ((GET_partition[1] == "GET") and (GET_partition[2][0] != " ") and (GET_partition[0] == '')):
            clientSocket.sendall(("HTTP/1.1 400 Bad Request\n" + html_msg).encode())
        elif (GET_partition[1] != "GET"):
            clientSocket.sendall(("HTTP/1.1 400 Bad Request\n" + html_msg).encode())

        # 404 File not found error checkers
        elif ((file_partition[1] == "/test.html") and (file_partition[2][0] != " ") and (file_partition[0] == "GET ")):
            clientSocket.sendall(("HTTP/1.1 404 Not Found\n" + html_msg).encode())
        elif (file_partition[1] != "/test.html"):
            clientSocket.sendall(("HTTP/1.1 404 Not Found\n" + html_msg).encode())

        #200 OK
        else:
            clientSocket.sendall(("HTTP/1.1 200 OK\n" + testFile_html).encode())

        clientSocket.close()
        


main()