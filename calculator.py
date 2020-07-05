"""This is calculator.
Goal is to receive task from dispatcher, make client's lower_case_string
upper_case_string and send it back to dispatcher. Also sending signal about state"""

import socket
import time
import threading
import json
import random


with open('config.json') as f:
    config = json.load(f)
    port_for_dispatcher = config['calculator']['port_for_dispatcher_socket']
    period_of_work = config['calculator']['period_of_work_time']
    pause = config['calculator']['seconds_pause_of_working']
    probability = config['calculator']['probability_to_stop_working']
    send_state_sec = config['calculator']['period_of_sending_state']
    port_for_check = config['dispatcher']['port_for_calculator_socket']


SOCK = socket.socket(type=socket.SOCK_DGRAM)
SOCK.bind(('', port_for_dispatcher))

I_AM_CRUSHED = False                             # state of calculator


def send_state():
    """This function sending state if calculator is not broken"""
    while True:
        if I_AM_CRUSHED is False:
            sleep_time = random.randint(send_state_sec[0], send_state_sec[1])
            sock_check = socket.socket(type=socket.SOCK_DGRAM)
            sock_check.sendto("I'am healthy", ('dispatcher', port_for_check))
            sock_check.close()
            time.sleep(sleep_time)


t = threading.Thread(target=send_state)          # launch function on another process
t.start()

while True:
    if random.randint(1, 100) <= probability:    # probability to be crushed
        I_AM_CRUSHED = True
        time.sleep(pause)                        # time of being off
        I_AM_CRUSHED = False

    content, addr = SOCK.recvfrom(1024)

    sec = random.randint(period_of_work[0], period_of_work[1])   # random time which will be spent for work
    time.sleep(sec)
    SOCK.sendto(content.upper(), addr)           # send finished task
