// File for agent class

class Agent {
    constructor(ID, type, opinion, connections, x, y) {
        this.ID = ID;
        this.type = type;
        this.opinion = opinion;
        this.connections = connections;
        this.x = x;
        this.y = y;
    }

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

}
