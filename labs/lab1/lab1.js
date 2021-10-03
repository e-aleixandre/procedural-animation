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
  
  spawnBoidsFromCircle(points, 250);

  fruitManager = new FruitManager();
  
  for (let i = 0; i < numPlayers; ++i)
  {
    addPlayer();
  }

  setupUI();
}

function draw() {
  background(255);
  
  fruitManager.update();
  fruitManager.display();  
  
  // Player behaviour (if fruit seek, else wander)
  for (let i = 0; i < players.length; ++i)
  {
    let playerSteer;
    const player = players[i];

    if (fruitManager.hasFruit)
    {
      playerSteer = player.seek(fruitManager.fruitLocation);
      if (fruitManager.consume(player.location))
      {
        player.addPoint();
      }
    } else {
      playerSteer = player.wander();
    }
    stroke(0);
    strokeWeight(1);
    fill(player.color);
    textSize(24);
    text("Player " + i + " points: " + player.points, 20, height - 20 * (i + 1));
    player.applyForce(playerSteer);
    player.update();
    player.display();
  }
  
  // Boids behaviour
  for (let i = 0; i < boids.length; ++i)
  {
    const boid = boids[i];
    const closestPlayer = getClosestPlayer(boid, players);
    const steer = boid.fleeOrArrive(closestPlayer.location, 100);
    boid.applyForce(steer);
    boid.update();
    boid.display();
  }
}

function getClosestPlayer(boid, players) {

  let closestPlayer = players[0];
  let closestDistance = p5.Vector.sub(boid.location, closestPlayer.location).mag();


  for (let i = 1; i < players.length; ++i)
  {
    const distance = p5.Vector.sub(boid.location, players[i].location).mag();

    if (distance < closestDistance)
    {
      closestPlayer = players[i];
      closestDistance = distance;
    }
  }

  return closestPlayer;
}

function setupUI() {
  const addPlayerButton = createButton("Add player");
  addPlayerButton.mousePressed(addPlayer);
}

function minTimeBetweenFruitsChanged() {
  event.target.value
}

function addPlayer() {
  const playerPosition = createVector(random(0, width), random(0, height));
  const playerColor = color(random(0, 255), random(0, 255), random(0,255));
  const player = new Player(playerPosition.x, playerPosition.y, playerColor);
  players.push(player);
}

function spawnBoidsFromCircle(points, radius) {
  const delta = 2 * window.PI / points.length;
  const center = createVector(width / 2, height / 2);

  for (let i = 0; i < points.length; ++i)
  {
    const objective = createVector(points[i].x, points[i].y);
    const location = createVector(center.x + radius * cos(delta * i) , center.y + radius * sin(delta * i));
    const boid = new Boid(location.x, location.y, objective);
    boids.push(boid);
  }
}

function spawnBoidsFromCenter(points) {
  for (let i = 0; i < points.length; ++i)
  {
    const objective = createVector(points[i].x, points[i].y);
    const location = createVector(width / 2, height / 2);
    const boid = new Boid(location.x, location.y, objective);
    boids.push(boid);
  }
}

function spawnBoidsRandomly(points) {
  for (let i = 0; i < points.length; ++i)
  {
    const objective = createVector(points[i].x, points[i].y);
    const location = createVector(random(0, width), random(0, height));
    const boid = new Boid(location.x, location.y, objective);
    boids.push(boid);
  }
}

function spawnBoidsFromSide(points, offset) {
  for (let i = 0; i < points.length; ++i)
  {
    const objective = createVector(points[i].x, points[i].y);
    //const location = createVector(random(0, width), random(0, height));
    const location = createVector(objective.x + offset, objective.y);
    const boid = new Boid(location.x, location.y, objective);
    boids.push(boid);
  }
}

function createPulse() {
  const mousePosition = createVector(mouseX, mouseY);
  const pulseStrength = 50000;

  for (let i = 0; i < boids.length; ++i)
  {
    // This is the direction of the force, but also the distance (its magnitude)
    const forceVector = p5.Vector.sub(boids[i].location, mousePosition);

    // So the pulseStrength / the distance^2 is an inverse relationship depending on the distance
    forceVector.setMag(pulseStrength / forceVector.magSq());

    boids[i].applyForce(forceVector);
  }
}

function mousePressed() {
  createPulse();
}