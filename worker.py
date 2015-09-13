from ws4py.client.threadedclient import WebSocketClient
import os


PROCESSES = []

class SmartifyApp(WebSocketClient):
    def opened(self):
        # what to do when socket connection is open
        pass

    def closed(self, code, reason=None):
    	# what to do when socket connection is closed
        print "Closed down", code, reason

    def received_message(self, m):

        # define deliminters
        parseDelim1 = m.index(' ')
        parseDelim2 = m.index('|')

        # app name
        job = m[1:parseDelim1]  # ignore initial #
        phone = m[parseDelim1 + 1 : parseDelim2]

        if 'terminate' in m:
            delete_process(m)
        else:
            handle_process(job, phone)

    def handle_process(phone, job):
        global PROCESSES

        process_id = '#' + job[:3] + str(abs(hash(phone)))[:4]

        if !process_exist(process_id):
            process = SmartifyApp(phone, job)
            PROCESSES.append(process)

    def start_process(process_id):
        pass

    def delete_process():
        pass

    def process_exist(process_id):
        for i in range(len(PROCESSES)):
            if PROCESSES[i].process_id == process_id:
                return True

        return False

if __name__ == '__main__':
    try:
        ws = SmartifyApp('ws://localhost:9000/', protocols=['http-only', 'chat'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()



