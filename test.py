request_data = b'GET /localhost:6789/helloworld.html HTTP/1.1\r\nHost: localhost:8888\r\nUser-Agent: curl/7.81.0\r\nAccept: */*\r\n\r\n'
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
hostname, port_bytes = host_info.split(b':')

# Replace the port number in the modified full path with the value from the port variable
modified_full_path = modified_full_path.replace(b':8888', b':' + port_bytes)

print("full path:", full_path.decode())
print("modified fp:", modified_full_path)
print("Method:", method.decode())
print("Hostname:", hostname.decode())
print("Port:", port.decode())
print("Filename:", filename.decode())