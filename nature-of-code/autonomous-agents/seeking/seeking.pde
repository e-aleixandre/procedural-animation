Vehicle a;
FlowField ff;

void setup() {
    size(512, 512);
    a = new Vehicle(width / 2, height / 2);
    ff = new FlowField(FlowType.PERLIN, 50);
}

void update() {
    a.follow(ff);
    a.update();
}

void draw() {
    background(50, 50, 50);
    update();
    ff.draw();
    a.display();
    
}