class Vehicle {
    PVector location;
    PVector velocity;
    PVector acceleration;
    float maxspeed;

    void seek(PVector target)
    {
        PVector desiredVelocity = PVector.sub(target, location);
        desired.normalize();
        desired.mult(maxspeed);

        PVector steer = PVector.sub(desired, velocity);
        applyForce(steer);
    }

    void applyForce(PVector force)
    {
        acceleration.add(force);
    }
}