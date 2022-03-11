import * as canvas_main from "/static/canvas_main.js";

//*** Canvas legend ***//  
let canvas_legend = document.getElementById("canvas_legend");
let ctx_legend = canvas_legend.getContext("2d");

ctx_legend.strokeStyle = "black";

// Size
ctx_legend.canvas.width = window.innerWidth;
ctx_legend.canvas.height = window.innerHeight;

ctx_legend.moveTo(0,0);

// Commoner 
canvas_main.commoner(ctx_legend, 100, 100, 50);


// Real news influencer
canvas_main.r_influencer(ctx_legend, 50, 250, 100);

// Fake news influencer
canvas_main.f_influencer(ctx_legend, 100, 450, 50);

