let font;
let boids = [];
let players = [];
let fruitManager;

const numPlayers = 3;

function preload() {
  font = loadFont('assets/Inconsolata.otf');
}

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
  
  for (let i = 0; i < numPlayers; ++i)
  {
    const playerPosition = createVector(random(0, width), random(0, height));
    const playerColor = color(random(0, 255), random(0, 255), random(0,255));
    const player = new Player(playerPosition.x, playerPosition.y, playerColor);
}

function draw() {
  background(255);
  
  fruitManager.update();
  fruitManager.display();
  
  const mousePosition = createVector(mouseX, mouseY);
  
  
  // Player behaviour (if fruit seek, else wander)
  for (let i = 0; i < players.length; ++i)
  {
    let playerSteer;
    
    if (fruitManager.hasFruit)
    {
      playerSteer = player.seek(fruitManger.fruitLocation);
      if (fruitManager.consume(player.location))
      {
        player.addPoint();
      }
    } else {
      playerSteer = player.wander();
    }
    
    player.applyForce(playerSteer);
    player.update();
    player.display();
  }
  
  // Boids behaviour
  for (let i = 0; i < boids.length; ++i)
  {
    const boid = boids[i];
    const steer = boid.fleeOrArrive(vehicle.location, 100);
    boid.applyForce(steer);
    boid.update();
    boid.display();
  }
}
