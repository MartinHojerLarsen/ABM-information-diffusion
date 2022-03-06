// Canvas 1 code 
let canvas = document.getElementById("canvas1");
let ctx = canvas.getContext("2d");

ctx.strokeStyle = "black";

// Border and background
ctx.moveTo(0,0);
ctx.rect(0, 0, canvas.width, canvas.height);
ctx.fillStyle = "white";
ctx.fillRect(0, 0, canvas.width, canvas.height);

ctx.stroke();

// Clear canvas of agents
function clear_canvas() {
    ctx.moveTo(0,0);
    ctx.rect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.stroke();
}


// Draw agent
function draw_agent(x, y, type, ID) {
    ctx.moveTo(x,y);
    ctx.beginPath();
    ctx.arc(x, y, 5, 0, 2*Math.PI);
    
    if (type == 0) {
        ctx.fillStyle = "red";
    } else if (type == 1) {
        ctx.fillStyle = "blue";
    } else {
        ctx.fillStyle = "gray";
    }
    ctx.fill();
    ctx.closePath();
    ctx.stroke();
};


// Random number for drawing agents
function randomInteger(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
};


// creating agents based on user input 
// number of: commoners, real, fake agents
function create_agents(c, r, f) {
    // commoners
    for (let i = 0; i < c; i++) {
        draw_agent(randomInteger(0, 401), randomInteger(0, 401), 2, i);
    }
    // real news influencers 
    for (let i = 0; i < r; i++) {
        draw_agent(randomInteger(0, 401), randomInteger(0, 401), 1, i);
    }
    // fake news influencers
    for (let i = 0; i < f; i++) {
        draw_agent(randomInteger(0, 401), randomInteger(0, 401), 0, i);
    }
}

let form = document.getElementById("form1");

form.addEventListener("submit", function(e) {
    clear_canvas();

    let c = form.elements["c"].value;
    let r = form.elements["r"].value;
    let f = form.elements["f"].value;
    
    create_agents(c, r, f);

    // stops refreshing page
    e.preventDefault();
});




// Notes: 

// To create a line in canvas (edges)
// ctx.beginPath();
// ctx.moveTo(xPos, yPos);
// ctx.lineTo(xPos, yPos); 
// ctx.closePath();