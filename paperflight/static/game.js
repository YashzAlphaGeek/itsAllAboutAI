const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

// HUD references
const scoreEl = document.getElementById("scoreValue");
const angleEl = document.getElementById("angleValue");
const powerEl = document.getElementById("powerValue");
const speedControl = document.getElementById("speedControl");
const speedLabel = document.getElementById("speedLabel");

// World state
let ball = { x: 100, y: 420, vx: 0, vy: 0 };
let bin  = { x: 600, y: 420 };
let score = 0;

// Physics
const radius = 10;
const groundY = 430;
const dt = 0.25;
const velocityScale = 12;
const gravity = 0.25;

// Speed multiplier
let speedMultiplier = 1.0;

// Trajectories fading
let trajectories = [];

// --------------------
// Draw functions
// --------------------
function drawBackground() {
    ctx.fillStyle = "#eaf2f8";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#bfc9ca";
    ctx.fillRect(0, groundY, canvas.width, canvas.height - groundY);
}

function drawBin() {
    ctx.fillStyle = "#c0392b";
    ctx.fillRect(bin.x - 22, bin.y - 40, 44, 40);
    ctx.fillStyle = "#922b21";
    ctx.fillRect(bin.x - 26, bin.y - 42, 52, 6);
}

function drawBall() {
    ctx.fillStyle = "#2e86de";
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, radius, 0, Math.PI * 2);
    ctx.fill();
}

function drawTrajectories() {
    for (let traj of trajectories) {
        if (traj.points.length < 2) continue;
        ctx.strokeStyle = `rgba(41,128,185,${traj.alpha})`;
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(traj.points[0].x, traj.points[0].y);
        for (let i = 1; i < traj.points.length; i++) {
            ctx.lineTo(traj.points[i].x, traj.points[i].y);
        }
        ctx.stroke();
        traj.alpha -= 0.01 * speedMultiplier;
    }
    trajectories = trajectories.filter(traj => traj.alpha > 0);
}

function draw() {
    drawBackground();
    drawTrajectories();
    drawBin();
    drawBall();
}

// --------------------
// Throw logic
// --------------------
async function throwBall() {
    const obs = [
        (bin.x - ball.x)/canvas.width,
        (bin.y - ball.y)/canvas.height,
        ball.vx / velocityScale,
        ball.vy / velocityScale
    ];

    let data;
    try {
        const res = await fetch("/get_action", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ obs })
        });
        data = await res.json();
    } catch {
        console.error("Server not reachable");
        return;
    }

    const angle = data.angle;
    const power = data.power;

    angleEl.textContent = angle.toFixed(2);
    powerEl.textContent = power.toFixed(2);

    let currentTrajectory = { points: [{ x: ball.x, y: ball.y }], alpha: 1.0 };
    trajectories.push(currentTrajectory);

    ball.vx = Math.cos(angle) * power * velocityScale;
    ball.vy = -Math.sin(angle) * power * velocityScale;

    const interval = setInterval(() => {
        ball.vy += gravity * speedMultiplier;
        ball.x += ball.vx * dt * speedMultiplier;
        ball.y += ball.vy * dt * speedMultiplier;

        currentTrajectory.points.push({ x: ball.x, y: ball.y });
        draw();

        if (ball.y >= groundY) {
            clearInterval(interval);
            ball.y = groundY;

            if (Math.abs(ball.x - bin.x) < 22) {
                score += 1;
                scoreEl.textContent = score;
                bin.x = 200 + Math.random() * 400;
            }

            ball = { x: 100, y: groundY, vx: 0, vy: 0 };
            setTimeout(throwBall, 600 / speedMultiplier);
        }
    }, 16 / speedMultiplier);
}

// --------------------
// Speed slider
// --------------------
speedControl.addEventListener("input", e => {
    speedMultiplier = parseFloat(e.target.value);
    speedLabel.textContent = `${speedMultiplier.toFixed(2)}x`;
});

// --------------------
// Initialize
// --------------------
draw();
throwBall();
