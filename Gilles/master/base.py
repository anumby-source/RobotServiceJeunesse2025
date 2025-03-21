import sys
import network
import espnow

# mac = b'$X|\x91\xe0\xd8'
# A WLAN interface must be active to send()/recv()
sta = network.WLAN(network.STA_IF)
sta.active(True)
e = espnow.ESPNow()
e.active(True)
print('espnow ok')
#
nbplayer = int(input())
addr_list = []

while len(addr_list) < nbplayer:
    addr, msg = e.recv()
    if addr not in addr_list:
        e.add_peer(addr)
        addr_list.append(addr)
        sys.stdout.write(msg)
#
cmd = input()
if cmd == 'start':
    e.send(cmd)
#
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