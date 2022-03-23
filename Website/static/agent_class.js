import { drawImageRot, draw_text } from "/static/canvas_main.js";

// agent images
let commoner_img_face1 = document.getElementById("commonerFace1");
let rinfluencer_img_face1 = document.getElementById("rinfluencerFace1");
let finfluencer_img_face1 = document.getElementById("finfluencerFace1");

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

}

class Commoner extends Agent {
  constructor(ctx, ID, type, opinion, connections, x, y, size, rotation = 0,speechBubble) {
    super(ctx, ID, type, opinion, connections, x, y, size, rotation,speechBubble);

    this.y_upperB = y - 15;
    this.y_lowerB = y + 15;
    this.speed = 0.25;
    this.dy = this.speed;
  }

  draw() {
    //To be deleted
    this.ctx.fillStyle = "lightgreen";
    this.ctx.fillRect(
      this.x - this.size / 2,
      this.y - this.size / 2,
      this.size,
      this.size
    );
    drawImageRot(
      this.ctx,
      commoner_img_face1,
      this.x,
      this.y,
      this.size,
      this.size,
      this.rotation
    );
  }

  minorHover() {
    this.y += this.dy;
    if (this.y > this.y_upperB) this.dy -= this.speed;
    if (this.y < this.y_lowerB) this.dy += this.speed;

    if (this.speechBubble) {
      draw_text(this.ctx, "I am a Commoner", this.x, this.y - 150);
    }

    this.draw();
  }
}

class R_influencer extends Agent {
  constructor(ctx, ID, type, opinion, connections, x, y, size, rotation,speechBubble) {
    super(ctx, ID, type, opinion, connections, x, y, size, rotation,speechBubble);

    this.y_upperB = y - 15;
    this.y_lowerB = y + 15;
    this.speed = 0.29;
    this.dy = this.speed;
  }

  draw() {
    //To be deleted
    this.ctx.fillStyle = "lightgreen";
    this.ctx.fillRect(
      this.x - this.size / 2,
      this.y - this.size / 2,
      this.size,
      this.size
    );

    drawImageRot(
      this.ctx,
      rinfluencer_img_face1,
      this.x,
      this.y,
      this.size,
      this.size,
      this.rotation
    );
  }

  minorHover() {
    this.y += this.dy;
    if (this.y > this.y_upperB) this.dy -= this.speed;
    if (this.y < this.y_lowerB) this.dy += this.speed;

    if (this.speechBubble) {
      draw_text(this.ctx, "I am an Influencer", this.x, this.y - 150);
    }

    this.draw();
  }
}

class F_influencer extends Agent {
  constructor(ctx, ID, type, opinion, connections, x, y, size, rotation,speechBubble) {
    super(ctx, ID, type, opinion, connections, x, y, size, rotation,speechBubble);

    this.y_upperB = y - 15;
    this.y_lowerB = y + 15;
    this.speed = 0.31;
    this.dy = this.speed;
  }

  draw() {
    //To be deleted
    this.ctx.fillStyle = "lightgreen";
    this.ctx.fillRect(
      this.x - this.size / 2,
      this.y - this.size / 2,
      this.size,
      this.size
    );
    drawImageRot(
      this.ctx,
      finfluencer_img_face1,
      this.x,
      this.y,
      this.size,
      this.size,
      this.rotation
    );
  }

  minorHover() {
    this.y += this.dy;
    if (this.y > this.y_upperB) this.dy -= this.speed;
    if (this.y < this.y_lowerB) this.dy += this.speed;

    if (this.speechBubble) {
      draw_text(this.ctx, "I am an Influencer", this.x, this.y - 150);
    }

    this.draw();
  }
}

export { Commoner, R_influencer, F_influencer };
