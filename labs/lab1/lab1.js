let font;
let boids = [];
let fruitManager;

function preload() {
  font = loadFont('assets/Inconsolata.otf');
}

let vehicle;
let target;

function setup() {
  createCanvas(1280, 720);
  
  // Get letter points and create boids
  let points = font.textToPoints('Lab 1 - TPA', 100, 200, 200);
  
  for (let i = 0; i < points.length; ++i)
  {
    const objective = createVector(points[i].x, points[i].y);
    const location = createVector(random(0, width), random(0, height));
    const boid = new Boid(location.x, location.y, objective);
    boids.push(boid);
  }
  
  fruitManager = new FruitManager();
}

function draw() {
  background(255);
  
  fruitManager.update();
  fruitManager.display();
  
  const mousePosition = createVector(mouseX, mouseY);
  
  for (let i = 0; i < boids.length; ++i)
  {
    const boid = boids[i];
    const steer = boid.fleeOrArrive(mousePosition, 100);
    boid.applyForce(steer);
    boid.update();
    boid.display();
  }
}
