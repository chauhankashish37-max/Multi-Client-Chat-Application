import socket
import threading

HOST = "127.0.0.1"
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

username = input("Enter your username: ")
print("\n" + "=" * 40)
print("      Connected to Chat Server")
print("=" * 40)
print("Type messages below")
print("Type 'exit' to leave the chat\n")

# Receive messages
def receive():
    while True:
        try:
            message = client.recv(1024).decode()

            if message == "USERNAME":
                client.send(username.encode())
            else:
                print(message)
        except:
            print("Disconnected from server")
            client.close()
            break


# Send messages
def write():
    while True:
        message = input()

        if message.lower() == "exit":
            client.send(f"{username} left the chat.".encode())
            client.close()
            print("You left the chat.")
            break

        client.send(f"{username}: {message}".encode())


# Start threads
threading.Thread(target=receive).start()
threading.Thread(target=write).start()