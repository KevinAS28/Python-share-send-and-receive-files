import socket
import getopt
import os
import sys
from threading import Thread

def usage():
 print("Simple FTP by Kevin Agusto")
 print("to receive files, simply python simftp.py -ip <your ip (not necessary)> -p <port number> -r -l </home/my/location/ (all your files will downloaded)>")
 print('to send a file, python simftp.py -ip <ip> -p <port number> -s "myfile.rar" ')
 print('to multiple files, python simftp.py -ip <ip> -p <port number> -s "myfile.rar yourfile.rar /home/thisisfile.exe" ')
 print("or just hit python simftp.py to guided options")
 sys.exit(0)
 return

global the_files
mode = "g"  #guided
ip = ""
port = 21
the_files = []
 
try:
 opts, args = getopt.getopt(sys.argv[1:], "hle:a:p:m:f", ["help", "address", "port", "mode", "files"])
except getopt.GetoptError as jadierror:
 print(str(jadierror))
 usage()

for o, a in opts:
 if o in ["-a", "--addr", "-addr", "--address"]:
  ip = str(a)
 elif o in ["-p", "--port"]:
  port = int(a)
 elif o in ["-m", "--mode"]:
  mode = str(a)
 elif o in ["-h", "--help"]:
  usage()
 elif o in ["-f", "--files"]:
  the_files = args[0].split()
  
if mode == "g":
 mode = str(input("you will receive files or send files? [R/S] ")).lower()
 if mode == "r":
  ip = str(input("your ip: (not necessary) "))
  port = str(input("port number (21 is default): "))
  if not len(port):
   port = 21
  else:
   port = int(port)
  the_files = str(input("the address files will downloaded(not necessary): "))
  if not len(the_files):
   the_files = str(os.getcwd())
  
 if mode == "s":
  ip = str(input("the receiver ip: "))
  if ip=="":
   print("error, ip must be exist")
   sys.exit(0)
  port = input("the receiver port: (21 is default) ")
  if not len(port):
   port = 21
  else:
   port = int(port)
  the_files.clear()
  while True:
   what = str(input("type the file address or file name (if you finsih, just hit enter with blank): "))
   if not len(what):
    break
   the_files.append(what)

tcp_ip = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def sendfiles():
 global the_files
 global ip
 global port
 tcp_ip.connect((ip, port))
 for a in the_files:
  to_send = b"%s<this is seperate>" %(bytes(a.encode("utf-8")))
  with open(a, "rb") as the_data:
   to_send += the_data.read()
   tcp_ip.send(to_send)
   print(tcp_ip.recv(4096).decode("utf-8"))
 tcp_ip.close()

class recvfiles:
 global the_files
 def __init__(self):
  global the_files
  if not os.access(the_files, os.R_OK):
   print("[WARNING] the directory is cannot be accessed")
   the_files = str(os.getcwd())
  os.chdir(the_files)
  tcp_ip.bind((ip, port))
  tcp_ip.listen()
  
 def client_handler(self, client_socket):
  data = client_socket.recv(1024).split(b"<this is seperate>")
  open(data[0], "w+")
  with open(data[0], "wb") as yeah:
   yeah.write(data[1])
  client_socket.send(("successfull send %s" %(data[0])).encode("utf-8"))
  client_socket.close()
 def run(self):
  print("Waiting for sender...")
  while True:
   client, addr = tcp_ip.accept()
   print("Received incoming data from %s:%d" %(addr[0], addr[1]))
   Thread(target=self.client_handler, args=[client]).start()

if __name__ == "__main__":
 if mode == "r":
  recvfiles().run()
 else:
  sendfiles()
  
  