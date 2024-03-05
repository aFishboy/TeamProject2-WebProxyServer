import socket
import threading

# Define the proxy server's address and port
proxy_host = '127.0.0.1'
proxy_port = 8888

# Cache to store responses from the remote server
cache = {}

# Cache directory to store responses from the remote server
CACHE_DIR = "cache/"

# Ensure cache directory exists
import os
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# Counter for file naming
file_counter = 0

def log(message):
    # Function to log messages with thread information
    print("[{}] {}".format(threading.current_thread().name, message))

def write_to_file(data):
    global file_counter
    filename = CACHE_DIR + "response_" + str(file_counter) + ".txt"
    with open(filename, "wb") as file:
        file.write(data)
    file_counter += 1

def handle_client(client_socket):
    # Receive data from the client
    request_data = client_socket.recv(4096)
    print("request_data", request_data)

    substring_index = request_data.find(b'/localhost:')
    # Check if the substring exists in the full path
    if substring_index != -1:
        # Find the index of the end of the substring '/localhost:xxxx'
        end_index = request_data.find(b'/', substring_index + 1)
        
        # Replace the substring with an empty string
        modified_full_path = request_data[:substring_index] + request_data[end_index:]
    else:
        # If the substring doesn't exist, use the original full path
        modified_full_path = request_data

    # Split request_data into request line and headers
    request_line, headers = request_data.split(b'\r\n', 1)

    # Extract method, resource path, and HTTP version from the request line
    method, full_path, http_version = request_line.split(b' ')

    # Extract hostname, port, and filename from the full path
    _, host_info, filename = full_path.split(b'/')
    hostName, portBytes = host_info.split(b':')

    # Replace the port number in the modified full path with the value from the port variable
    modified_full_path = modified_full_path.replace(b':8888', b':' + portBytes)
    port = int(portBytes)
    
    # Check if the filename is in the cache
    if filename in cache:
        log("Cached request found")
        # If so, serve the response from the cache
        cached_response = cache[filename]
        client_socket.send(cached_response)
        client_socket.close()
        return

    log("New request received")
    
    # Create a socket to connect to the remote server
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the remote server
    server_socket.connect((hostName, port))
    
    log("Connected to remote server")
    
    # Send the received data to the remote server
    server_socket.send(modified_full_path)
    
    log("Request forwarded to remote server")
    
    # Receive data from the remote server
    server_response = server_socket.recv(4096)
    print("server response:\n", server_response)
    
    log("Received response from remote server")
    
    # Cache the response using the filename as the key
    cache[filename] = server_response
    
    log("Response cached")
    
    # Write the response to a file
    write_to_file(server_response)
    
    log("Response written to file")
    
    # Send the received data back to the client
    client_socket.send(server_response)
    
    log("Response forwarded to client")
    
    # Close the connections
    server_socket.close()
    client_socket.close()

def proxy_server():
    # Create a TCP socket
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the address and port
    proxy_socket.bind(("", proxy_port))
    
    # Start listening for incoming connections
    proxy_socket.listen(5)
    
    log('[*] Proxy server listening on {}:{}'.format("All", proxy_port))
    
    while True:
        # Accept incoming client connections
        client_socket, client_address = proxy_socket.accept()
        
        log('[*] Accepted connection from {}:{}'.format(client_address[0], client_address[1]))
        
        # Create a new thread to handle the client connection
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    proxy_server()
