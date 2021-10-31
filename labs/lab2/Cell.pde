class Cell {
    int col;
    int row;
    boolean obstacle;
    float weight;
    // Precalculating center
    PVector center;

    Cell(int col, int row, int cellsize) {
        this(col, row, cellsize, 1.0);
    }

    Cell(int col, int row, int cellsize, float weight)
    {
        this.col = col;
        this.row = row;
        this.weight = weight;
        this.obstacle = false;
        this.center = new PVector(col * cellsize + cellsize / 2, row * cellsize + cellsize / 2);
    }

    void draw(int cellSize, color cellColor)
    {
        strokeWeight(1);
        
        if (obstacle)
            fill(0);
        else
            fill(cellColor);

        square(col * cellSize, row * cellSize, cellSize);
    }

    void draw(int cellSize)
    {
        draw(cellSize, color(255));
    }

    public boolean isObstacle() {
        return obstacle;
    }
}