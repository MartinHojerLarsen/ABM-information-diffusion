// Canvas 1 code 
let canvas = document.getElementById("canvas1");
let ctx = canvas.getContext("2d");

ctx.strokeStyle = "black";

// Border and background
ctx.moveTo(0,0);
ctx.rect(0, 0, canvas.width, canvas.height);
ctx.fillStyle = "white";
ctx.fillRect(0, 0, canvas.width, canvas.height);

ctx.stroke();

// Draw agent
function draw_agent(x, y, type, ID) {
    ctx.moveTo(x,y);
    ctx.beginPath();
    ctx.arc(x, y, 5, 0, 2*Math.PI);
    
    if (type == 0) {
        ctx.fillStyle = "red";
    } else if (type == 1) {
        ctx.fillStyle = "blue";
    } else {
        ctx.fillStyle = "gray";
    }
    ctx.fill();
    ctx.closePath();
    ctx.stroke();
};


// Random number for drawing agents
function randomInteger(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
};


draw_agent(randomInteger(0, 401), randomInteger(0, 401), randomInteger(0,3));
draw_agent(randomInteger(0, 401), randomInteger(0, 401), randomInteger(0,3));
draw_agent(randomInteger(0, 401), randomInteger(0, 401), randomInteger(0,3));
draw_agent(randomInteger(0, 401), randomInteger(0, 401), randomInteger(0,3));
draw_agent(randomInteger(0, 401), randomInteger(0, 401), randomInteger(0,3));