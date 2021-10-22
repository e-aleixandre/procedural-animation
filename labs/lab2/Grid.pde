class Grid {
    Cell cells[][];
    Cell start;
    Cell goal;
    private int cols;
    private int rows;
    private int cellsize;

    Grid(int cols, int rows, int cellsize) {
        this.cols = cols;
        this.rows = rows;
        this.cellsize = cellsize;

        this.cells = new Cell[cols][rows];

        for (int i = 0; i < cols; ++i)
            for (int j = 0; j < rows; ++j)
                cells[i][j] = new Cell(i * cellsize, j * cellsize);
        
        start = cells[0][0];
        goal = cells[cols - 1][rows - 1];
    }

    void draw() {
        strokeWeight(1);

        for (Cell[] row : this.cells)
        {
            for (Cell cell : row)
            {
                // Is it an obstacle? Paint it black
                //cell.isObstacle() ? fill(0) : noFill();
                if (cell.isObstacle())
                    fill(0);
                else
                    noFill();

                square(cell.x, cell.y, cellsize);
            }
        }

        // Simpler solution: draw start and goal after the loop
        fill(51, 51, 180);
        square(start.x, start.y, cellsize);
        fill(51, 180, 51);
        square(goal.x, goal.y, cellsize);
    }

    public void handleLeftClick(int mouseX, int mouseY) {
        Cell cell = getCellFromPosition(mouseX, mouseY);

        // Prevent obstructing goal/start
        if (cell != null && cell != this.start && cell != this.goal)
            cell.obstacle = true;
    }

    public void handleRightClick(int mouseX, int mouseY) {
        Cell cell = getCellFromPosition(mouseX, mouseY);

        if (cell != null)
            cell.obstacle = false;
    }

    public boolean isStart(int mouseX, int mouseY) {
        Cell cell = getCellFromPosition(mouseX, mouseY);

        return cell != null && this.start == cell;
    }

    public void moveStart(int mouseX, int mouseY) {
        Cell cell = getCellFromPosition(mouseX, mouseY);

        if (cell == null || cell.isObstacle())
            return;

        cell.obstacle = false;
        this.start = cell;
    }

    public boolean isGoal(int mouseX, int mouseY) {
        Cell cell = getCellFromPosition(mouseX, mouseY);

        return cell != null && this.goal == cell;
    }

    public void moveGoal(int mouseX, int mouseY) {
        Cell cell = getCellFromPosition(mouseX, mouseY);

        if (cell == null || cell.isObstacle())
            return;

        cell.obstacle = false;
        this.goal = cell;
    }

    Cell getCellFromPosition(int mouseX, int mouseY) {
        int col = mouseX / cellsize;
        int row = mouseY / cellsize;

        if (!isValid(col, row))
            return null;
        
        return this.cells[col][row];
    }

    boolean isValid(int column, int row) {
        return column >= 0 && row >= 0 && column < this.cols && row < this.rows;
    }
}