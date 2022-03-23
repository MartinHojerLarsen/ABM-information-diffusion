import {background,getCursorPosition,line,insideObj,change_cursor} from "/static/canvas_main.js";
import * as ag from "/static/agent_class.js";

window.addEventListener("load", function () {

//*** Canvas1 1 code ***//
let canvas1 = document.getElementById("canvas1");
let ctx1 = canvas1.getContext("2d");

// Background
let canvaWidth = document.getElementById('canvas_story_1_container').offsetWidth;
let canvaHeight = document.getElementById('canvas_story_1_container').offsetHeight;
background(canvas1, ctx1,canvaWidth,canvaHeight);

// Create agents
let commoner = new ag.Commoner(ctx1,1,2, 55, [1,2,3],(ctx1.canvas.width*0.50),(ctx1.canvas.height*0.35),110,0)
let r_influencer = new ag.R_influencer(ctx1,2,1, 90, [1,2,3],ctx1.canvas.width*0.25,ctx1.canvas.height*0.85,110,0);
let f_influencer = new ag.F_influencer(ctx1,3,0, -90, [1,2,3],ctx1.canvas.width*0.75,ctx1.canvas.height*0.85,110,0);

/*
*************
Animation
-------------
STORY TELLING
*************
*/

// Mouse interaction
let states = ['ph1','ph2']
let anim_state = states[0]

//on mousemove
canvas1.addEventListener('mousemove', function(e) {
    let mouse = getCursorPosition(canvas1, e)
    change_cursor([commoner,f_influencer,r_influencer],mouse)
});


// on click
canvas1.addEventListener('click', function(e) {
    let mouse = getCursorPosition(canvas1, e)
    insideObj(commoner,mouse) ? commoner.setSpeechBubble(true):commoner.setSpeechBubble(false);
    insideObj(r_influencer,mouse) ? r_influencer.setSpeechBubble(true):r_influencer.setSpeechBubble(false);
    insideObj(f_influencer,mouse) ? f_influencer.setSpeechBubble(true):f_influencer.setSpeechBubble(false);
});


let tick = 0;
let edgeThickness = 4;
// Create animation frames
function render() {
    requestAnimationFrame(render);
    background(canvas1, ctx1,canvaWidth,canvaHeight);
    
    tick += 1 // counter

    edgeThickness += 0.05 // edge thickness
    edgeThickness > 9 == true ? edgeThickness=4:edgeThickness;

    /****Agent Animations****/
    if(anim_state == states[0]){
        // Edges
        line(ctx1, commoner.getX(), commoner.getY(), r_influencer.getX(), r_influencer.getY(), edgeThickness);
        line(ctx1, commoner.getX(), commoner.getY(), f_influencer.getX(), f_influencer.getY(), edgeThickness);
        commoner.minorHover();
        r_influencer.minorHover();
        f_influencer.minorHover();
    }
}
render()
});