class Target extends Vehicle {
    Target(float x, float y) {
        super(x, y);
    }

    void display()
    {
        float theta = velocity.heading() + PI / 2;

        fill(204, 73, 73);
        stroke(0);
        pushMatrix();
        {
            translate(location.x, location.y);
            rotate(theta);
            circle(0, 0, 20);
        }
        popMatrix();
    }
}