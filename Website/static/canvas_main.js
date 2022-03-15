// *** Main canvas file *** //
// Containing all draw() functions //

// Background
function background(canvas, ctx, color="#eeeaea") {
    
    // Size
    ctx.canvas.width = window.innerWidth;
    ctx.canvas.height = window.innerHeight;
    
    // Border and background
    ctx.moveTo(0,0);
    ctx.beginPath();
    ctx.rect(2, 2, canvas.width - 3, canvas.height - 3);
    ctx.fillStyle = color;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.closePath();
};

// Clear canvas
function clear_canvas(canvas, ctx, color="#eeeaea") {
    ctx.moveTo(0,0);
    ctx.beginPath();
    ctx.rect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = color;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.stroke();
    ctx.closePath();
};

// Commoner 
function commoner(ctx, x, y, size, ID=0, type=2, connections) {
    ctx.strokeStyle = "#4d4d4d";
    ctx.lineWidth = size/5;
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
    ctx.strokeStyle = "#0000b3";
    ctx.beginPath();
    ctx.rect(x, y, size, size);
    ctx.closePath();
    ctx.stroke();
    ctx.fillStyle = color_agent(type, opinion);
    ctx.fill();
};

// Fake news influencer 
function f_influencer(ctx, x, y, size, ID=0, type=0, opinion=-100, connections) {
    ctx.strokeStyle = "#b30000";
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
function line(ctx, x1, y1, x2, y2) {
    ctx.strokeStyle = "black";
    ctx.moveTo(x1,y1);
    ctx.beginPath();
    ctx.lineTo(x2, y2);
    ctx.closePath();
    ctx.stroke();
}


//*** Helper functions ***//

// Random number for drawing agents - used for positions
function randInt(min, max) {
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
export {background, commoner, r_influencer, f_influencer, clear_canvas, randInt, line};