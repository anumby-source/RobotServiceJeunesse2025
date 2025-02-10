# On a installé Kicad v8

Puis on ajoute la librairie expressif qui fournit entre autres, les composants Kicad associés au ESP32-C3

https://github.com/espressif/kicad-libraries/tree/legacy_kicad7

La librairie est donc le fichier zip  espressif-kicad-addon.zip

Il faut utiliser l'outil "Gestionnaire de pluin et de contenu" qui va directement installer la librairie expressif à partir du fichier zib précédemment téléchargé

J'ai ajouté dans la librairie "Expressif" les composants nécessaires pour "esp32-c3-supermini" qui n'existaient pas dans la librairie de base

https://github.com/SurrealityLabs/esp32c3-wled

Mise à jour de la librairie (installée dans le commit)

"expressif-kicad-addon.zip"

# Nos développements pour le projet RobotJeunesse

Lors des développements effectués dans le cadre du Robot, j'ai été amenée à créer plusieurs éléments Kicad:
- des symboles,
- des empreintes associées

Ces éléments sont installés dans deux librairies:

1) https://github.com/anumby-source/RobotServiceJeunesse2025/blob/main/Vehicule/Kicad/Anumby.kicad_sym
2) https://github.com/anumby-source/RobotServiceJeunesse2025/tree/main/Vehicule/Kicad/Empreintes.pretty

Si vous souhaitez utiliser Kicad, pour développer dans le cadre de nos projets actuels, vous devrez importer ces librairies dans votre version de Kicad, ainsi les deux projets en cours seront modifiables:

1) https://github.com/anumby-source/RobotServiceJeunesse2025/tree/main/Vehicule/Kicad/T%C3%A9l%C3%A9commande
2) https://github.com/anumby-source/RobotServiceJeunesse2025/tree/main/Vehicule/Kicad/Robot

[Outil 3D](https://circuitcellar.com/research-design-hub/basics-of-design/create-3d-models-of-components-and-board-outlines-in-kicad/)


