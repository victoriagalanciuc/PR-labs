import socket

commands = [
    '/help - Get all supported commands',
    '/hello Text - Display the used text',
    '/current_time - Display the current time',
    '/number_generator - Generate a random number',
    '/flip_coin - Flip the coin'
]

def start_server(address, port, max_connections=5):
    # We're using TCP/IP as transport
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Bind to the given address and port
    server_socket.bind((address, port))
    # Listen for incoming connection (with max connections)
    server_socket.listen(max_connections)
    print("=== Listening for connections at %s:%s" % (address, port))
    while True:
        # Accept an incomming connection
        # Note: this is blocking and synchronous processing of incoming connection
        incoming_socket, address = server_socket.accept()
        print("=== New connection from %s" % (address,))
        # Recv up to 1kB of data
        data = incoming_socket.recv(1024)
        print(">>> Received data %s" % (data,))
        if(data[0] == '/'):
            command = data[1:]
            if command == 'help':
                string_response = '\n'
                for i in range(len(commands)):
                    string_response = string_response + commands[i] + '\n'
                    incoming_socket.send(string_response)
                    incoming_socket.close()
            




if __name__ == '__main__':
    start_server('127.0.0.1', 8000)