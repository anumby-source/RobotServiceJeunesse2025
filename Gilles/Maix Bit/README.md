# Reconnaissance de paneaux de signalisation avec la carte Maix Bit

On utilise le _self_learning_classifier_ de MaixPy : 

voir https://wiki.sipeed.com/soft/maixpy/en/course/ai/image/self_learn_classifier.html

## 1) Créer un compte sur le site maixhub : 

     https://maixhub.com

## 2) Récupération du code machine (code spécifique à chaque carte, nécessaire pour télécharger le modèle):
   
   voir    https://maixhub.com/share/6
   - se logger sur le site
   - télécharger _key.gen.bin_ (https://dl.sipeed.com/shareURL/MaixHub_Tools) et le flasher avec 
     kflash_gui sur la Maix Bit à l'adresse 0X000000
   - lancer un terminal (screen, putty, …) et rebooter la carte. Le code apparait dans la fenêtre.

## 3) Télécharger le firmware : 

     https://dl.sipeed.com/MAIX/MaixPy/release/master/
   
   Il faut prendre la version minimum nue ou avec IDE:
      https://dl.sipeed.com/shareURL/MAIX/MaixPy/release/master/maixpy_v0.6.3_2_gd8901fd22
   Puis flasher la carte

## 4) Télécharger le modèle sur MaixHub (utiliser le code machine récupéré au 1)) :
     
     https://maixhub.com/model/zoo/61
   et le charger sur la carte à l'adresse 0X300000

## 5) Charger et exécuter le script : self_learning_classifier.py
   
   (https://github.com/sipeed/MaixPy-v1_scripts/tree/master/machine_vision/self_learning_classifier)
  

