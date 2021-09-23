class Vehicle {
    final static int arriveDistance = 100;
    final static float maxWanderVariation = PI / 8;
    PVector location;
    PVector velocity;
    PVector acceleration;
    float maxspeed;
    float maxforce;
    float radius;
    float wanderAngle;
    int fleeDistance;

    Vehicle(float x, float y) {
        acceleration = new PVector(0, 0);
        velocity = new PVector(0, 0);
        location = new PVector(x, y);
        radius = 5.0f;

        maxspeed = 4.0f;
        maxforce = 0.1f;

        wanderAngle = .0f;
        fleeDistance = 100;
    }

    void update() {
        velocity.add(acceleration);
        velocity.limit(maxspeed);
        location.add(velocity);
        acceleration.set(0, 0);
    }

    PVector seek(PVector target)
    {
        PVector desiredVelocity = PVector.sub(target, location);
        desiredVelocity.setMag(maxspeed);

        PVector steer = PVector.sub(desiredVelocity, velocity);

        steer.limit(maxforce);

        return steer;
    }

    PVector arrive(PVector target)
    {
        PVector desiredVelocity = PVector.sub(target, location);

        float distanceToTarget = desiredVelocity.mag();

        // Adjusting desiredVelocity magnitude depending on target distance
        float velocityMagnitude = distanceToTarget < arriveDistance ? distanceToTarget * maxspeed / arriveDistance : maxspeed;
        desiredVelocity.setMag(velocityMagnitude);

        PVector steer = PVector.sub(desiredVelocity, velocity);
        steer.limit(maxforce);

        return steer;
    }

    // Exercise 6.1 - Implement a "fleeing" steering behaviour
    PVector flee(PVector target)
    {
        PVector desiredVelocity = PVector.sub(location, target);
        desiredVelocity.setMag(maxspeed);
        
        PVector steer = PVector.sub(desiredVelocity, velocity);

        steer.limit(maxforce);
        return steer;
    }

    /**
    * Just to illustrate the difference between steering behaviours and "straight following"
     */
    void towards(PVector target)
    {
        PVector desiredVelocity = PVector.sub(target, location);
        desiredVelocity.setMag(maxspeed);

        velocity = desiredVelocity;
    }

    PVector fleeAndWander(PVector target, boolean draw)
    {
        PVector fleeVelocity = PVector.sub(location, target);

        if (fleeVelocity.mag() < fleeDistance)
            return flee(target);
        else
            return wander(draw);
    }

    PVector pursue(Vehicle target)
    {
        PVector prediction = target.location.copy();
        // How many frames ahead? 20 (1/3 secs) seems a reasonable number
        prediction.add(PVector.mult(target.velocity, 20));

        return seek(prediction);
    }

    void evade(Vehicle target)
    {
    }

    PVector follow(FlowField ff)
    {
        PVector desired = ff.lookup(location);
        desired.mult(maxspeed);  // FlowField.lookup always returns a normalized vector

        PVector steer = PVector.sub(desired, velocity);
        steer.limit(maxforce);

        return steer;
    }

    PVector wander(boolean draw)
    {
        // 1. Determine a circle that will contain the target
        // 2. Get a random angle variation and add it to the current angle
        // 3. Find the point in the circumference at that angle
        // 4. Call seek with that point as argument (?)

        // Step 1
        // Circle is at vehicle location + normalized velocity direction * circleDistance
        int radius = 25;
        int circleDistance = 75;
        PVector circleCenter = PVector.add(location, velocity.copy().setMag(circleDistance));

        // Step 2
        wanderAngle += random(-maxWanderVariation, maxWanderVariation);

        // Step 3
        // Polar coordinates
        // x = r * cos(angle)
        // y = r * sin(angle)
        PVector circlePoint = new PVector(circleCenter.x + radius * cos(wanderAngle), circleCenter.y + radius * sin(wanderAngle));
        
        // This is kind of an anti-pattern, drawing in the update function
        if (draw)
        {
            noFill();
            stroke(255, 255, 255);
            circle(circleCenter.x, circleCenter.y, radius * 2);
            line(circleCenter.x, circleCenter.y, location.x, location.y);
            line(circleCenter.x, circleCenter.y, circlePoint.x, circlePoint.y);
            fill(255, 255, 255);
            circle(circlePoint.x, circlePoint.y, 5);
        }

        // Step 4
        return seek(circlePoint);
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
            vertex(-radius, radius * 2);
            vertex(radius, radius * 2);
            endShape();
        }
        popMatrix();
    }
}