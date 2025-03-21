import sys
import network
import espnow
from time import sleep_ms

# mac = b'$X|\x91\xe0\xd8'  # base MAC address
# espnow init
sta = network.WLAN(network.STA_IF)
sta.active(True)
e = espnow.ESPNow()
e.active(True)
print('espnow ok')
# get nbplayer from master
while (nbplayer := int(input())) not in (1, 2):
    pass
#
addr_list = []     #  player robot MAC address list
#  wait for robots connections
while (len(addr_list) < nbplayer):
    addr, msg = e.recv()
    if addr not in addr_list:
        e.add_peer(addr)
        addr_list.append(addr)
        sys.stdout.write(msg)
#  wait for start command from master
cmd = input()
if cmd == 'start':
    e.send(cmd)
#  receive robots messages and forward to master
while True:
    try:
        if e.any():
            addr, msg = e.recv()
            ind = addr_list.index(addr)
            fmsg = "{}:".format(ind) + msg.decode()
#             sys.stdout.write(fmsg.encode())
            print(fmsg)
    except KeyboardInterrupt:
        print("keyboard interrupt")
        break