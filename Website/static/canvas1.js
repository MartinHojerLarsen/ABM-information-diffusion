import * as canvas_main from "/static/canvas_main.js";

//*** Canvas1 1 code ***//
let canvas1 = document.getElementById("canvas1");
let ctx1 = canvas1.getContext("2d");

// Background
canvas_main.background(canvas1, ctx1);

// Edges
// C -> R
canvas_main.line(ctx1, ctx1.canvas.width/2, 200, ctx1.canvas.width * 0.23, 700, 4);
// C -> F
canvas_main.line(ctx1, ctx1.canvas.width/2, 200, ctx1.canvas.width * 0.75, 700, 4);

// Commoner
let c = {
    x: (ctx1.canvas.width/2),
    y: 170,
    size: 200
};

canvas_main.commoner(ctx1, c.x, c.y, c.size);
// Hover handling - commoner - not really working correctly 
canvas1.addEventListener("mousemove", function(e) {
    canvas_main.hover(e, c);
});

// Real news influencer
let r = {
    x: ctx1.canvas.width * 0.20,
    y: 700,
    size: 250
}
canvas_main.r_influencer(ctx1, r.x, r.y, r.size);

// Fake news influencer
let f = {
    x: ctx1.canvas.width * 0.80,
    y: 730,
    size: 220
}
canvas_main.f_influencer(ctx1, f.x, f.y, f.size);

