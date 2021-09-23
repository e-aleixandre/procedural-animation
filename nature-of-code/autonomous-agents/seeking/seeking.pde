Vehicle a;
Vehicle b;
FlowField ff;

void setup() {
    size(1080, 1080);
    a = new Vehicle(width / 2, height / 2);
    b = new Vehicle(width / 2, height / 2);
    ff = new FlowField(FlowType.PERLIN);
}

void update() {
    PVector mouse = new PVector(mouseX, mouseY);
    a.follow(ff);
    a.update();
}

void draw() {
    background(50, 50, 50);
    update();
    ff.draw();
    a.display();
}