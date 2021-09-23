Target a;
Vehicle b;
FlowField ff;

void setup() {
    size(1080, 1080);
    a = new Target(width / 4, height / 4);
    b = new Vehicle(width / 2, height / 2);
    ff = new FlowField(FlowType.PERLIN, 300);
}

void update() {
    PVector mouse = new PVector(mouseX, mouseY);
    PVector steer = a.seek(mouse);
    a.applyForce(steer);
    a.update();
    steer = b.pursue(a);
    b.applyForce(steer);
    b.update();
}

void draw() {
    background(50, 50, 50);
    update();
    a.display();
    b.display();
}