## Reconnaissance de panneaux de signalisation avec la carte M5Stack UnitV

voir :     https://wiki.sipeed.com/soft/maixpy/en/course/ai/image/self_learn_classifier.html

### 1) Créer un compte sur MaixHub : 
    
    https://maixhub.com

### 2) Récupération du code machine du module M5Stack UnitV (nécessaire pour télécharger le modèle):
   
   voir https://maixhub.com/share/6
   - se logger sur le site MaixHub
   - télécharger key.gen.bin (https://dl.sipeed.com/shareURL/MaixHub_Tools) et le flasher avec 
     kflash_gui sur la carte UnitV à l'adresse 0X000000
   - lancer un terminal (screen, putty, …) et rebooter la carte. Le code apparait dans la fenêtre.

### 3) Installer le firmware : 

Flasher le firmrware (fichier _M5StickV_Firmware_v5.1.2.kfpkg_) avec kflash_gui

![Flash firmware](https://github.com/user-attachments/assets/22ee4d43-eabd-41df-bd9a-1d606ebbcc3e)

### 4) Télécharger le modèle sur MaixHub (utiliser le code machine récupéré au 2) ) :
     
     https://maixhub.com/model/zoo/61
   
et le charger sur la carte avec kflash_gui à l'adresse 0X300000

![Flash kmodel](https://github.com/user-attachments/assets/df5b09c9-7f6f-418e-9d61-fabbc00d21bd)

### 5) Sur une carte micro-SD, charger _3_panneaux.classifier_ et _classify.py_
   
Inserer la carte micro-SD dans le M5Stack UnitV et lancer le script _classify.py_ 

Il est aussi possible de charger des fichiers (en particulier 3_panneaux.classifier) directement dans la mémoire flash de la M5Stack UnitV, sans utiliser la carte SD, dans MaixPy IDE : onglet "Tools > transfert file to board".

Pour chaque panneau reconnu, la led de la carte s'allume :
   - rouge -> stop
   - vert -> sens interdit
   - bleu -> dépassement interdit
      

## Connecteur Grove 

* 4 - GND noir
* 3 - VCC orange
* 2 - TX/SDA jaune
* 1 - RX/SCL blanc

* ![image](https://github.com/user-attachments/assets/2ac6458e-cd73-4ef4-918b-d3d32a30b153)
* ![image](https://github.com/user-attachments/assets/c72b4672-5137-4473-9a05-a35cb2121fff)
* 

