// *** Main canvas file *** //
// Containing all draw() functions //
// let commoner_img = document.getElementById('commoner_img');

// Background
function background(canvas, ctx, width, height, color = "#eeeaea") {

    // Size
    ctx.canvas.width = width;
    ctx.canvas.height = height;

    // Border and background
    ctx.moveTo(0, 0);
    ctx.beginPath();
    ctx.rect(2, 2, canvas.width - 3, canvas.height - 3);
    ctx.fillStyle = color;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.closePath();
};

// Clear canvas
function clear_canvas(canvas, ctx, color = "#eeeaea") {
    ctx.moveTo(0, 0);
    ctx.beginPath();
    ctx.rect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = color;
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.stroke();
    ctx.closePath();
};

// Draw text on
function draw_text(ctx, text, x, y, txt_size = 30) {

    ctx.fillStyle = 'lightblue';
    ctx.fillRect(x - 125, y - 30, 250, 75)

    ctx.font = `italic ${txt_size}px Calibri`;
    ctx.strokeStyle = "black";
    ctx.textAlign = "center";
    ctx.strokeText(text, x, y + 20)
}

// Offset image x,y coordinates to center of image
function drawImageRot(ctx, img, x, y, width, height, deg) {
    //Convert degrees to radian
    var rad = deg * Math.PI / 180;
    //Set the origin to the center of the image
    ctx.translate(x, y);
    //Rotate the canvas around the origin
    ctx.rotate(rad);
    //draw the image
    ctx.drawImage(img, width / 2 * (-1), height / 2 * (-1), width, height);
    //reset the canvas
    ctx.rotate(rad * (-1));
    //
    ctx.translate((x) * (-1), (y) * (-1));
}

// Line (edge) 
function line(ctx, x1, y1, x2, y2, size = 1) {
    ctx.strokeStyle = "black";
    ctx.lineWidth = size;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
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
    console.log(cx, cy);

    let isInside = touchingCircle(object, cx, cy);
    // console.log(isInside);

    if (isInside) {
        document.body.style.cursor = "pointer";
    } else {
        document.body.style.cursor = "default";
    }

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

function getCursorPosition(canvas, event) {
    const rect = canvas.getBoundingClientRect()
    const mouseX = event.clientX - rect.left
    const mouseY = event.clientY - rect.top
    return { 'x': mouseX, 'y': mouseY }
}

function insideObj(obj, mousePos) {
    if (mousePos.x > obj.getX() - obj.getSize() / 2            // mouse x between x and x + width
        && mousePos.x < obj.getX() + obj.getSize() / 2
        && mousePos.y > obj.getY() - obj.getSize() / 2            // mouse y between y and y + height
        && mousePos.y < obj.getY() + obj.getSize() / 2) {
        return true
    }
    return false
}

function change_cursor(objArray,mousePos) {
    let checkList = [];
    for (let index = 0; index < objArray.length; index++) {
        checkList[index] = insideObj(objArray[index],mousePos);
    }
    if(checkList.includes(true)) {
        document.body.style.cursor = 'pointer';
    } else {
        document.body.style.cursor = 'default';
    }
}


// Export
export { background, clear_canvas, randInt, line, hover, drawImageRot, draw_text, getCursorPosition, insideObj,change_cursor};