// Canvas sandbox code 
let canvas_sandbox = document.getElementById("canvas_sandbox");
let ctx_sandbox = canvas_sandbox.getContext("2d");

ctx_sandbox.strokeStyle = "black";

// Size
ctx_sandbox.canvas.width = window.innerWidth;
ctx_sandbox.canvas.height = window.innerHeight;


// Border and background
ctx_sandbox.moveTo(0,0);
ctx_sandbox.rect(0, 0, canvas.width, canvas.height);
ctx_sandbox.fillStyle = "white";
ctx_sandbox.fillRect(0, 0, canvas.width, canvas.height);

ctx_sandbox.stroke();

// Clear canvas of agents
function clear_canvas() {
    ctx_sandbox.moveTo(0,0);
    ctx_sandbox.beginPath();
    ctx_sandbox.rect(0, 0, canvas.width, canvas.height);
    ctx_sandbox.fillStyle = "white";
    ctx_sandbox.fillRect(0, 0, canvas.width, canvas.height);
    ctx_sandbox.stroke();
    ctx_sandbox.closePath();
}


// Draw commoner agent - circle
function draw_c_agent(y, x, type, ID, opinion, connections,  i_factor, susceptibility) {
    ctx_sandbox.moveTo(y,x);
    ctx_sandbox.beginPath();
    ctx_sandbox.arc(y, x, 5, 0, 2*Math.PI);
    ctx_sandbox.closePath();
    ctx_sandbox.stroke();

    // color of agent 
    ctx_sandbox.fillStyle = "gray";
    ctx_sandbox.fill();
};

// Draw real news influencer agent - square
function draw_r_agent(x, y, type, ID, opinion, connections,  i_factor, susceptibility) {
    ctx_sandbox.moveTo(x,y);
    ctx_sandbox.beginPath();
    ctx_sandbox.rect(x, y, 10, 10);
    ctx_sandbox.closePath();
    ctx_sandbox.stroke();
    
    // color of agent 
    ctx_sandbox.fillStyle = color_agent(type, opinion);
    ctx_sandbox.fill();
};

// Drawing Fake news influencer agent - triangle
function draw_f_agent(x, y, type, ID, opinion, connections,  i_factor, susceptibility) {
    ctx_sandbox.moveTo(x,y);
    ctx_sandbox.beginPath();
    ctx_sandbox.lineTo(x-6, y-11);
    ctx_sandbox.lineTo(x-11, y);
    ctx_sandbox.lineTo(x, y);
    ctx_sandbox.closePath();
    ctx_sandbox.stroke();
    
    // color of agent 
    ctx_sandbox.fillStyle = color_agent(type, opinion);
    ctx_sandbox.fill();
};

// Setting color of agents - corresponding to their opinion
function color_agent(type, opinion) {
    // Fake news influencers
    if (type == 0) {
        if (opinion < -80) {
            return "red"
        } else if (opinion < -50) {
            return "#ff8080"
        } else {
            return "#ffcccc"
        }
    // Real news influencers
    } else if (type == 1) {
        if (opinion > 80) {
            return "blue"
        } else if (opinion > 50) {
            return "#0066ff"
        } else {
            return "#33ccff"
        }
    }
};

// Random number for drawing agents - used for positions
function randomInteger(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
};


// creating agents based on user input 
// number of: commoners, real, fake agents
function create_agents(c, r, f) {
    // commoners
    for (let i = 0; i < c; i++) {
        draw_c_agent(randomInteger(10, ctx_sandbox.canvas.width - 10), randomInteger(10, ctx_sandbox.canvas.height - 10), 2, i);
    }
    // real news influencers - ending position is -20px to x,y coords
    for (let i = 0; i < r; i++) {
        draw_r_agent(randomInteger(10, ctx_sandbox.canvas.width - 20), randomInteger(10, ctx_sandbox.canvas.height - 20), 1, i, randomInteger(0, 100));
    }
    // fake news influencers - starting position is +20px to x,y coords
    for (let i = 0; i < f; i++) {
        draw_f_agent(randomInteger(20, ctx_sandbox.canvas.width - 10), randomInteger(20, ctx_sandbox.canvas.height - 10), 0, i, randomInteger(-100, 0));
    }
}

let sandbox_form = document.getElementById("form_sandbox");

sandbox_form.addEventListener("submit", function(e) {
    clear_canvas();
    
    let c = sandbox_form.elements["c"].value;
    let r = sandbox_form.elements["r"].value;
    let f = sandbox_form.elements["f"].value;
    
    create_agents(c, r, f);
    
    // stops refreshing page
    e.preventDefault();
});
