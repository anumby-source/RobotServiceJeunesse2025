########################################################
#             Connection réseau
#
#   >>> from WifiConnect import WifiConnect
#   >>> WifiConnect(True)
#   ou
#   >>> execfile('WifiConnect.py')
#
########################################################

import network
from machine import Pin
from time import sleep
import sys

def WifiConnect(lan=None):
    credentials = { 'KIWI_11091':'iSpEnJ2q',
                    'iPhone de Gilles':'sx8tuu5zx1jdr',
                    'Livebox-FDB5':'33311297193A5A1733FF813783',
                    'Wifi-Eleves':'a$@0910626L',
#                     'Wifi-Profs':'&*%@0910626L',
                    'Bbox-0989EBA7':'Zppcz1UU61wwp7P2VN'}

    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(False)                     # disable wifi access point
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    lanlist = sta.scan()
    
    for nets in lanlist:
        ssid = nets[0].decode()
        if (not lan and ssid in credentials.keys()) or (ssid==lan):
            print('*** WifiConnect: trying connection to ', ssid)
            sta.connect(ssid, credentials[ssid])
            try:
                while not sta.isconnected():
                    sleep(1)
                    sys.stdout.write(b'.')
                print('\n*** WifiConnect: connection successfull :', sta.ifconfig()[0])
            except KeyboardInterrupt:
                print('\n*** WifiConnect: connection failed')
            return sta
    print('*** WifiConnect ***')
    if lan:        
        print('   lan ' + lan + ' is not reachable')
    else:
        print('   no reachable lan')
    print('   discovered lans:')
    for lan in lanlist:
        print(lan)
    return False

if __name__ == '__main__':
    WifiConnect()