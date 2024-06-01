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
const boutonHaut = document.getElementById("Haut");
const boutonBas = document.getElementById("Bas");
const boutonDroite = document.getElementById("droite");
const boutonGauche = document.getElementById("gauche");

let robot = {
    x: 100,
    y: 100,
    r: 30,
    direction: "haut"
};

const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");
drawRobot();

function drawRobot() {
    // Dessinez la tête
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.arc(robot.x, robot.y, robot.r, 0, 2 * Math.PI);
    ctx.fillStyle = "blue";
    ctx.fill();
};

// Ajoutez des écouteurs d'événements pour chaque bouton
boutonHaut.addEventListener("click", () => {
    robot.y -= 10;
    drawRobot();
    console.log(`Robot va vers le haut. Nouvelle position : (${robot.x}, ${robot.y})`);
});

boutonBas.addEventListener("click", () => {
    robot.y += 10;
    drawRobot();
    console.log(`Robot va vers le bas. Nouvelle position : (${robot.x}, ${robot.y})`);
});

boutonDroite.addEventListener("click", () => {
    robot.x += 10;
    drawRobot();
    console.log(`Robot va vers la droite. Nouvelle position : (${robot.x}, ${robot.y})`);
});

boutonGauche.addEventListener("click", () => {
    robot.x -= 10;
    drawRobot();
    console.log(`Robot va vers la gauche. Nouvelle position : (${robot.x}, ${robot.y})`);
});

