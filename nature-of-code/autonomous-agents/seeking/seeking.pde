Vehicle a;
FlowField ff;

void setup() {
    size(512, 512);
    a = new Vehicle(width / 2, height / 2);
    ff = new FlowField(FlowType.CENTER);
}

void update() {
    a.arrive(new PVector(mouseX, mouseY));
    a.wander(true);
    a.update();
}

void draw() {
    background(50, 50, 50);
    update();
    ff.draw();
    a.display();
    
}