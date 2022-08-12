import socket
import signal
import atexit
import logging

class Socket_tcp_client:
	def __init__(self, ip, port, strformat="utf-8", dcmsg="--DISCON--", length_msg_size = 512, loglevel="INFO"):
		self.__runmodes = {'TEST_LOCAL': 1, 'TEST_HOST': 2, 'PRODUCTION': 3}
		self.__runmode = self.__runmodes['TEST_HOST']
		self.__port = port
		self.__format = strformat
		self.__server = ip
		if self.__runmode == self.__runmodes['TEST_LOCAL']:
			self.__server = 'localhost'
		self.__addr = (self.__server, self.__port)
		self.__discon_msg = dcmsg
		self.__len_msg_size = length_msg_size
		
		self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		#signal.signal(signal.SIGKILL, self.__on_exit)
		signal.signal(signal.SIGTERM, self.__on_exit)
		signal.signal(signal.SIGINT, self.__on_exit)
		atexit.register(self.__on_exit)
		
		logging.basicConfig(level=getattr(logging, loglevel.upper(), None))
		
		self.is_connected = False
		self.is_at_exit = False
		
	def send_msg(self, text):
		if self.is_connected is False:
			logging.warning("[SEND] cannot send, client is not connected!")
			return False
		msg = text.encode(self.__format)
		msg_length = len(msg)
		msg_length = str(msg_length).encode(self.__format)
		while len(msg_length) < self.__len_msg_size:
			msg_length += b' '
		self.__client.send(msg_length)
		while len(msg) > 1024:
			self.__client.send(msg[0:1024])
			msg = msg[1024:]
		self.__client.send(msg)
		return True
	
	def connect(self):
		if self.is_connected is True:
			logging.warning("[CONNECT] cannot connect, client is already connected!")
			return False
		try:
			self.__client.connect(self.__addr)
			self.is_connected = True
			return True
		except TimeoutError as e:
			logging.error(repr(e))
			return False
		
	def disconnect(self):
		if self.is_connected is False and self.is_at_exit is False:
			logging.warning("[DISCONNECT] cannot disconnect, client is not connected!")
			return False
		if self.is_connected is False and self.is_at_exit is True:
			logging.info("[DISCONNECT] You disconnected before exiting. Thats good practice!")
			return False
		if self.is_connected is True and self.is_at_exit is True:
			logging.warning("[DISCONNECT] You didn't disconnect before exiting. Please try to, next time!")
		self.send_msg(self.__discon_msg)
		self.__client.close()
		self.is_connected = False
		return True

	def __on_exit(self):
		self.is_at_exit = True
		logging.info("[ATEXIT] trying to finalize an shut down")
		self.disconnect()
		