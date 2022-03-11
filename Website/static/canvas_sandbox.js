import * as canvas_main from "/static/canvas_main.js";

//*** Canvas sandbox code ***//
let canvas_sandbox = document.getElementById("canvas_sandbox");
let ctx_sandbox = canvas_sandbox.getContext("2d");

// Background
canvas_main.background(canvas_sandbox, ctx_sandbox);


// Create map of agents positions 
// map(ID, [x, y, type]) 
function agent_map(c, r, f) {
    // Create agents 
    let agent_map = new Map();
    for (let i = 0; i < parseInt(c) + parseInt(r) + parseInt(f); i++) {
        // Commoners
        if (i < parseInt(c)) {
            agent_map.set(i, [canvas_main.randomInteger(10, ctx_sandbox.canvas.width - 10), canvas_main.randomInteger(10, ctx_sandbox.canvas.width - 10), 2])   
            // Real news influencers
        } else if (i > parseInt(c)) {
            agent_map.set(i, [canvas_main.randomInteger(10, ctx_sandbox.canvas.width - 10), canvas_main.randomInteger(10, ctx_sandbox.canvas.width - 10), 1])   
            // Fake news influencers
        } else {
            agent_map.set(i, [canvas_main.randomInteger(10, ctx_sandbox.canvas.width - 10), canvas_main.randomInteger(10, ctx_sandbox.canvas.width - 10), 0])   
        }
    };
    
    console.log(agent_map);
    create_agents(agent_map);
};

// Creating agents based on user input 
// number of: commoners, real, fake agents
function create_agents(agent_map) {
    //******************************//
    // NÅET HERTIL - loopet der løber igennem agent_map skal kunne finde ID - altså keyen//
    //******************************//

    for (let i = 0; i < agent_map.size; i++) {
        if (agent_map.get(i)[2] == 2) {
            canvas_main.commoner(ctx_sandbox, agent_map.get(i)[0], agent_map.get(i)[1], 5, , e[2]);
        } else if (agent_map.get(i)[2] == 1) {
            canvas_main.r_influencer(ctx_sandbox, agent_map.get(i)[0], agent_map.get(i)[1], 10, e.value, e[2], canvas_main.randomInteger(0, 100));
        } else if (agent_map.get(i)[2] == 0) {
            canvas_main.f_influencer(ctx_sandbox, agent_map.get(i)[0], agent_map.get(i)[1], 5, e.value, e[2], canvas_main.randomInteger(-100, 0));
        }
    }
    
};



// User input
// Form handling
let sandbox_form = document.getElementById("form_sandbox");

sandbox_form.addEventListener("submit", function(e) {
    e.preventDefault();
    
    canvas_main.clear_canvas(canvas_sandbox, ctx_sandbox);
    
    let c = sandbox_form.elements["c"].value;
    let r = sandbox_form.elements["r"].value;
    let f = sandbox_form.elements["f"].value;
    
    agent_map(c, r, f);
    
    // stops refreshing page
    e.preventDefault();
});
