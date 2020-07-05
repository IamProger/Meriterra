"""This is dispatcher.
Goal is to receive task from client, find available calculator
and send it to it. Then receive uppercase variant of the string which client send
and send back to client"""

import socket
import threading
import json

with open('config.json') as f:       # Read config data
    config = json.load(f)
    port_for_client = config['dispatcher']['port_for_client_socket']
    port_for_check = config['dispatcher']['port_for_calculator_socket']
    port_for_calculator = config['calculator']['port_for_dispatcher_socket']

# create socket for interaction between client-dispatcher
CLIENT_DISPATCHER_SOCK = socket.socket(type=socket.SOCK_DGRAM)
CLIENT_DISPATCHER_SOCK.bind(('', port_for_client))

# create socket for checking state of calculators
CHECK_SOCK = socket.socket(type=socket.SOCK_DGRAM)
CHECK_SOCK.bind(('', port_for_check))

HEALTHY_CALCULATORS = set()


def check_calculators():
    """This function getting state from calculators"""
    while True:
        _, addr_check = CHECK_SOCK.recvfrom(1024)
        HEALTHY_CALCULATORS.add(addr_check[0])


t = threading.Thread(target=check_calculators)                 # launch function on another process
t.start()

while True:
    content, addr = CLIENT_DISPATCHER_SOCK.recvfrom(1024)      # get task from client
    while True:
        dispatcher_calculator_sock = socket.socket(type=socket.SOCK_DGRAM)
        dispatcher_calculator_sock.settimeout(16)
        for host in HEALTHY_CALCULATORS.copy():                # looking for available calculator
            try:
                dispatcher_calculator_sock.sendto(content, (host, port_for_calculator))
                data = dispatcher_calculator_sock.recvfrom(1024)[0]
                CLIENT_DISPATCHER_SOCK.sendto(data, addr)      # sending task to calculator
                dispatcher_calculator_sock.close()
                break
            except (socket.timeout, socket.error):
                HEALTHY_CALCULATORS.discard(host)          # if timeout or error mark that calculator is off or busy
        else:
            continue
        break
