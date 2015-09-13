import sys
from websocket import create_connection

NUM_FLAG = len(sys.argv)
FLAGS = sys.argv

class SmartifyApp:

	# constructor
	def __init__(self, phone, job):
		self.process_id = '#' + job[:3] + str(abs(hash(phone)))[:4]
		self.phone = phone
		self.job = job
		self.socket = 'ws://localhost:4080/'

	# read user input
	def read_input():
		return self.prompt_input('')

	# this method asks the user a question, then waits for an answer (blocking)
	def prompt_input(msg):
		return

	# send raw text output as SMS
	def send_sms(self, msg):
		self.send_mms(msg, None)

	# this low-level API sends a message through the websocket
	def send_socket_msg(self, msg):
		ws = create_connection(self.socket)
		ws.send(msg)
		result = ws.recv()
		ws.close()

		return result

	# send text and image as MMS
	def send_mms(self, msg, imgURL):
		if imgURL == None:
			imgURL = ""

		socket_msg = self.phone + ' ' + msg + '|' + imgURL
		result = self.send_socket_msg(socket_msg)

		return result

	def terminate(self):
		self.send_socket_msg('terminate ' + self.process_id)
		sys.exit(0)

	# main program
	def run(self):
		# your main program
		newProgram = SmartifyApp("+124012339210", "amazon")

		print newProgram.process_id

def main():
	app = SmartifyApp(FLAGS[0], FLAGS[1])

	# your app code goes here

	app.terminate()

if __name__ == '__main__':
	main()
