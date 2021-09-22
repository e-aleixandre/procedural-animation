Vehicle a;

void setup() {
    size(512, 512);
    a = new Vehicle(width / 2, height / 2);
}

void update() {
    a.seek(new PVector(mouseX, mouseY));
    a.update();
}

void draw() {
    background(50, 50, 50);
    update();
    a.display();
}