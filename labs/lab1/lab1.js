let font;
let boids = [];

function preload() {
  font = loadFont('assets/Inconsolata.otf');
}

let points;
let vehicle;
let target;

function setup() {
  createCanvas(1280, 720);
  points = font.textToPoints('Lab 1 - TPA', 100, 200, 200);
  stroke('purple');
  strokeWeight(4);
  
  vehicle = new Vehicle(100, 100);
  target = new Target(150, 150);
}

function draw() {
  background(255);
  
  const steer = vehicle.arrive(createVector(mouseX, mouseY));
  vehicle.applyForce(steer);
  vehicle.update();
  
  vehicle.display();
  
  const targetSteer = target.fleeAndWander(vehicle.location, true);
  target.applyForce(targetSteer);
  target.update();
  target.display();
  
  for (let i = 0; i < points.length; ++i)
  {
    point(points[i].x, points[i].y);
  }
}
