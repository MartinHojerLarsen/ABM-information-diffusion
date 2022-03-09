// Canvas sandbox code 
let canvas = document.getElementById("canvas1");
let ctx = canvas.getContext("2d");

ctx.strokeStyle = "black";

// Size
ctx.canvas.width = window.innerWidth;
ctx.canvas.height = window.innerHeight;


// Border and background
ctx.moveTo(0,0);
ctx.beginPath();
ctx.rect(1, 1, canvas.width-2, canvas.height-2);
ctx.fillStyle = "white";
ctx.fillRect(0, 0, canvas.width, canvas.height);
ctx.closePath();
ctx.stroke();

// Commoner 
ctx.beginPath();
ctx.arc(900, 800, 50, 0, 2*Math.PI);
ctx.closePath();
ctx.stroke();
ctx.fillStyle = "gray";
ctx.fill();

// Real news influencer
ctx.beginPath();
ctx.rect(300, 300, 50, 50);
ctx.closePath();
ctx.stroke();
ctx.fillStyle = "blue";
ctx.fill();


// Fake news influencer
function draw_f_agent(x, y) {
    ctx.moveTo(x,y);
    ctx.beginPath();
    ctx.lineTo(x-25, y-50);
    ctx.lineTo(x-25, y);
    ctx.lineTo(x, y);
    ctx.closePath();
    ctx.stroke();
    ctx.fillStyle = "red";
    ctx.fill();
};
draw_f_agent(100,100);