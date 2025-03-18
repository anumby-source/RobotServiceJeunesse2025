import random, time, os

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
    
def motor():
    return int(random.random()*100)

def detect():
    return random.randint(1, 6)
    

history = Steps()

t = time.time()

s = 1
while True:
    # print("s = ", s)
    town = detect()
    t += motor()
    history.addstep(s, town, t)
    if town == 6:
        break
    s += 1
    
os.remove('history.txt')

f = open("history.txt", "w+")

for h in sorted(history.keys()):
    print(f"history[{h}]={history.value(h)}\n")
    f.write(f"history[{h}]={history.value(h)}\n")
f.close()

    

    