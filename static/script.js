const canvas = document.getElementById("grid");
const GRID_SIZE = parseInt(canvas.dataset.gridSize, 10);
const ctx = canvas.getContext("2d");
const cell = canvas.width / GRID_SIZE;

let interval = null;

function draw(state) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    const cell = Math.floor(Math.min(canvas.width / GRID_SIZE, canvas.height / GRID_SIZE));

    for (let y = 0; y < GRID_SIZE; y++) {
        for (let x = 0; x < GRID_SIZE; x++) {
            if (state[y][x] === 1) ctx.fillStyle = "#4caf50"; // prey
            else if (state[y][x] === 2) ctx.fillStyle = "#f44336"; // predator
            else ctx.fillStyle = "#111"; // empty

            ctx.fillRect(x * cell, y * cell, cell, cell);
        }
    }
}

async function getState() {
    const res = await fetch("/state");
    return await res.json();
}

async function step() {
    await fetch("/step");
    const state = await getState();
    draw(state);
}

document.getElementById("step").onclick = step;

document.getElementById("start").onclick = () => {
    if (!interval) interval = setInterval(step, 100);
};

document.getElementById("stop").onclick = () => {
    clearInterval(interval);
    interval = null;
};

document.getElementById("reset").onclick = async () => {
    await fetch("/reset");
    const state = await getState();
    draw(state);
};

window.onload = async () => {
    const state = await getState();
    draw(state);
};
