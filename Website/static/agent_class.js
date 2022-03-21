import { drawImageRot } from "/static/canvas_main.js";

// agent images
let commoner_img_face1 = document.getElementById('commonerFace1');
let rinfluencer_img_face1 = document.getElementById('rinfluencerFace1');
let finfluencer_img_face1 = document.getElementById('finfluencerFace1');

class Agent {
    constructor(ctx,ID, type, opinion, connections, x, y,size,rotation) {
        this.ctx = ctx;
        this.ID = ID;
        this.type = type;
        this.opinion = opinion;
        this.connections = connections;
        this.x = x;
        this.y = y;
        this.size = size;
        this.rotation = rotation;
    }

    // Getters 
    getID() {
        return this.ID;
    }

    getType() {
        return this.type;
    }

    getOpinion() {
        return this.opinion;
    }

    getConnections() {
        return this.connections;
    }

    getX() {
        return this.x;
    }

    getY() {
        return this.y;
    }

    getSize() {
        return this.size;
    }
    getRotation() {
        return this.rotation;
    }

    setRotation(newRotation) {
        this.rotation = newRotation;
    }
}

class Commoner extends Agent {
    constructor(ctx,ID, type, opinion, connections, x, y,size,rotation = 0) {
        super(ctx,ID, type, opinion, connections, x, y,size,rotation);

        this.y_upperB = y - 15
        this.y_lowerB = y + 15
        this.speed = 0.25
        this.dy = this.speed;
    }

    draw() {
        drawImageRot(this.ctx,commoner_img_face1,this.x,this.y,this.size,this.size,this.rotation); 
    }

    minorHover() {
        this.y += this.dy
        if(this.y > this.y_upperB) this.dy -= this.speed;
        if(this.y < this.y_lowerB) this.dy += this.speed;
    }

    update() {
        // Animation elements
        this.minorHover();

        // Draw animation
        this.draw()
    }
}

class R_influencer extends Agent {
    constructor(ctx,ID, type, opinion, connections, x, y,size,rotation) {
        super(ctx,ID, type, opinion, connections, x, y,size,rotation);
        
        this.y_upperB = y - 15
        this.y_lowerB = y + 15
        this.speed = 0.25
        this.dy = this.speed;
    }

    draw() {
        drawImageRot(this.ctx,rinfluencer_img_face1,this.x,this.y,this.size,this.size,this.rotation); 
    };

    minorHover() {
        this.y += this.dy
        if(this.y > this.y_upperB) this.dy -= this.speed;
        if(this.y < this.y_lowerB) this.dy += this.speed;
    }

    update() {
        // Animation elements
        this.minorHover();

        // Draw animation
        this.draw()
    }

}

class F_influencer extends Agent {
    constructor(ctx,ID, type, opinion, connections, x, y,size,rotation) {
        super(ctx,ID, type, opinion, connections, x, y,size,rotation);
    
        this.y_upperB = y - 15
        this.y_lowerB = y + 15
        this.speed = 0.25
        this.dy = this.speed;
    }

    draw() {
        drawImageRot(this.ctx,finfluencer_img_face1,this.x,this.y,this.size,this.size,this.rotation); 
    };

    minorHover() {
        this.y += this.dy
        if(this.y > this.y_upperB) this.dy -= this.speed;
        if(this.y < this.y_lowerB) this.dy += this.speed;
    }

    update() {
        // Animation elements
        this.minorHover();

        // Draw animation
        this.draw()
    }
}

export {Commoner,R_influencer,F_influencer};
