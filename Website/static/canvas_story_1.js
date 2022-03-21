import * as canvas_main from "/static/canvas_main.js";
import * as ag from "/static/agent_class.js";

window.addEventListener("load", function () {

//*** Canvas1 1 code ***//
let canvas1 = document.getElementById("canvas1");
let ctx1 = canvas1.getContext("2d");

// Background
canvas_main.background(canvas1, ctx1);

// create agents
let commoner = new ag.Commoner(ctx1,1,2, 55, [1,2,3],(ctx1.canvas.width*0.50),(ctx1.canvas.height*0.25),200,0)
let r_influencer = new ag.R_influencer(ctx1,3,1, 90, [1,2,3],ctx1.canvas.width*0.25,ctx1.canvas.height*0.85,200,0);
let f_influencer = new ag.F_influencer(ctx1,2,0, -90, [1,2,3],ctx1.canvas.width*0.75,ctx1.canvas.height*0.85,200,0);

// Edges
// C -> R
canvas_main.line(ctx1, commoner.getX(), commoner.getY(), r_influencer.getX(), r_influencer.getY(), 4);
// C -> F
canvas_main.line(ctx1, commoner.getX(), commoner.getY(), f_influencer.getX(), f_influencer.getY(), 4);

// Animation


function render() {
    requestAnimationFrame(render);
    canvas_main.background(canvas1,ctx1);
    // C -> R
    canvas_main.line(ctx1, commoner.getX(), commoner.getY(), r_influencer.getX(), r_influencer.getY(), 4);
    // C -> F
    canvas_main.line(ctx1, commoner.getX(), commoner.getY(), f_influencer.getX(), f_influencer.getY(), 4);
    
    // Animation
    commoner.update();
    r_influencer.update();
    f_influencer.update();

}
render()

});