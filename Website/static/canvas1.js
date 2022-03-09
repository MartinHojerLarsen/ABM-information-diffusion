// Canvas sandbox code 
let canvas = document.getElementById("canvas1");
let ctx = canvas.getContext("2d");

ctx.strokeStyle = "black";

// Size
ctx.canvas.width = window.innerWidth;
ctx.canvas.height = window.innerHeight;


// Border and background
ctx.moveTo(0,0);
ctx.rect(0, 0, canvas.width, canvas.height);
ctx.fillStyle = "white";
ctx.fillRect(0, 0, canvas.width, canvas.height);

ctx.stroke();