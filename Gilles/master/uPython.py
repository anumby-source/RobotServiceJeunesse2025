##############################################################################################################
#
# Recherche les cartes Micropython sur les ports série du PC/Mac
#
##############################################################################################################


import sys, serial
from serial.tools.list_ports import comports
from time import sleep

class uPython():

    def __init__(self, port=None, speed=115200):
        ''' scan des ports USB. Si une carte MicroPython est trouvée, initialise self.serial '''
        print('************* initUSB: ', len(comports()), 'serial ports found ************')
        for p in comports():
            if port == None or port == p.device:
                print('   looking for micropython device on port ', p.device, ' (speed=', speed, 'bauds)')
                try:
                    s = serial.Serial(p.device, speed, write_timeout=2.)
                    sleep(0.1)
                    s.write(b'\x03')
                    sleep(2)
                    while s.in_waiting:
                        s.reset_input_buffer()
                        sleep(1)
                    s.write(b'\x03')
                    sleep(0.1)
                    ans = b''
                    while s.in_waiting:
                        ans += s.read(s.in_waiting)
                        sleep(1)
                    if ans == b'\r\n>>> ':    # carte Micropython trouvée
                        self.serial = s
                        self.cmd(b'import os', silent=True)
                        sleep(0.1)
                        s.reset_input_buffer()
                        ans = self.cmd(b'os.uname().machine', return_ans=True, silent=True)
                        board = ans[1].decode().strip("'")
                        print(board + ' found on port', p.device)
                        return
                    else:
                        s.close()
                except:
                    pass
        print('No Micropython board found!')
        return

    def cmd(self, com, return_ans=False, silent=False):
        ''' Envoi d'une commande à l'interface REPL de la carte
            com = commande pyboard, de la forme b'commande'
            Affiche la liste des lignes de la reponse shell
            Renvoie la liste des lignes si return_ans=True'''
        if type(com) != bytes:
            print("Error : command must be of the form : b'command'")
            return
        # on verifie que le buffer d'entrée est vide
        if self.serial.in_waiting != 0:
            self.serial.reset_input_buffer()   # on vide le buffer d'entrée
        # execution de la commande
        self.serial.write(com + b'\r')
        ans = b''
        # affichage de la réponse
        while ans != b'>>> ':
            ans = self.serial.read(self.serial.in_waiting)
            lines = ans.split(b'\r\n')
            ans = lines.pop()
            if not silent:
                for line in lines:
                    print(line.decode())
            sleep(0.05)
        if return_ans: return lines

    def reset(self):
        ''' Reset de la carte'''
        self.serial.write(b'\x04')

    def ctrlC(self):
        self.serial.write(b'\x03')