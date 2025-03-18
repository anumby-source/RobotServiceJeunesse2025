import random

class Steps:
    def __init__(self):
        self.steps = dict()

    def addstep(self, num, name, time):
        print(num, name, time)
        self.steps[num] = (name, time)

    def keys(self):
        return self.steps.keys()

    def value(self, k):
        return self.steps[k]

history = Steps()

for s in range(6):
    # print("s = ", s)
    town = f"ville {s}"
    t = random.random()*100
    history.addstep(s, town, t)

f = open("history.txt", "w")
for h in history.keys():
    f.write(f"history[{h}]={history.value(h)}\n")
f.close()

    

    