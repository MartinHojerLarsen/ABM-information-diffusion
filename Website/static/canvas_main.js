// *** Main canvas file *** //
// Containing all draw() functions //

// Background
function background(canvas, ctx) {
    ctx.strokeStyle = "black";
    
    // Size
    ctx.canvas.width = window.innerWidth;
    ctx.canvas.height = window.innerHeight;
    
    // Border and background
    ctx.moveTo(0,0);
    ctx.beginPath();
    ctx.rect(2, 2, canvas.width - 3, canvas.height - 3);
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.closePath();
    ctx.stroke();    
};

// Clear canvas
function clear_canvas(canvas, ctx) {
    ctx.moveTo(0,0);
    ctx.beginPath();
    ctx.rect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "white";
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.stroke();
    ctx.closePath();
};

// Commoner 
function commoner(ctx, x, y, size, ID=0, type=2, connections) {
    ctx.moveTo(0,0);
    ctx.beginPath();
    ctx.arc(x, y, size, 0, 2*Math.PI);
    ctx.closePath();
    ctx.stroke();
    ctx.fillStyle = "gray";
    ctx.fill();
};

// Real news influencer
function r_influencer(ctx, x, y, size, ID=0, type=1, opinion=100, connections) {
    ctx.beginPath();
    ctx.rect(x, y, size, size);
    ctx.closePath();
    ctx.stroke();
    ctx.fillStyle = color_agent(type, opinion);
    ctx.fill();
};

// Fake news influencer 
function f_influencer(ctx, x, y, size, ID=0, type=0, opinion=-100, connections) {
    ctx.beginPath();
    ctx.lineTo(x,y);
    ctx.lineTo(x-size, y+(size*2));
    ctx.lineTo(x+size, y+(size*2));
    ctx.closePath();
    ctx.stroke();
    ctx.fillStyle = color_agent(type, opinion);
    ctx.fill();
};

// Line (edge) 



//*** Helper functions ***//

// Random number for drawing agents - used for positions
function randomInteger(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
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


// Export
export {background, commoner, r_influencer, f_influencer, clear_canvas, randomInteger};