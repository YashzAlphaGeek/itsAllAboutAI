const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const logDiv = document.getElementById("log");
const scoreDiv = document.getElementById("score");

let ball = {x:100, y:450, vx:0, vy:0};
let bin = {x:650, y:450};
let score = 0;
const gravity = 0.3;
const dt = 0.1;
const speedMultiplier = 3.0;

function drawTrajectory(angle, power) {
    let tempX = 100;
    let tempY = 450;
    let vx = Math.cos(angle) * power * speedMultiplier * dt;
    let vy = -Math.sin(angle) * power * speedMultiplier * dt;

    ctx.strokeStyle = "rgba(0,0,255,0.3)";
    ctx.beginPath();
    ctx.moveTo(tempX, tempY);

    for(let i=0; i<100; i++){
        vy += gravity * dt;
        tempX += vx;
        tempY += vy;
        if(tempY > 450) tempY = 450;
        ctx.lineTo(tempX, tempY);
        if(tempY >= 450) break;
    }
    ctx.stroke();
}

function draw() {
    ctx.clearRect(0,0,canvas.width,canvas.height);

    ctx.fillStyle = "#ff6347";
    ctx.fillRect(bin.x-15, bin.y-30, 30, 30);
    ctx.strokeStyle = "#000";
    ctx.strokeRect(bin.x-15, bin.y-30, 30, 30);

    ctx.fillStyle = "#1e90ff";
    ctx.beginPath();
    ctx.arc(ball.x, ball.y, 10,0,2*Math.PI);
    ctx.fill();

    scoreDiv.innerText = "Score: " + score;
}

function resetBin() {
    bin.x = 400 + Math.random()*300;
}

function log(message) {
    const p = document.createElement("div");
    p.innerText = message;
    logDiv.appendChild(p);
    logDiv.scrollTop = logDiv.scrollHeight;
}

async function throwBall() {
    const response = await fetch("/get_action", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({ball_x: ball.x})
    });
    const data = await response.json();
    let angle = data.angle;
    let power = data.power;

    draw();
    drawTrajectory(angle, power);

    ball.vx = Math.cos(angle) * power * speedMultiplier;
    ball.vy = -Math.sin(angle) * power * speedMultiplier;

    const interval = setInterval(()=>{
        ball.vy += gravity;
        ball.x += ball.vx * dt;
        ball.y += ball.vy * dt;

        draw();

        if(ball.y >= 450){
            clearInterval(interval);
            ball.y = 450;

            let dist = Math.abs(ball.x - bin.x);
            let hit = dist < 20 ? 1 : (dist < 50 ? 0.5 : 0);

            score += hit;

            fetch("/update", {
                method:"POST",
                headers:{"Content-Type":"application/json"},
                body: JSON.stringify({reward: hit})
            });

            ball.x=100; ball.y=450; ball.vx=0; ball.vy=0;

            if(hit === 1){
                resetBin();
                log(`Hit! Bin moved to x=${bin.x.toFixed(0)}`);
            } else {
                log(`Missed! Distance=${dist.toFixed(0)}`);
            }

            setTimeout(throwBall, 300);
        }
    }, 20);
}

draw();
throwBall();
