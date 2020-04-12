import socket
import threading

#constantly refresh chat for new messages from server
def refresh_chat(server):
   while True:
      try:
         msg = server.recv(1024)
         print(msg.decode())
      except:
         pass

#Exchange username and welcome message from server
def welcome_handshake(server, username):
   server.send(username.encode())
   welcome = server.recv(1024).decode()
   print(welcome)

def main():
   print("- - - Chat Client - - -")
   address = (input("Enter Server IP Address: "), 1717)
   username = input("Enter username: ")

   #Attempt to connect to server
   sock = socket.socket()
   connection = False
   while not connection:
      print(address[0])
      print(address[1])
     # print(sock.connect(address))
      try:
         print("Connecting to " + address[0] + ":" + address[1])
         sock.connect(address)
         connection == True
      except:
         print("Unable to connect to host!")
         address = (input("Enter Server IP Address: "), 1717)

   welcome_handshake(sock, username)
   threading.Thread(target=refresh_chat,args=(sock,)).start()

   while True:
      msg = input()
      if msg == '!exit':
         break
      elif len(msg) == 0:
         continue
      sock.send(msg.encode())
   #if msg = "!exit" send the message and close the socket
   sock.send(msg.encode())
   sock.close()

if __name__ == '__main__':
    main()
