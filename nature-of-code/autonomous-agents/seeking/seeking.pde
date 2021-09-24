Target a;
Target b;
Vehicle c;
FlowField ff;

void setup() {
    size(800, 800);
    
    a = new Target(random(0, width), random(0, height));
    b = new Target(random(0, width), random(0, height));
    c = new Vehicle(random(0, width), random(0, height));
    ff = new FlowField(FlowType.PERLIN, 300);
}

void update() {
    PVector mouse = new PVector(mouseX, mouseY);
    PVector steerA = a.wander(false);
    PVector steerB = b.seek(a.location);
    PVector steerC = c.pursue(a);

    a.applyForce(steerA);
    b.applyForce(steerB);
    c.applyForce(steerC);

    a.avoidWalls(50);
    b.avoidWalls(50);
    c.avoidWalls(50);

    a.update();
    b.update();
    c.update();
}

void draw() {
    background(50, 50, 50);
    update();
    a.display();
    b.display();
    c.display();
}