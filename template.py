import sys
import threading
from websocket import create_connection

NUM_FLAG = len(sys.argv)
FLAGS = sys.argv
SOCKET = 'ws://localhost:4080/'

class SmartifyApp:

	# main program thread constructor
	def __init__(self, phone, job):
		self.process_id = '#' + job[:3] + str(abs(hash(phone)))[:4]
		self.phone = phone
		self.job = job

	# this method will send user a message, then wait for an input
	def prompt_user_input(self, msg):
		try:
			ws = create_connection(SOCKET)
			ws.send(msg)
			result = ''
			# process_id is not in process_id computed from result (phone, job)
			while self.process_id not in result:
				result = ws.recv()
			ws.close()
		except:
			return None

		return result

	# send raw text output as SMS
	def send_sms(self, msg):
		send_mms(msg, None)

	# send text and image as MMS
	def send_mms(self, msg, imgURL):
		if imgURL == None:
			imgURL = ""

		socket_msg = self.phone + ' ' + msg + '|' + imgURL
		result = self.send_socket_msg(socket_msg)

		return result

	# sends a message through the websocket
	def send_socket_msg(self, msg):
		try:
			ws = create_connection(SOCKET)
			ws.send(msg)
			ws.close()
		except:
			return False

		return True

	# close the application
	def terminate(self):
		self.send_socket_msg('terminate ' + self.process_id)
		sys.exit(0)

def main():
	app = SmartifyApp(FLAGS[0], FLAGS[1])

	# your app code goes here

	app.terminate()

if __name__ == '__main__':
	main()
