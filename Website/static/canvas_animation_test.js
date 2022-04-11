let canvas_animation = document.getElementById("canvas_animation");
let ctx_animation = canvas_animation.getContext("2d");

let move = document.getElementById("move_animation");


var x = 10;
var y = 10;
var r = 10;
var duration = 500; // in ms
var nextX, nextY;
var startTime;


var WIDTH = ctx_animation.canvas.width;
var HEIGHT = ctx_animation.canvas.height;


function anim(time) {
    if (!startTime) // it's the first frame
    startTime = time || performance.now();
    
    // deltaTime should be in the range [0 ~ 1]
    var deltaTime = (time - startTime) / duration;
    // currentPos = previous position + (difference * deltaTime)
    var currentX = x + ((nextX - x) * deltaTime);
    var currentY = y + ((nextY - y) * deltaTime);
    
    if (deltaTime >= 1) { // this means we ended our animation
        x = nextX; // reset x variable
        y = nextY; // reset y variable
        startTime = null; // reset startTime
        draw(x, y); // draw the last frame, at required position
    } else {
        draw(currentX, currentY);
        requestAnimationFrame(anim); // do it again
    }
}

move.onclick = e => {
    nextX = +x_in.value || 0;
    nextY = +y_in.value || 0;
    anim();
}


function circle(x, y, r) {
    ctx_animation.beginPath();
    ctx_animation.arc(x, y, r, 0, Math.PI * 2, true);
    ctx_animation.fill();
    ctx_animation.closePath();
}

function clear() {
    ctx_animation.clearRect(0, 0, WIDTH, HEIGHT);
}


function draw(x, y) {
    clear(WIDTH, HEIGHT);
    ctx_animation.fillStyle = "white";
    circle(x, y, r);
}

draw(x, y);