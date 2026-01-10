const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");
const logDiv = document.getElementById("log");
const scoreDiv = document.getElementById("score");

let ball = {x:100, y:450, vx:0, vy:0, angle:0};
let bin = {x:650, y:450};
let score = 0;
const gravity = 0.3;
const dt = 0.1;
const speedMultiplier = 3.0;
let particles = [];
let time = 0;

let throwsSinceMove = 0;
const throwsPerMove = 5;

function drawGround() {
    ctx.fillStyle = "#d0d7de";
    ctx.fillRect(0, 470, canvas.width, 30);
}

function drawTrajectory() {
    if(ball.vx===0 && ball.vy===0) return;
    let tempX = ball.x;
    let tempY = ball.y;
    let vx = ball.vx * dt;
    let vy = ball.vy * dt;

    ctx.strokeStyle = "rgba(52,152,219,0.5)";
    ctx.setLineDash([6,4]);
    ctx.beginPath();
    ctx.moveTo(tempX, tempY);

    for(let i=0;i<30;i++){
        vy += gravity * dt;
        tempX += vx;
        tempY += vy;
        if(tempY > 450) tempY = 450;
        ctx.lineTo(tempX, tempY);
        if(tempY >= 450) break;
    }
    ctx.stroke();
    ctx.setLineDash([]);
}

function drawParticles() {
    particles.forEach((p,index)=>{
        ctx.fillStyle = `rgba(255,165,0,${p.alpha})`;
        ctx.beginPath();
        ctx.arc(p.x,p.y,p.size,0,2*Math.PI);
        ctx.fill();
        p.x += p.vx;
        p.y += p.vy;
        p.alpha -= 0.05;
        if(p.alpha<=0) particles.splice(index,1);
    });
}

function drawBasket() {
    ctx.fillStyle = "#8B4513";
    ctx.fillRect(bin.x-20, bin.y-40, 40, 40);

    let wobble = Math.sin(time*0.2)*3;
    ctx.strokeStyle = "#5D2A00";
    ctx.lineWidth = 3;
    ctx.strokeRect(bin.x-20-wobble, bin.y-40-wobble, 40 + wobble*2, 40 + wobble*0.5);

    ctx.strokeStyle = "rgba(0,0,0,0.1)";
    ctx.strokeRect(bin.x-20-wobble, bin.y-40-wobble, 40 + wobble*2, 40 + wobble*0.5);

    // Label
    ctx.fillStyle = "#222";
    ctx.font = "14px Arial";
    ctx.textAlign = "center";
    ctx.fillText("Basket", bin.x, bin.y + 25);
}

function drawBall() {
    ctx.save();
    ctx.translate(ball.x, ball.y);
    ctx.rotate(ball.angle);
    ctx.fillStyle = "#ffffff";
    ctx.shadowColor = "rgba(0,0,0,0.2)";
    ctx.shadowBlur = 4;
    ctx.beginPath();
    ctx.arc(0,0,10,0,2*Math.PI);
    ctx.fill();
    ctx.strokeStyle = "#bbb";
    ctx.stroke();
    ctx.restore();

    // Label above ball
    ctx.fillStyle = "#333";
    ctx.font = "12px Arial";
    ctx.textAlign = "center";
    ctx.fillText("Paper Ball", ball.x, ball.y - 15);
}

function draw() {
    ctx.clearRect(0,0,canvas.width,canvas.height);
    drawGround();
    drawBasket();
    drawBall();
    drawTrajectory();
    drawParticles();
    scoreDiv.innerText = "Score: " + score;
    time++;
}

function resetBin() {
    bin.x = 400 + Math.random()*300;
}

function log(message){
    const p=document.createElement("div");
    p.innerText = message;
    logDiv.appendChild(p);
    logDiv.scrollTop = logDiv.scrollHeight;
}

function spawnParticles(x,y){
    for(let i=0;i<15;i++){
        particles.push({
            x:x, y:y,
            vx:(Math.random()-0.5)*2,
            vy:(Math.random()-1.5),
            size:Math.random()*3+2,
            alpha:1
        });
    }
}

async function throwBall() {
    const response = await fetch("/get_action", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({ball_x: ball.x, bin_x: bin.x})
    });
    const data = await response.json();
    let angle = data.angle;
    let power = data.power;
    ball.angle = angle;

    ball.vx = Math.cos(angle)*power*speedMultiplier;
    ball.vy = -Math.sin(angle)*power*speedMultiplier;

    const interval = setInterval(()=>{
        ball.vy += gravity;
        ball.x += ball.vx*dt;
        ball.y += ball.vy*dt;
        ball.angle += 0.1;
        draw();

        if(ball.y >= 450){
            clearInterval(interval);
            ball.y = 450;

            let dist = Math.abs(ball.x - bin.x);
            let hit = dist<20?1:(dist<50?0.5:0);
            score += hit;

            fetch("/update", {
                method:"POST",
                headers:{"Content-Type":"application/json"},
                body: JSON.stringify({reward: hit})
            });

            if(hit===1){
                spawnParticles(ball.x, ball.y);
                throwsSinceMove++;
                if(throwsSinceMove >= 5){ // move bin every 5 hits
                    resetBin();
                    throwsSinceMove=0;
                    log(`Hit! Bin moved to x=${bin.x.toFixed(0)}`);
                } else {
                    log(`Hit! Keep aiming at same bin.`);
                }
            } else {
                log(`Missed! Distance=${dist.toFixed(0)}`);
            }

            ball.x=100; ball.y=450; ball.vx=0; ball.vy=0;
            setTimeout(throwBall,300);
        }
    },20);
}

draw();
throwBall();
