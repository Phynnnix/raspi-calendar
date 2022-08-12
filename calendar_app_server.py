import socket
import threading
import netifaces

RUNMODES = {'TEST_LOCAL': 1, 'TEST_HOST': 2, 'PRODUCTION': 3}
RUNMODE = RUNMODES['TEST_HOST']
PORT = 29222
FORMAT = 'utf-8'
#SERVER = socket.gethostbyname(socket.gethostname())
SERVER = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
if RUNMODE == RUNMODES['TEST_LOCAL']:
	SERVER = 'localhost'
ADDR = (SERVER, PORT)
DISCON_MSG = "--DISCON--"
LENGTH_MSG_SIZE = 512

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
	connected = True
	while connected:
		msg_len = conn.recv(LENGTH_MSG_SIZE)
		msg_len = int(msg_len)
		msg = b""
		while msg_len >= 1024:
			msg += conn.recv(1024)
			msg_len -= 1024
		msg += conn.recv(msg_len)
		msg = msg.decode(FORMAT)
		print(f"[RECIEVE] {addr[0]} posts '{msg}'")
		

def start():
	print("[BOOT] ...Server startet...")
	server.listen()
	print(f"[LISTENING] ...Server hört auf {SERVER} zu...")
	running = True
	while running:
		conn, addr = server.accept()
		print(f"[ACCEPT] ...Server akzeptiert Anfrage von {addr[0]}")
		thread = threading.Thread(target=handle_client, args=(conn, addr))
		thread.start()
	
start()
