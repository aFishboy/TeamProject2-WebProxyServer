import socket
import threading

# Define the proxy server's address and port
proxy_host = '127.0.0.1'
proxy_port = 8888

def handle_client(client_socket):
    # Receive data from the client
    request_data = client_socket.recv(4096)
    
    # Create a socket to connect to the remote server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the remote server
    server_socket.connect(('www.example.com', 80))
    
    # Send the received data to the remote server
    server_socket.send(request_data)
    
    # Receive data from the remote server
    server_response = server_socket.recv(4096)
    
    # Send the received data back to the client
    client_socket.send(server_response)
    
    # Close the connections
    server_socket.close()
    client_socket.close()

def proxy_server():
    # Create a TCP socket
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the address and port
    proxy_socket.bind((proxy_host, proxy_port))
    
    # Start listening for incoming connections
    proxy_socket.listen(5)
    
    print('[*] Proxy server listening on {}:{}'.format(proxy_host, proxy_port))
    
    while True:
        # Accept incoming client connections
        client_socket, client_address = proxy_socket.accept()
        
        print('[*] Accepted connection from {}:{}'.format(client_address[0], client_address[1]))
        
        # Create a new thread to handle the client connection
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    proxy_server()