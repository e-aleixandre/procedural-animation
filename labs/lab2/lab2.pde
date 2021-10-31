final int cols = 5, rows = 5, cellsize = 25, timeBetweenSpawn = 600;
int lastSpawn = 0;
Grid grid;
Algorithm algo;
Heuristic heuristic;
ArrayList<Boid> boids;

// Fixing problems with processing handling dragging
boolean holdingLeft = false, holdingRight = false,
        movingStart = false, movingGoal = false,
        fast = false, debug = false, play = false;

void settings() {
    size(cols * cellsize, rows * cellsize);
}

void setup() {
    grid = new Grid(cols, rows, cellsize, false);
    heuristic = new Euclidean();
    algo = new WAstar();
    algo.setHeuristic(heuristic);
    grid.setAlgorithm(algo);
    grid.allowDiagonal(true);
    
    boids = new ArrayList<Boid>();
}

void draw() {
    // Filling the background
    background(220);
    
    // Drawing the grid and the current path
    grid.draw(debug);
    grid.drawPath();

    // Fast solving
    if (fast)
    {
        grid.iterate();
        if (grid.isSolved())
            fast = false;
    }

    if (play)
    {
        if (millis() - lastSpawn > timeBetweenSpawn)
        {
            grid.solvePath();
            boids.add(new Boid(grid.getPath()));
            grid.restart();
            lastSpawn = millis();
        }
    }

    // Update boids
    // Using a ListIterator to remove elements while iterating
    ListIterator<Boid> iterator = boids.listIterator();

    while (iterator.hasNext())
    {
        Boid boid = iterator.next();

        // if it's dead, remove it
        if (boid.isDead())
        {
            iterator.remove();
            continue;
        }

        // Else, follow the path and draw the boid
        boid.followPath();
        boid.update();
        boid.draw();
    }

    // Handle mouse clicks
    if (mousePressed)
    {
        if (mouseButton == LEFT)
        {
            grid.handleLeftClick(mouseX, mouseY);
        } else if(mouseButton == RIGHT) {
            grid.handleRightClick(mouseX, mouseY);
        }
    }
}

void mousePressed() {
    if (mouseButton == LEFT)
    {
        // Could improve this grabbing the cell once and comparing it
        if (grid.isGoal(mouseX, mouseY))
        {
            movingGoal = true;
        } else if (grid.isStart(mouseX, mouseY)) {
            movingStart = true;
        } else {
            holdingLeft = true;
            grid.handleLeftClick(mouseX, mouseY);   
        }
    } 
    else if (mouseButton == RIGHT)
    {
        holdingRight = true;
        grid.handleRightClick(mouseX, mouseY);
    }
        
}

void mouseReleased() {
    if (mouseButton == LEFT)
    {
        movingGoal = false;
        holdingLeft = false;
        movingStart = false;
    }
    else if (mouseButton == RIGHT)
        holdingRight = false;
}

void mouseDragged() {
    if (holdingLeft)
        grid.handleLeftClick(mouseX, mouseY);
    else if(holdingRight)
        grid.handleRightClick(mouseX, mouseY);
    else if(movingGoal)
        grid.moveGoal(mouseX, mouseY);
    else if(movingStart)
        grid.moveStart(mouseX, mouseY);
}

void keyPressed() {
    if (key == 'i')
        grid.iterate();
    else if (key == 'd')
        debug = !debug;
    else if (key == 'f')
        fast = !fast;
    else if (key == 'r')
        grid.restart();
    else if (key == ' ')
    {
        grid.solvePath();
        boids.add(new Boid(grid.getPath()));   
    } else if (key == 'p')
        play = !play;
}