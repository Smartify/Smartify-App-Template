from ws4py.client.threadedclient import WebSocketClient
import os

PROCESSES = []

class SmartifyApp(WebSocketClient):

    # socket connection is open
    def opened(self):
        print "web socket connection is open!"

    # socket connection is closed
    def closed(self, code, reason=None):
        print "socket is closed", code, reason

    # a message is received
    def received_message(self, m):
        print "socket message received!"

        # define deliminters
        parseDelim1 = m.index(' ')
        parseDelim2 = m.index('|')

        # parse app name and phone number
        job = m[1:parseDelim1]
        phone = m[parseDelim1+1:parseDelim2]

        # terminate program if terminate command
        if 'terminate' in m:
            delete_process(m)
        else:
            handle_process(job, phone)

    # handle the process
    def handle_process(phone, job):
        global PROCESSES

        # compute the process_id
        process_id = '#' + job[:3] + str(abs(hash(phone)))[:4]

        # start process if the program isn't already running
        if !process_exist(process_id):
            start_process(process_id)

    # this function starts a process
    def start_process(process_id):
        global PROCESSES
        PROCESSES.append(process_id)

    # this function deletes a process
    def delete_process(process_id):
        global PROCESSES

        for i in range(len(PROCESSES)):
            if PROCESSES[i] == process_id:
                PROCESSES.remove(process_id)
                break

    # this function checks if a process already exists
    def process_exist(process_id):
        for i in range(len(PROCESSES)):
            if PROCESSES[i].process_id == process_id:
                return True

        # process does not exist
        return False

if __name__ == '__main__':
    try:
        ws = SmartifyApp('ws://localhost:9000/', protocols=['http-only', 'chat'])
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()



