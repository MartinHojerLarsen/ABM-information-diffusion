// Canvas sandbox code 
let canvas_sandbox = document.getElementById("canvas_sandbox");
let ctx_sandbox = canvas.getContext("2d");

ctx_sandbox.strokeStyle = "black";

// Size
ctx_sandbox.canvas_sandbox.width = window.innerWidth;
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


// Draw agent
function draw_agent(y, x, type, ID) {
    ctx_sandbox.moveTo(y,x);
    ctx_sandbox.beginPath();
    ctx_sandbox.arc(y, x, 5, 0, 2*Math.PI);
    ctx_sandbox.stroke();
    
    if (type == 0) {
        ctx_sandbox.fillStyle = "red";
    } else if (type == 1) {
        ctx_sandbox.fillStyle = "blue";
    } else {
        ctx_sandbox.fillStyle = "gray";
    }
    ctx_sandbox.fill();
    ctx_sandbox.closePath();
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
        draw_agent(randomInteger(10, ctx_sandbox.canvas.width - 10), randomInteger(10, ctx_sandbox.canvas.height - 10), 2, i);
    }
    // real news influencers 
    for (let i = 0; i < r; i++) {
        draw_agent(randomInteger(10, ctx_sandbox.canvas.width - 10), randomInteger(10, ctx_sandbox.canvas.height - 10), 1, i);
    }
    // fake news influencers
    for (let i = 0; i < f; i++) {
        draw_agent(randomInteger(10, ctx_sandbox.canvas.width - 10), randomInteger(10, ctx_sandbox.canvas.height - 10), 0, i);
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




// Notes: 

// To create a line in canvas (edges)
// ctx_sandbox.beginPath();
// ctx_sandbox.moveTo(xPos, yPos);
// ctx_sandbox.lineTo(xPos, yPos); 
// ctx_sandbox.closePath();