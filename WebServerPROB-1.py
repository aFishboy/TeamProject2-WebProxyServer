# Import socket module
from socket import *

# Create a TCP server socket
# (AF_INET is used for IPv4 protocols)
# (SOCK_STREAM is used for TCP)

serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 6789
serverSocket.bind(("", serverPort))
serverSocket.listen(1)  # Listen for incoming connections, allowing only one connection at a time

# Server should be up and running and listening to the incoming connections
while True:
    print('Ready to serve...')
    
    # Set up a new connection from the client
    connectionSocket, addr = serverSocket.accept()  # Accept a new connection
    
    # If an exception occurs during the execution of try clause
    # the rest of the clause is skipped
    # If the exception type matches the word after except
    # the except clause is executed
    try:
        # Receives the request message from the client
        message = connectionSocket.recv(1024).decode()
        print("message:", message)

        # Extract the path of the requested object from the message
        # The path is the second part of HTTP header, identified by [1]
        filename = message.split()[1]
        print('Request for file:', filename)

        # Because the extracted path of the HTTP request includes 
        # a character '\', we read the path from the second character 
        with open(filename[1:], "rb") as f:
            # Store the entire content of the requested file in a temporary buffer
            outputdata = f.read()
        print("Read File")
        
        with open("outputData.txt", "wb") as file:
            file.write(outputdata)
        # Send the HTTP response header line to the connection socket
        connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
 
        # Send the content of the requested file to the connection socket
        connectionSocket.sendall(outputdata)
        print('File', filename, 'sent successfully')
    
        # Close the client connection socket
        connectionSocket.close()

    except IOError:
        # Send HTTP response message for file not found
        print('File not found')
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        
        # Close the client connection socket
        connectionSocket.close()

serverSocket.close()