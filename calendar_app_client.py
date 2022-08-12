import socket_tcp_client as stc
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout

class ScreenWidget(Widget):
	pass
		
class HeaderWidget(Widget):
	pass
		
class OperationsWidget(Widget):
	pass
		
class MonthLayout(GridLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		for week_day in range(7):
			for week in range(5):
				self.add_widget( DayOfMonthWidget(week_day+1, week+1))

class DayOfMonthWidget(Widget):
	def __init__(self, week_day, week, **kwargs):
		super().__init__(**kwargs)
		self.week = week
		self.week_day = week_day

class CalendarClientApp(App):
	def __init__(self, ip, port, **kwargs):
		super().__init__(**kwargs)
		self.__client = stc.Socket_tcp_client(ip, port)
	
	def build(self):
		return ScreenWidget()
		
	def send_to_server(self, msg):
		self.__client.connect()
		self.__client.send_msg(msg)
		self.__client.disconnect()

if __name__ == "__main__":
	app = CalendarClientApp("192.168.178.11", 29222)
	app.run()
#RUNMODES = {'TEST_LOCAL': 1, 'TEST_HOST': 2, 'PRODUCTION': 3}
#RUNMODE = RUNMODES['TEST_HOST']
#PORT = 29222
#FORMAT = 'utf-8'
#SERVER = '192.168.178.11'
#if RUNMODE == RUNMODES['TEST_LOCAL']:
#	SERVER = 'localhost'
#ADDR = (SERVER, PORT)
#DISCON_MSG = "--DISCON--"
#LENGTH_MSG_SIZE = 512

#client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#client.connect(ADDR)

#def run_client():
#	running = True
#	while running:
#		text = input()
#		msg = text.encode(FORMAT)
#		msg_length = len(msg)
#		msg_length = str(msg_length).encode(FORMAT)
#		while len(msg_length) < LENGTH_MSG_SIZE:
#			msg_length += b' '
#		client.send(msg_length)
#		while len(msg) > 1024:
#			client.send(msg[0:1024])
#			msg = msg[1024:]
#		client.send(msg)
#	
#	
#run_client()
