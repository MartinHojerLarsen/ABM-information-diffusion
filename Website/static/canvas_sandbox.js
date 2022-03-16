import * as canvas_main from "/static/canvas_main.js";

//*** Canvas sandbox code ***//
let canvas_sandbox = document.getElementById("canvas_sandbox");
let ctx_sandbox = canvas_sandbox.getContext("2d");

// Background
canvas_main.background(canvas_sandbox, ctx_sandbox);


// ************************** //
// ****** NÅET HERTIL ****** //
// ************************** //
// Creates position for an agent - makes sure to avoid already taken positions
let posX = [];
let posY = [];
function createPositions(n) {
    
}

function checkN(n) {
    canvas_main.randInt(0, n-10);
}


// Make random connections 
function rand_connections() {
    let list = [];
    for (let i = 0; i < 5; i++) {
        list.push(canvas_main.randInt(0, 10))
    }
    return list;
}


// Create list of agents 
let agent_list = [];

function map_agents(c, r, f) {
    // Create agents 
    // Commoners
    if (c > 0) {
        for (let i = agent_list.length; i < c; i++) {
            let agent = new Agent(i, 2, canvas_main.randInt(-100, 100), rand_connections(), canvas_main.randInt(20, window.innerWidth -20), canvas_main.randInt(20, window.innerHeight -20))
            agent_list.push(agent);
        }
    }
    // Real news influencers
    if (r > 0) {
        for (let i = agent_list.length; i < (r + c); i++) {
            let agent = new Agent(i, 1, canvas_main.randInt(0, 100), [], canvas_main.randInt(10, window.innerWidth -30), canvas_main.randInt(10, window.innerHeight -30))
            agent_list.push(agent);
        }
    }
    // Fake news influencers
    if (f > 0) {
        for (let i = agent_list.length; i < (f + r); i++) {
            let agent = new Agent(i, 0, canvas_main.randInt(-100, 0), [], canvas_main.randInt(15, window.innerWidth -15), canvas_main.randInt(10, window.innerHeight -30))
            agent_list.push(agent);
        }
    }
    console.log("Agent List:")
    console.log(agent_list);
    create_edges(agent_list);
    create_agents(agent_list);
};


// Creating agents based on user input 
// number of: commoners, real, fake agents
function create_agents(agent_list) {
    agent_list.forEach(e => {
        // Commoner
        if (e.getType() == 2) {
            canvas_main.commoner(ctx_sandbox, e.getX(), e.getY(), 10, e.getID(), e.getType());
        }
        // Real news influencer
        if (e.getType() == 1) {
            canvas_main.r_influencer(ctx_sandbox, e.getX(), e.getY(), 20, e.getID(), e.getType());
        }
        // Fake news influencer
        if (e.getType() == 0) {
            canvas_main.f_influencer(ctx_sandbox, e.getX(), e.getY(), 10, e.getID(), e.getType());
        }
    });
};

// ************************** //
// ****** NÅET HERTIL ****** //
// ************************** //
// Create edges between connected agents
function create_edges(agent_list) {
    for (let i = 0; i < agent_list.length; i++) {
        let cl = agent_list[i].getConnections();
        for (let j = 0; j < cl.length; j++) {
            let ID2 = cl[j]
            let x2 = agent_list[ID2].getX();
            let y2 = agent_list[ID2].getY();;
            canvas_main.line(ctx_sandbox, agent_list[i].getX(), agent_list[i].getY(), x2, y2);
        }
    }
}


// User input
// Form handling
let sandbox_form = document.getElementById("form_sandbox");

sandbox_form.addEventListener("submit", function(e) {
    e.preventDefault();
    
    canvas_main.clear_canvas(canvas_sandbox, ctx_sandbox);
    
    let c = parseInt(sandbox_form.elements["c"].value);
    let r = parseInt(sandbox_form.elements["r"].value);
    let f = parseInt(sandbox_form.elements["f"].value);
    
    createPositions((c+r+f));
    map_agents(c, r, f);
    
    // stops refreshing page
    e.preventDefault();
});
