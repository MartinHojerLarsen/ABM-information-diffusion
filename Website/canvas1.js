// Canvas 1 code 

// Grid
var canvas = document.getElementById("canvas1");
var context = canvas.getContext("2d");

for (var x = 0.5; x < 501; x += 10) {
    context.moveTo(x, 0);
    context.lineTo(x, 500);
}

for (var y = 0.5; y < 500; y += 10) {
    context.moveTo(0, y);
    context.lineTo(500, y);
}

context.strokeStyle = "darkgray";
context.stroke();


