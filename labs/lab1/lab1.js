let font;
let boids = [];
let grid;
let cols;
let rows;
let players = [];
let fruitManager;

const options = {
  objective: true,
  objectiveMultiplier: 1.0,
  separate: false,
  separateMultiplier: 1.0,
  cohesion: false,
  cohesionMultiplier: 1.0,
  align: false,
  alignMultiplier: 1.0,
  flee: false,
  fleeMultiplier: 1.0
}

const numPlayers = 3;
const cellSize = 75;

function preload() {
  font = loadFont('assets/Inconsolata.otf');
}

function setup() {
  createCanvas(1280, 720);
  
  // Get letter points and create boids
  let points = font.textToPoints('Lab 1 - TPA', 100, 200, 200);
  
  //spawnBoidsFromCircle(points, 250);
  //spawnBoidsFromBottom(points);
  spawnBoidsRandomly(points);

  fruitManager = new FruitManager();
  
  for (let i = 0; i < numPlayers; ++i)
  {
    addPlayer();
  }

  setupUI();
  // Prepare the grid
  cols = int(width / cellSize) + 1;
  rows = int(height / cellSize) + 1;

  grid = new Array(cols);

  for (let i = 0; i < cols; ++i)
  {
    grid[i] = new Array(rows);
    for (let j = 0; j < rows; ++j)
    {
      grid[i][j] = [];
    }
  }
}

function draw() {
  background(255, 255, 255, 137);
  
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
  
  refreshGrid(boids);

  // Boids behaviour
  for (let i = 0; i < boids.length; ++i)
  {
    const boid = boids[i];

    const neighbours = getCurrentNeighbours(boid);
    
    const steer = createVector();

    if (options.objective) {
      steer.add(boid.arrive().mult(options.objectiveMultiplier));
    }

    if (options.separate) {
      steer.add(boid.separate(/* boids */neighbours, 50).mult(options.separateMultiplier));
    }

    if (options.cohesion) {
      steer.add(boid.cohesion(/* boids */neighbours, 50).mult(options.cohesionMultiplier));
    }

    if (options.align)  {
      steer.add(boid.align(/* boids */neighbours, 50).mult(options.alignMultiplier));
    }

    if (options.flee) {
      const closestPlayer = getClosestPlayer(boid, players);
      steer.add(boid.fleeIfClose(closestPlayer.location, 100).mult(options.fleeMultiplier));
    }

    boid.applyForce(steer);
    boid.update();
    boid.display();
  }

  fill(0);
  noStroke();
  text("(O)bjective: " + (options.objective ? "Enabled" : "Disabled"), width - 320, height - 100);
  text("(S)eparate: " + (options.separate ? "Enabled" : "Disabled"), width - 320, height - 80);
  text("(C)ohesion: " + (options.cohesion ? "Enabled" : "Disabled"), width - 320, height - 60);
  text("(A)lign: " + (options.align ? "Enabled" : "Disabled"), width - 320, height - 40);
  text("(F)lee: " + (options.flee ? "Enabled" : "Disabled"), width - 320, height - 20);
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

  const removePlayerButton = createButton("Remove player");
  removePlayerButton.mousePressed(removePlayer);

  // Hacky way to add the event listeners to each input
  const variables = ["objective", "separate", "cohesion", "align", "flee"];

  variables.forEach(function(variable) {

    const slider = document.getElementById(variable);

    document.getElementById(variable + "Value").innerText = options[variable + "Multiplier"];
    slider.value = options[variable + "Multiplier"];

    slider.addEventListener("input", function(event) {
      options[event.target.id + "Multiplier"] = parseFloat(event.target.value);

      const valueElement = event.target.parentElement.parentElement.querySelector("#" + event.target.id + "Value");
      valueElement.innerText = event.target.value;
    });
  });
}

function addPlayer() {
  const playerPosition = createVector(random(0, width), random(0, height));
  const playerColor = color(random(0, 255), random(0, 255), random(0,255));
  const player = new Player(playerPosition.x, playerPosition.y, playerColor);
  players.push(player);
}

function removePlayer() {
  players.pop();
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

function spawnBoidsFromBottom(points) {
  for (let i = 0; i < points.length; ++i)
  {
    const objective = createVector(points[i].x, points[i].y);
    const location = createVector(random(0, width), height);
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

function keyTyped() {
  switch(key) {
    case 'o':
    case 'O':
      options.objective = !options.objective;
      break;
    case 's':
    case 'S':
      options.separate = !options.separate;
      break;
    case 'c':
    case 'C':
      options.cohesion = !options.cohesion;
      break;
    case 'a':
    case 'A':
      options.align = !options.align;
      break;
    case 'f':
    case 'F':
      options.flee = !options.flee;
      break;
  }
}

function refreshGrid(boids) {
  // First clear the grid
  for (let i = 0; i < cols; ++i)
    for (let j = 0; j < rows; ++j)
      grid[i][j] = [];

  // Then put each boid on its cell
  for (let i = 0; i < boids.length; ++i)
  {
    let [currentCol, currentRow] = getCurrentGridPosition(boids[i]);

    grid[currentCol][currentRow].push(boids[i]);
  }
}

function getCurrentNeighbours(boid) {
  let [currentCol, currentRow] = getCurrentGridPosition(boid);
  return grid[currentCol][currentRow];
}

function getCurrentGridPosition(boid) {
  // Constraining to avoid negative or out of bounds indexes

  return [
    constrain(int(boid.location.x / cellSize), 0, cols - 1),
    constrain(int(boid.location.y / cellSize), 0, rows - 1)
  ]
}
