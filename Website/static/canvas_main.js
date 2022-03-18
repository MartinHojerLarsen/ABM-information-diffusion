// *** Main canvas file *** //
// Containing all draw() functions //
let commoner_img = document.getElementById('commoner_img');
let f_influencer_img = document.getElementById('finfluencer_img');
let r_influencer_img = document.getElementById('rinfluencer_img');



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


// Offset image x,y coordinates to center of image
function drawImageRot(ctx,img,x,y,width,height,deg) {
    //Convert degrees to radian
    var rad = deg * Math.PI / 180;
    //Set the origin to the center of the image
    ctx.translate(x, y);
    //Rotate the canvas around the origin
    ctx.rotate(rad);
    //draw the image
    ctx.drawImage(img, width / 2 * (-1), height / 2 * (-1), width, height);
    //reset the canvas
    ctx.rotate(rad * ( -1 ) );
    //
    ctx.translate((x) * (-1), (y) * (-1));
  }

// Commoner
function commoner(ctx, x, y, size, ID=0, type=2, connections) {
    //ctx.drawImage(commoner_img,x,y,size,size);
    drawImageRot(ctx,commoner_img,x,y,size,size)
};

// Real news influencer
function r_influencer(ctx, x, y, size, ID=0, type=1, opinion=100, connections) {
    drawImageRot(ctx,r_influencer_img,x,y,size,size)
};

// Fake news influencer 
function f_influencer(ctx, x, y, size, ID=0, type=0, opinion=-100, connections) {
    drawImageRot(ctx,f_influencer_img,x,y,size,size)
};

// Line (edge) 
function line(ctx, x1, y1, x2, y2, size=1) {
    ctx.strokeStyle = "black";
    ctx.lineWidth = size;
    ctx.beginPath();
    ctx.moveTo(x1,y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
    ctx.closePath();
}


// Mouse hover handling
function hover(e, object) {
    e.preventDefault(); 
    e.stopPropagation();
    
    // Cursor position
    let cx = e.offsetX;
    let cy = e.offsetY;
    //console.log(cx, cy);
    
    let isInside = touchingCircle(object, cx, cy); 
    // console.log(isInside);
    
    if (isInside) {
        document.body.style.cursor = "pointer";
    } else {
        document.body.style.cursor = "default";
    }
    
}



//*** Helper functions ***//

// detect circle
// if(Math.pow(x-50,2)+Math.pow(y-50,2) < Math.pow(50,2))  
function touchingCircle(ob, x, y) {
    return Math.sqrt((x-ob.x) ** 2 + (y - ob.y) ** 2) < ob.size;
};

// detect square
function touchingSquare(ob, x, y) {
    let obX = ob.x;
    let obY = ob.y;
    let size = ob.size;
    
    // Returning true/false if (x,y) (mouse coords) are inside the object 
    return (x >= obX-size && x <= obX+size && y >= obY-size && y <= obY+size);
};

// detect triangle
function touchinTriangle(ob, x, y) {

};

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
export {background, commoner, r_influencer, f_influencer, clear_canvas, randInt, line, hover};