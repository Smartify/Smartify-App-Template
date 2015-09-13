import sys
import threading
from websocket import create_connection

NUM_FLAG = len(sys.argv)
FLAGS = sys.argv
SOCKET = 'ws://localhost:4080/'

class SmartifyApp:

	# main program thread constructor
	def __init__(self, code, job, phone):
		self.process_id = getProcessID(job, phone)
		self.code = code
		self.phone = phone
		self.job = '#' + job

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
		newCode = ''

		if self.code = 'f':
			newCode = 'e'
		else:
			newCode = '7'

		newMsg = newMessage(newCode, self.job, self.phone, msg)
		result = self.send_socket_msg(newMsg)

		return result

	# send text and image as MMS
	def send_mms(self, msg, imgURL):
		pass

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


def getProcessID(job, phone):
    return '#' + job[:3] + str(abs(hash(phone)))[:4]

def newMessage(newCode, job, phone, body):
	return newCode + job + ' ' + phone + '|' + body

def main():
	app = SmartifyApp(FLAGS[0], FLAGS[1], FLAGS[2])
	# FLAGS = [code, job, phone]
	# your app code goes here

	app.terminate()

if __name__ == '__main__':
	main()
