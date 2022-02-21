// Canvas 1 code 

function render_canvas1() {
    // Grid
    let canvas = document.getElementById("canvas1");
    let context = canvas.getContext("2d");
    
    // horisontal lines
    for (let x = 0.5; x < 401; x += 10) {
        context.moveTo(x, 0);
        context.lineTo(x, 400);
    }
    
    // vertical lines
    for (let y = 0.5; y < 401; y += 10) {
        context.moveTo(0, y);
        context.lineTo(400, y);
    }
    
    context.strokeStyle = "darkgray";
    context.stroke();
};
