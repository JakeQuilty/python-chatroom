import socket
import threading
import time

active_connections = list()

def new_client(client,address):
   #setup new client and send welcome message
   username = client.recv(1024).decode()
   print(username + " joined chat(" + address[0] + ")")

   welcome_msg = ("\n- - - Connected to chatroom! - - -\n"
   "  -  Number of users: " + str(threading.active_count()-1)+"\n"
   "  -  '!exit' to leave\n"
   )
   client.send(welcome_msg.encode())

   while True:
      try:
         msg = client.recv(1024).decode()
         if not msg or msg == "!exit":
            break
         
         #Format and send message to all users
         msg = format_message(username, msg)
         send_to_all_clients(msg)
      except:
         #catch error from user leaving without !exit
         leave_chat(username,client,address)
         return

   leave_chat(username,client,address)

def send_to_all_clients(message):
   message = message.encode()
   for curr in active_connections:
      curr.send(message)

#add time and username to message(decoded)
def format_message(username, message):
   return "["+ time.strftime("%H:%M:%S") + "](" + username + ")" + message

#when connection ends send message to all users of leavings
def leave_chat(username, client, address):
   print(username + " left chat(" + address[0] + ")")
   active_connections.remove(client)
   farewell_msg = username + " has left the chat"
   send_to_all_clients(farewell_msg)

def main():
   #Setup server
   print("<.> Setting up server...")
   host_name = socket.gethostname()
   address = (socket.gethostbyname(host_name),1717)
   print("<.> Host IP: " + str(address[0]))
   print("<.> Host Port: " + str(address[1]))
   server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   server.bind((host_name, address[1]))
   server.listen(5)

   #Wait for connections
   print("<.> Waiting for connections...")
   while True:
      #when connection is established create a new client thread
      connection, address = server.accept()
      client = threading.Thread(target = new_client,args = (connection,address))
      active_connections.append(connection)
      try:
         client.start()
      except:
         pass

if __name__ == '__main__':
    main()