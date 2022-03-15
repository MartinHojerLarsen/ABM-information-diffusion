import * as canvas_main from "/static/canvas_main.js";

//*** Canvas1 1 code ***//
let canvas1 = document.getElementById("canvas1");
let ctx1 = canvas1.getContext("2d");

// Cackground
canvas_main.background(canvas1, ctx1);

// Commoner
canvas_main.commoner(ctx1, ctx1.canvas.width/2, 200, 80);

// Real news influencer
canvas_main.r_influencer(ctx1, ctx1.canvas.width * 0.25, 600, 140);

// Fake news influencer
canvas_main.f_influencer(ctx1, ctx1.canvas.width*0.75, 575, 80);