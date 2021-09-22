class Vehicle {
    PVector location;
    PVector velocity;
    PVector acceleration;
    float maxspeed;
    float maxforce;
    float radius;

    Vehicle(float x, float y) {
        acceleration = new PVector(0, 0);
        velocity = new PVector(0, 0);
        location = new PVector(x, y);
        radius = 3.0f;

        maxspeed = 4.0f;
        maxforce = 0.1f;
    }

    void update() {
        velocity.add(acceleration);
        velocity.limit(maxspeed);
        location.add(velocity);
        acceleration.set(0, 0);
    }

    void seek(PVector target)
    {
        PVector desiredVelocity = PVector.sub(target, location);
        desiredVelocity.normalize();
        desiredVelocity.mult(maxspeed);

        PVector steer = PVector.sub(desiredVelocity, velocity);

        steer.limit(maxforce);

        applyForce(steer);
    }

    // Exercise 6.1 - Implement a "fleeing" steering behaviour
    void flee(PVector target)
    {
        PVector desiredVelocity = PVector.sub(location, target);
        desiredVelocity.normalize().mult(maxspeed);
        
        PVector steer = PVector.sub(desiredVelocity, velocity);

        steer.limit(maxforce);
        applyForce(steer);
    }

    void applyForce(PVector force)
    {
        acceleration.add(force);
    }

    void display()
    {
        float theta = velocity.heading() + PI / 2;

        fill(175);
        stroke(0);
        pushMatrix();
        {
            translate(location.x, location.y);
            rotate(theta);
            beginShape();
            vertex(0, -radius * 2);
            vertex(-radius, radius*2);
            vertex(radius, radius*2);
            endShape();
        }
        popMatrix();
    }
}