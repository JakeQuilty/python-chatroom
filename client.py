import re
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

#I got this regex template from https://www.geeksforgeeks.org/python-program-to-validate-an-ip-address/
#I used this regex, because it is a standard template for checking if a string is a valid ip address
def checkIP(ip):
   regex = '''^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\.( 
            25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)'''
   return re.search(regex, ip)

def main():
   print("- - - Chat Client - - -")
   address = (input("Enter Server IP Address: "), 1717)
   username = input("Enter username: ")

   #Attempt to connect to server
   #Checks that IP address is valid to avoid crashing client
   sock = socket.socket()
   connection = False
   while not connection:
      try:
         if checkIP(address[0]):
            sock.connect(address)
            connection = True
         else:
            raise ValueError("Not a valid IP address!")
      except:
         print("Unable to connect to host!")
         address = (input("Enter Server IP Address: "), 1717)

   #On a successful connection, exchange welcome handshake and start new thead for chat refreshes
   welcome_handshake(sock, username)
   threading.Thread(target=refresh_chat,args=(sock,)).start()

   while True:
      msg = input()
      if msg == '!exit':
         break
      elif len(msg) == 0:
         continue
      sock.send(msg.encode())
   #if the msg equals "!exit" send the message and close the socket
   sock.send(msg.encode())
   sock.close()

if __name__ == '__main__':
    main()
