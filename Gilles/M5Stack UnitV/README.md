# Reconnaissance de panneaux de signalisation avec la carte M5Stack UnitV

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

### 4) Télécharger le modèle sur MaixHub (utiliser le code machine récupéré au 1)) :
     
     https://maixhub.com/model/zoo/61
   
   et le charger sur la carte avec kflash_gui à l'adresse 0X300000

### 5) Sur une carte micro-SD, charger _3_panneaux.classifier_ et _classifiy.py_
   
    Inserer la carte micro-SD dans le M5Stack UnitV et lancer le script _classify.py_ 
      
