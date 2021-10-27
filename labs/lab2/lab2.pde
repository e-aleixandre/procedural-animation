final int cols = 20, rows = 20, cellsize = 20;
Grid grid;
Dijkstra dijkstra;
Astar astar;
Heuristic heuristic;

// Fixing problems with processing handling dragging
boolean holdingLeft = false, holdingRight = false,
        movingStart = false, movingGoal = false,
        iterate = false;

void settings() {
    size(cols * cellsize, rows * cellsize);
}

void setup() {
    grid = new Grid(cols, rows, cellsize);
    heuristic = new Euclidean();
    astar = new Astar();
    astar.setHeuristic(heuristic);
    grid.setAlgorithm(astar);
    grid.allowDiagonal(true);
}

void draw() {
    update();

    background(220);
    
    if (iterate)
        grid.iterate();
    
    grid.draw();
    grid.drawPath();
}

void update() {
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
    {
        iterate = !iterate;
    }
}