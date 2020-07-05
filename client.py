"""This is client for sending task.
Goal is to get uppercase variant of the string which client send"""

import socket
import time
import json
import random

MY_TIME = time.time()             # Start timer
LIST_OF_ANSWER_TIME = []          # Collect answer time
RESPONSES = 0
REQUESTS = 0

with open('config.json') as f:    # Read config data
    config = json.load(f)
    seconds_to_sleep = config['client']['pause_between_requests']
    port = config['dispatcher']['port_for_client_socket']

while True:
    sec = random.randint(seconds_to_sleep[0], seconds_to_sleep[1])  # Set period of sending request
    if time.time() - MY_TIME >= sec:
        try:
            sock = socket.socket(type=socket.SOCK_DGRAM)
            sock.settimeout(25)
            sock.sendto('hello world', ('dispatcher', port))
            start_time = time.time()
            REQUESTS += 1
            MY_TIME = time.time()
            data = sock.recvfrom(1024)
            end_time = time.time()
            LIST_OF_ANSWER_TIME.append(end_time-start_time)         # Add to list time which was taken for answer
            RESPONSES += 1
            sock.close()
        except (socket.error, socket.timeout):
            sock.close()

        with open('client_dir/RQ_RE_client_log', 'w') as d:
            d.write('Amount of requests: ' + str(REQUESTS) + '\n')
            d.write('Amount of response: ' + str(RESPONSES) + '\n')
            d.write('Amount of requests without response: ' + str(REQUESTS - RESPONSES) + '\n')
            if LIST_OF_ANSWER_TIME:
                d.write('The shortest answer from dispatcher: ' +
                        str(min(LIST_OF_ANSWER_TIME)) + '\n')
                d.write('The longest answer from dispatcher: ' +
                        str(max(LIST_OF_ANSWER_TIME)) + '\n')
                d.write('The average answer from dispatcher: ' +
                        str(sum(LIST_OF_ANSWER_TIME)/len(LIST_OF_ANSWER_TIME)) + '\n')
