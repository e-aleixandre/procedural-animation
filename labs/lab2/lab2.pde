import java.util.*;
int cols = 25, rows = 25, cellsize = 20, timeBetweenSpawn = 600, numtests, maxCols, maxRows, increment;
int lastSpawn = 0;
Grid grid;
Algorithm algo;
Heuristic heuristic;
ArrayList<Boid> boids;
PrintWriter output;

// Fixing problems with processing handling dragging
boolean holdingLeft = false, holdingRight = false,
        movingStart = false, movingGoal = false,
        fast = false, debug = false, play = false;

void settings() {
    size(cols * cellsize, rows * cellsize);
}

void setup() {
    mainSetup();
    //testSetup();
}

void mainSetup() {
    grid = new Grid(cols, rows, cellsize, false);
    heuristic = new Chebyshev();
    algo = new WAstar();
    algo.setHeuristic(heuristic);
    grid.setAlgorithm(algo);
    grid.allowDiagonal(false);
    
    boids = new ArrayList<Boid>();
}

void testSetup() {
    cols = 10;
    rows = 10;
    output = createWriter("results.txt");
    numtests = 1000;
    maxCols = 200;
    maxRows = 200;
    increment = 10;
    heuristic = new Chebyshev();
    algo = new Astar();
    algo.setHeuristic(heuristic);
}

void draw() {
    mainDraw();
    //testDraw();
}

void testDraw() {
    int currentTime;
    int accumulatedTime = 0;
    grid = new Grid(cols, rows, cellsize, false);
    grid.setAlgorithm(algo);
    System.out.format("Testing with a %dx%d grid\n", cols, rows);
    for (int i = 0; i < numtests; ++i)
    {
        currentTime = millis();
        
        grid.solvePath();
        
        accumulatedTime += millis() - currentTime;
        grid.restart();
    }

    accumulatedTime /= numtests;
    output.println(cols + "\t" + accumulatedTime);

    cols += increment;
    rows += increment;

    if (cols > maxCols || rows > maxRows)
    {
        output.flush();
        output.close();
        exit();
    }
}

void mainDraw() {
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