from time import monotonic, sleep
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import Button, CheckButtons
from serial.tools.list_ports import comports
from uPython import uPython
from serial import Serial
import matplotlib.pyplot as plt

# scenario = ['stop', 'sens-interdit', 'dep-interdit']
scenario = ['Paris', 'Sens', 'Lyon', 'Marseille', 'Toulon']
robot_list = ['robot 1', 'robot 2', 'robot 3', 'robot 4', 'robot 5', 'robot 6']
plt.ion()

class master():

    def __init__(self, port=None):

        self.connect_to_base(port=port)
        self.start_base()
        self.run = False
        self.start_t = 0                           # for timing purpose
        self.players = []                          # list of robot number (2 max)
        self.axplayer = []                         # list of score displays (2 max)
        self.etapes = [[],[]]
        self.progression = [0, 0]                  # players progression
        self.fig = plt.figure(figsize=(10, 8))
        self.fig.set_facecolor('w')
        self.gs = GridSpec(6, 6, self.fig)
        self.create_chrono()
        self.create_buttons()
        self.create_check_buttons()
        plt.tight_layout()
        plt.show()

    def create_chrono(self):
        ''' Create chrono timer and display '''

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
        ''' Create game management buttons '''

        ax = self.fig.add_axes([.7, .92, .1, .05])
        self.bStart = Button(ax, 'Start')
        self.bStart.on_clicked(self.start_stop)
        #
        ax = self.fig.add_axes([.7, .85, .1, .05])
        self.bClear = Button(ax, 'Clear')
        self.bClear.on_clicked(self.clear_chrono)
        #
        ax = self.fig.add_axes([.25, .88, .05, .05])
        self.bReset = Button(ax, 'Reset')
        self.bReset.on_clicked(self.reset_players)

    def create_check_buttons(self):
        ''' Create robot selection buttons '''

        ax = self.fig.add_axes([.05, .80, .15, .2])
        ax.axison = False
        self.check = CheckButtons(ax, labels=robot_list, actives=(False,)*6, label_props={'fontsize': [12, 12]})
        self.check.on_clicked(self.select_players)

    def update_chrono(self):
        ''' Update chrono display '''

        self.chrono.set_text('{:5.1f}'.format(monotonic()-self.start_t))

    def update_display(self):
        ''' Read serial buffer and update score display '''

        if self.ser.in_waiting:
            msg = self.ser.read(self.ser.in_waiting).strip()
            print(msg)
            j, etape = msg.split(b':')
            j, etape = int(j), etape.decode()
            if j in self.players:
                ind = self.players.index(j)
                print('robot: {}  etape: {}  en route vers: {}'.format(j, etape, scenario[self.progression[ind]]))
                if etape == scenario[self.progression[ind]]:
                    tim = self.chrono.get_text()
                    self.etapes[ind][self.progression[ind]].set_text(tim)
                    self.progression[ind] += 1
                    if self.progression[ind] == len(scenario):
                        self.start_stop(None)
                        alert = plt.figure(figsize=(4.5, 2), facecolor='g')
                        alert.text(0.1, 0.5, robot_list[j-1] + " vainqueur !" , fontsize=26, color='w', va='center')
        return

    def start_stop(self, event):
        ''' Start/Stop button handler '''

        if self.run == False:
            self.start_t = monotonic() - float(self.chrono.get_text())
            self.timer.start()
            self.run = True
            self.bStart.label.set_text('Stop')
            self.ser.read(self.ser.in_waiting)    # empty serial buffer
        else:
            self.timer.stop()
            self.run = False
            self.bStart.label.set_text('Start')

    def clear_chrono(self, event):
        ''' Stop chrono and set to 0'''

        self.timer.stop()
        self.chrono.set_text('{:5.1f}'.format(0))
        self.run = False
        self.bStart.label.set_text('Start')

    def reset_players(self, event):
        ''' Reset game '''

        for k in range(len(robot_list)):
            if self.check.get_status()[k]:
                self.check.eventson = False    # disable event to prevent call to select_players
                self.check.set_active(k)
                self.check.eventson = True     # enable event

        # remove all players score display
        for ax in self.axplayer:
            ax.remove()

        self.timer.stop()
        self.clear_chrono(None)
        self.run = False
        self.bStart.label.set_text('Start')

        self.axplayer = []
        self.players = []
        self.etapes = [[],[]]
        self.progression = [0, 0]
        return

    def select_players(self, label):
        ''' Select one or to robots and initialize score display '''

        ind = robot_list.index(label)
        selected = self.check.get_status()[ind]

        if (not selected) or (self.check.get_status().count(True) > 2):  # already selected or more than 2 robots
            self.check.eventson = False    # disable event to prevent recursion
            self.check.set_active(ind)
            self.check.eventson = True     # enable event
            return

        robot_num = ind + 1
        k = len(self.axplayer)
        # create player score display
        ax = self.fig.add_subplot(self.gs[1:, 3*k:3*k+3])
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(.5, .95, label, color='b', fontsize=35, va='center', ha='center')
        for i, etape in enumerate(scenario):
            ax.text(.05, 0.8 - i*.1, etape, color='k', fontsize=26)
            t = ax.text(.75, 0.8 - i*.1, '000.0', color='r', fontsize=26)
            self.etapes[k].append(t)
        self.axplayer.append(ax)
        self.players.append(robot_num)

    def start_base(self):
        ''' Send start command to base '''

        print('starting base')
        # start base
        self.ser.write(b'import base\r\n')
        ans = self.ser.read(24)
        # print(ans)

    def connect_to_base(self, port=None):
        ''' Look for Micropython device connected to a serial port '''

        u = uPython(port=port)
        #
        if not hasattr(u, 'serial'):
            alert = plt.figure(figsize=(4,2), facecolor='r')
            alert.text(0.1, 0.5, "Base non trouvée", fontsize=26, color='w', va='center')
            raise Exception("base not found")
        #
        self.ser = u.serial

if __name__ == '__main__':
    m = master()
    # m = master(port='COM10')
    # m = master(port='/dev/cu.usbmodem14101')