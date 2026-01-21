const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");


const scoreEl = document.getElementById("scoreValue");
const hitsEl = document.getElementById("hitsValue");
const nearHitsEl = document.getElementById("nearHitsValue");
const minDistEl = document.getElementById("minDistValue");
const angleEl = document.getElementById("angleValue");
const powerEl = document.getElementById("powerValue");
const speedControl = document.getElementById("speedControl");
const speedLabel = document.getElementById("speedLabel");

let ball = { x: 100, y: 430, vx: 0, vy: 0 };
let bin  = { x: 600, y: 430 };

let score = 0;
let hits = 0;
let nearHits = 0;
let throwsThisEpisode = 0;
const THROWS_PER_EPISODE = 25;
let minDist = Infinity;

const radius = 10;
const groundY = 430;
const dt = 0.25;
const gravity = 0.25;
const airDrag = 0.995;

let speedMultiplier = 1.0;

let trajectories = [];


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


async function throwBall() {
    const obs = [
        (bin.x - ball.x) / 800,
        (groundY - ball.y) / 600,
        ball.vx / 12,
        ball.vy / 12
    ];

    let data;
    try {
        const res = await fetch("/get_action", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ obs })
        });
        if (!res.ok) throw new Error(`Server returned ${res.status}`);
        data = await res.json();
    } catch (err) {
        console.warn("Server not reachable. Using fallback action.", err);
        data = { angle: 0.6, power: 12 };
    }


    const binDist = obs[0];
    const minAngle = 0.4, maxAngle = 1.0;
    let angle = minAngle + (maxAngle - minAngle) * binDist + data.angle * 0.2;
    angle = Math.min(Math.max(angle, minAngle), maxAngle);

    const minPower = 10, maxPower = 16;
    let power = minPower + (maxPower - minPower) * binDist + data.power * 1.0;
    power = Math.min(Math.max(power, minPower), maxPower);

    ball.vx = Math.cos(angle) * power;
    ball.vy = -Math.sin(angle) * power;

    angleEl.textContent = angle.toFixed(2);
    powerEl.textContent = power.toFixed(2);

    trajectories.push({ points: [{ x: ball.x, y: ball.y }], alpha: 1.0 });

    requestAnimationFrame(updateBall);
}

function updateBall() {
    ball.vx *= airDrag;
    ball.vy += gravity * speedMultiplier;

    ball.x += ball.vx * dt * speedMultiplier;
    ball.y += ball.vy * dt * speedMultiplier;

    if (ball.y > groundY) ball.y = groundY;

    if (trajectories.length > 0 && trajectories[trajectories.length - 1].points) {
        trajectories[trajectories.length - 1].points.push({ x: ball.x, y: ball.y });
    }

    draw();

    if (ball.y >= groundY && ball.vy >= 0) {
        const dist = Math.abs(ball.x - bin.x);
        minDist = Math.min(minDist, dist);
        minDistEl.textContent = minDist.toFixed(2);

        if (dist < 22) hits += 1;
        else if (dist < 50) nearHits += 1;

        score += dist < 50 ? 1 : 0;
        scoreEl.textContent = score;
        hitsEl.textContent = hits;
        nearHitsEl.textContent = nearHits;

        throwsThisEpisode += 1;

        ball = { x: 100, y: groundY, vx: 0, vy: 0 };
        bin.x = 200 + Math.random() * 400;
        trajectories.push({ points: [{ x: ball.x, y: ball.y }], alpha: 1.0 });

        if (throwsThisEpisode >= THROWS_PER_EPISODE) {
            hits = 0; nearHits = 0; throwsThisEpisode = 0; minDist = Infinity;
            hitsEl.textContent = hits;
            nearHitsEl.textContent = nearHits;
            minDistEl.textContent = minDist.toFixed(2);
        }

        setTimeout(throwBall, 600 / speedMultiplier);
        return;
    }

    requestAnimationFrame(updateBall);
}



speedControl.addEventListener("input", e => {
    speedMultiplier = parseFloat(e.target.value);
    speedLabel.textContent = `${speedMultiplier.toFixed(2)}x`;
});


draw();
throwBall();
