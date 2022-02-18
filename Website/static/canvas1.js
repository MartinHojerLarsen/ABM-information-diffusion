// Canvas 1 code 

// Grid
var canvas = document.getElementById("canvas1");
var context = canvas.getContext("2d");

// horisontal lines
for (var x = 0.5; x < 401; x += 10) {
    context.moveTo(x, 0);
    context.lineTo(x, 400);
}

// vertical lines
for (var y = 0.5; y < 401; y += 10) {
    context.moveTo(0, y);
    context.lineTo(400, y);
}

context.strokeStyle = "darkgray";
context.stroke();