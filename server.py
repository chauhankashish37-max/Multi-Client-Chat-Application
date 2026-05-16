import socket
import threading
from datetime import datetime

HOST = "127.0.0.1"
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Prevent port reuse error
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen()
# Clear old chat history on server start
open("chat.txt", "w").close()

print("=" * 40)
print("   Multi-Client Chat Server")
print("=" * 40)
print(f"Server running on {HOST}:{PORT}")
print("Waiting for connections...\n")

clients = []
usernames = []

# Broadcast message to all clients
def broadcast(message):
    timestamp = datetime.now().strftime("%H:%M")
    formatted_message = f"[{timestamp}] | {message.decode()}"

    for client in clients:
        client.send(formatted_message.encode())

    # Save chat to file
    with open("chat.txt", "a") as file:
        file.write(formatted_message + "\n")


# Handle individual client
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()

            username = usernames[index]
            broadcast(f"{username} left the chat.".encode())

            usernames.remove(username)
            break


# Accept new clients
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {address}")

        client.send("USERNAME".encode())
        username = client.recv(1024).decode()

        usernames.append(username)
        clients.append(client)

        print(f"Username: {username}")

        # Send old chat history (optional but impressive)
        try:
            with open("chat.txt", "r") as file:
                history = file.read()
                client.send(history.encode())
        except:
            pass

        broadcast(f"{username} joined the chat!".encode())

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


receive()