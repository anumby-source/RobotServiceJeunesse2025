import random, time, os

VILLES = 6

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
    pass

def detect(t):
    return random.randint(1, VILLES), t + int(random.random() * 100)


def trajet1():
    """
    Premier algorithme:
    - le véhicule démarre
    - dès que l'on détecte la ville 1 on commence l'enregistrement de l'historique
    - on enregistre chaque détection de ville quel que soit l'ordre
    - on termine lorsque l'on détecte la ville VILLES

    Puis on écrit l'historique ordonné dans le fichier history.txt
    """
    history = Steps()

    t = 0
    s = 1

    while True:
        # print("s = ", s)
        town, t = detect(t)
        if town == 1:
            history.addstep(s, 1, t)
            s += 1
            break

    while True:
        # print("s = ", s)
        town, t = detect(t)
        history.addstep(s, town, t)
        if town == VILLES:
            break
        s += 1

    return history


def trajet2():
    """
    Deuxième algorithme:
    - le véhicule démarre
    - dès que l'on détecte la ville 1 on commence l'enregistrement de l'historique
    - on enregistre chaque détection de ville à condition que l'on suive l'ordre de villes prévu
    - on termine lorsque l'on détecte la ville VILLES

    Puis on écrit l'historique ordonné dans le fichier history.txt
    """
    ordre = range(1, VILLES)

    history = Steps()

    t = 0
    s = 1
    contrat = 1

    while True:
        # print("s = ", s)
        town, t = detect(t)
        if town == contrat:
            history.addstep(s, town, t)
            s += 1
            break

    contrat += 1

    while True:
        # print("s = ", s)
        town, t = detect(t)
        if town == contrat:
            history.addstep(s, town, t)
            s += 1
            contrat += 1
            if town == VILLES:
                break


    return history


history = trajet1()

f = open("history.txt", "w+")

for h in sorted(history.keys()):
    print(f"history[{h}]={history.value(h)}")
    f.write(f"history[{h}]={history.value(h)}\n")
f.close()

    

    