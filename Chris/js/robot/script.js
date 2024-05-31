/*
1: Contrôlez votre ESP32 à partir d’une page web! (version facile) - Tommy Desrochers
2: Application electron.js pour piloter un port série - Robot Maker
3: Créer une Interface Web pour ESP32 — Wikidebrouillard
4: Interface web pour un raspberry Pi et un Arduino - Programmation
5: Controlling a robot through a webpage - Stack Overflow

1 - tommydesrochers.com
2 - robot-maker.com
3 - wikidebrouillard.org
4 - robot-maker.com
5 - stackoverflow.com
*/


// Récupérez les références des boutons
const boutonAvant = document.getElementById("Avant");
const boutonArrière = document.getElementById("Arrière");
const boutonDroite = document.getElementById("droite");
const boutonGauche = document.getElementById("gauche");

// Ajoutez des écouteurs d'événements pour chaque bouton
boutonAvant.addEventListener("click", () => {
    // Code pour déplacer le robot vers l'e 'Avant
    console.log("Robot va vers l'e 'Avant");
});

boutonArrière.addEventListener("click", () => {
    // Code pour déplacer le robot vers l'Arrière
    console.log("Robot va vers l'Arrière");
});

boutonDroite.addEventListener("click", () => {
    // Code pour déplacer le robot vers la droite
    console.log("Robot va vers la droite");
});

boutonGauche.addEventListener("click", () => {
    // Code pour déplacer le robot vers la gauche
    console.log("Robot va vers la gauche");
});
