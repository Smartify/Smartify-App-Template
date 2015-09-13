import websocket
import thread
import time
import os

PROCESSES = []

# socket connection is open
def opened(ws):
    print "web socket connection is open!"

    def run(*args):
        for i in range(3):
            time.sleep(1)
        ws.close()
        print "thread terminating..."
        thread.start_new_thread(run, ())

# socket connection is closed
def closed(code, reason=None):
    print "socket is closed", code, reason

def on_error(ws, error):
    print error

# a message is received
def received_message(ws, m):
    print "socket message received!"

    print m
    # m always has '#' as its first character

    # define deliminters
    parseDelim1 = m.index(' ')
    parseDelim2 = m.index('|')

    # parse app name and phone number
    job = m[1:parseDelim1]
    phone = m[parseDelim1+1:parseDelim2]

    # terminate program if terminate command
    if 'terminate' in m:
        delete_process(m[10:])
    else:
        handle_process(job, phone)

# handle the process
def handle_process(phone, job):
    global PROCESSES

    # compute the process_id
    process_id = '#' + job[:3] + str(abs(hash(phone)))[:4]

    # start process if the program isn't already running
    if not process_exist(process_id):
        start_process(process_id)

# this function starts a process
def start_process(process_id):
    global PROCESSES
    PROCESSES.append(process_id)
    # run the application
    os.system('python ' + process_id[1:3] + '.py' + phone + ' ' + job)

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

    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:4080/",
    on_message = received_message,
    on_error = on_error,
    on_close = closed)
    ws.on_open = opened
    ws.run_forever()
