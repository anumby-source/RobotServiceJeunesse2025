from time import monotonic, sleep
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import Button, RadioButtons
import matplotlib.patches as mpatches
from serial.tools.list_ports import comports
from uPython import uPython
from serial import Serial

import matplotlib.pyplot as plt
import numpy as np

scenario = ['stop', 'sens-interdit', 'dep-interdit']

class master():

    def __init__(self, nplayers=1, port=None):

        self.nplayers = nplayers
        self.run = False
        self.start_t = 0
        self.axplayer = []
        self.fig = plt.figure(figsize=(10, 8))
        self.fig.set_facecolor('w')
        self.gs = GridSpec(6, 6, self.fig)
        self.create_chrono()
        self.create_buttons()
        self.create_radio_buttons()
        plt.tight_layout()
        # plt.show()

    def create_chrono(self):

        ax = self.fig.add_subplot(self.gs[0, 2:4])
        ax.axison = False
        ax.set_aspect('equal')
        self.chrono = plt.text(0.5, 0.5, '00.0', fontsize=35, color='g',
                                va='center', ha='center',
                                bbox=dict(boxstyle="round", fc="w", ec="k"))
        ax.add_artist(self.chrono)
        self.timer = self.fig.canvas.new_timer(interval=100)
        self.timer.add_callback(self.update_chrono)
        self.timer.add_callback(self.update_display)

    def create_buttons(self):

        ax = self.fig.add_axes([.7, .92, .1, .05])
        self.bStart = Button(ax, 'Start')
        self.bStart.on_clicked(self.start_stop)
        #
        ax = self.fig.add_axes([.7, .85, .1, .05])
        self.bReset = Button(ax, 'Reset')
        self.bReset.on_clicked(self.reset_chrono)
        #
        ax = self.fig.add_axes([.25, .85, .05, .05])
        self.bOk = Button(ax, 'OK')
        self.bOk.on_clicked(self.init_config)

    def create_radio_buttons(self):

        ax = self.fig.add_axes([.05, .9, .2, .05])
        ax.axison = False
        ax.text(0., 0.7, 'nombre de joueurs', fontsize=16, color='b',
                        bbox=dict(boxstyle="round", fc="w", ec="k"))
        ax = self.fig.add_axes([.1, .83, .15, .1])
        ax.axison = False
        self.radio = RadioButtons(ax, labels=('1', '2'), active=0,
                                    label_props={'fontsize': [12, 12]})
        self.radio.on_clicked(self.select_nb)

    def update_chrono(self):

        self.chrono.set_text('{:5.1f}'.format(monotonic()-self.start_t))

    def update_display(self):

        if not self.run: return

        if self.ser.in_waiting:
            msg = self.ser.read(self.ser.in_waiting)
            # print(msg)
            try:
                j, etape = msg.strip(b'\r\n').split(b':')
                j, etape = int(j), etape.decode()
                # print('joueur: {}  etape: {}'.f ormat(j+1, etape))
                if etape == scenario[self.progression[j]]:
                    tim = self.chrono.get_text()
                    self.etapes[j][self.progression[j]].set_text(tim)
                    self.progression[j] += 1
                    if self.progression[j] == len(scenario):
                        self.start_stop(None)
                        alert = plt.figure(figsize=(5,2), facecolor='g')
                        alert.text(0.1, 0.5, self.names[j] + " vainqueur !" , fontsize=26, color='w', va='center')
            except:
                print(msg)

    def start_stop(self, event):

        if self.run == False:
            self.ser.write(b'start\r\n')
            self.start_t = monotonic() - float(self.chrono.get_text())
            self.timer.start()
            self.run = True
            self.bStart.label.set_text('Stop')
        else:
            self.timer.stop()
            self.run = False
            self.bStart.label.set_text('Start')

    def reset_chrono(self, event):

        self.timer.stop()
        self.chrono.set_text('{:5.1f}'.format(0))
        self.run = False
        self.bStart.label.set_text('Start')

    def select_nb(self, label):

        self.nplayers = int(label)

    def init_config(self, event):

        for ax in self.axplayer:
            ax.remove()

        self.axplayer = []
        self.names = self.start_master()
        if self.names == None:
            return
        # names=['ROBOT 1']
        self.etapes = [[],[]]
        self.progression = [0, 0]

        for k in range(self.nplayers):
            ax = self.fig.add_subplot(self.gs[1:, 3*k:3*k+3])
            ax.set_xticks([])
            ax.set_yticks([])
            ax.text(.5, .95, self.names[k], color='b', fontsize=35, va='center', ha='center')
            for i, etape in enumerate(scenario):
                ax.text(.05, 0.8 - i*.1, etape, color='k', fontsize=26)
                t = ax.text(.75, 0.8 - i*.1, '000.0', color='r', fontsize=26)
                self.etapes[k].append(t)
            self.axplayer.append(ax)

    def start_master(self):

        u = uPython(port='COM10')
        #
        if not hasattr(u, 'serial'):
            alert = plt.figure(figsize=(4,2), facecolor='r')
            alert.text(0.1, 0.5, "Base non trouvée", fontsize=26, color='w', va='center')
            # plt.show()
            # raise Exception("ESP32C3 non trouvée")
            return
        #
        self.ser = u.serial
        self.ser.write(b'import base\r\n')
        self.ser.read(24)
        self.ser.write(str(self.nplayers).encode() + b'\r\n')
        self.ser.read(3)
        #
        ans = self.ser.read(self.nplayers * 7).decode()
        names = [ans[k*7:(k+1)*7] for k in range(self.nplayers)]
        #
        return names

if __name__ == '__main__':
    m = master()