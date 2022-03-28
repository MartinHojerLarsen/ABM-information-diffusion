import { drawImageRot, draw_text } from "/static/canvas_main.js";

// agent images
let commoner_img_normal = document.getElementById("commonerNormal");
let commoner_img_scared = document.getElementById("commonerScared");
let commoner_img_happy = document.getElementById("commonerHappy");
let rinfluencer_img_normal = document.getElementById("rinfluencerNormal");
let rinfluencer_img_influencing = document.getElementById("rinfluencerInfluencing");
let finfluencer_img_normal = document.getElementById("finfluencerNormal");
let finfluencer_img_influencing = document.getElementById("finfluencerInfluencing");

class Agent {
  constructor(ctx, ID, type, opinion, connections, x, y, size, rotation) {
    this.ctx = ctx;
    this.ID = ID;
    this.type = type;
    this.opinion = opinion;
    this.connections = connections;
    this.x = x;
    this.y = y;
    this.size = size;
    this.rotation = rotation;
    
    this.speechBubble = false;
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
  
  getSpeechBubble() {
    this.speechBubble
  }
  
  setSpeechBubble(bool) {
    this.speechBubble = bool;
  }
  
  setRotation(newRotation) {
    this.rotation = newRotation;
  }
  
};

class Commoner extends Agent {
  constructor(ctx, ID, type, opinion, connections, x, y, size, rotation = 0,speechBubble) {
    super(ctx, ID, type, opinion, connections, x, y, size, rotation,speechBubble);
    
    this.y_upperB = y - 15;
    this.y_lowerB = y + 15;
    this.speed = 0.25;
    this.dy = this.speed;
    this.face = commoner_img_normal;
  };
  
  draw(img) {
    //To be deleted
    //this.ctx.fillStyle = "lightgreen";
    // this.ctx.fillRect(
    //   this.x - this.size / 2,
    //   this.y - this.size / 2,
    //   this.size,
    //   this.size
    // );
    drawImageRot(
      this.ctx,
      img,
      this.x,
      this.y,
      this.size,
      this.size,
      this.rotation
    );
  };
    
  minorHover() {
    this.y += this.dy;
    if (this.y > this.y_upperB) this.dy -= this.speed;
    if (this.y < this.y_lowerB) this.dy += this.speed;
    
    // OnClick - show text and change face
    if (this.speechBubble) {
      draw_text(this.ctx, "I am a Commoner", this.x, this.y - 150);
      this.draw(commoner_img_happy);
    } else {
      this.draw(commoner_img_normal);
    };
  };
};
  
class R_influencer extends Agent {
  constructor(ctx, ID, type, opinion, connections, x, y, size, rotation,speechBubble) {
    super(ctx, ID, type, opinion, connections, x, y, size, rotation,speechBubble);
    
    this.y_upperB = y - 15;
    this.y_lowerB = y + 15;
    this.speed = 0.29;
    this.dy = this.speed;
  };
  
  draw(img) {
    //To be deleted
    // this.ctx.fillStyle = "lightgreen";
    // this.ctx.fillRect(
    //   this.x - this.size / 2,
    //   this.y - this.size / 2,
    //   this.size,
    //   this.size
    // );
    
  drawImageRot(
    this.ctx,
    img,
    this.x,
    this.y,
    this.size,
    this.size,
    this.rotation
    );
  };
    
  minorHover() {
    this.y += this.dy;
    if (this.y > this.y_upperB) this.dy -= this.speed;
    if (this.y < this.y_lowerB) this.dy += this.speed;
    
    if (this.speechBubble) {
      draw_text(this.ctx, "I am an Influencer", this.x, this.y - 150);
      this.draw(rinfluencer_img_influencing);
      
    } else {
      this.draw(rinfluencer_img_normal);
    };
    
  };
    
};
    
class F_influencer extends Agent {
  constructor(ctx, ID, type, opinion, connections, x, y, size, rotation,speechBubble) {
    super(ctx, ID, type, opinion, connections, x, y, size, rotation,speechBubble);
    
    this.y_upperB = y - 15;
    this.y_lowerB = y + 15;
    this.speed = 0.31;
    this.dy = this.speed;
  };
  
  draw(img) {
    //To be deleted
    // this.ctx.fillStyle = "lightgreen";
    // this.ctx.fillRect(
    //   this.x - this.size / 2,
    //   this.y - this.size / 2,
    //   this.size,
    //   this.size
    // );
    drawImageRot(
      this.ctx,
      img,
      this.x,
      this.y,
      this.size,
      this.size,
      this.rotation
      );
  };
    
  minorHover() {
    this.y += this.dy;
    if (this.y > this.y_upperB) this.dy -= this.speed;
    if (this.y < this.y_lowerB) this.dy += this.speed;
    
    if (this.speechBubble) {
      draw_text(this.ctx, "I am an Influencer", this.x, this.y - 150);
      this.draw(finfluencer_img_influencing);
    } else {
      this.draw(finfluencer_img_normal);
    };
  };
};
      
export { Commoner, R_influencer, F_influencer };