final float MAX_WEIGHT = 5.0;
final float MIN_WEIGHT = 1.0;

class Grid {
    Cell cells[][];
    Cell start;
    Cell goal;
    Algorithm algorithm;
    private int cols;
    private int rows;
    private int cellsize;
    boolean diagonalMovement = false;

    Grid(int cols, int rows, int cellsize, boolean randomWeights) {
        this.cols = cols;
        this.rows = rows;
        this.cellsize = cellsize;

        this.cells = new Cell[cols][rows];

        if (randomWeights)
            for (int i = 0; i < cols; ++i)
                for (int j = 0; j < rows; ++j)
                {
                    float weight = random(MIN_WEIGHT, MAX_WEIGHT);
                    cells[i][j] = new Cell(i, j, cellsize, weight);
                }
        else
            for (int i = 0; i < cols; ++i)
                for (int j = 0; j < rows; ++j)
                    cells[i][j] = new Cell(i, j, cellsize);
        
        start = cells[0][0];
        goal = cells[cols - 1][rows - 1];
    }

    void draw(boolean info) {
        color computed = color(172, 172, 242);

        for (Cell[] col : this.cells)
        {
            for (Cell cell : col)
            {
                if (algorithm.isComputed(cell))
                {
                    cell.draw(this.cellsize, computed);
                }
                else
                {
                    color weightColor = color(122, 24, 24, map(cell.weight, MIN_WEIGHT, MAX_WEIGHT, 0, 180));
                    cell.draw(this.cellsize, weightColor);
                }

                if (info)
                {
                    fill(0);
                    algorithm.info(cell);
                }
            }
        }

        // Simplest solution: draw start and goal after the loop
        start.draw(this.cellsize, color(51, 51, 180));
        goal.draw(this.cellsize, color(51, 180, 51));
    }

    public void handleLeftClick(int mouseX, int mouseY) {
        Cell cell = getCellFromPosition(mouseX, mouseY);

        // Prevent obstructing goal/start, which might not be necessary
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

    public boolean isStart(Cell cell) {
        return cell == this.start;
    }

    public void moveStart(int mouseX, int mouseY) {
        Cell cell = getCellFromPosition(mouseX, mouseY);

        if (cell == null || cell.isObstacle() || this.isGoal(cell))
            return;

        cell.obstacle = false;

        // Re-setup the algorithm, this could actually be improved
        // i.e.: In A*, we could just remove start form gScore, fScore and pending, and add it again. No need to process all cells again.
        this.algorithm.setup(this);

        this.start = cell;
    }

    public boolean isGoal(int mouseX, int mouseY) {
        Cell cell = getCellFromPosition(mouseX, mouseY);

        return cell != null && this.goal == cell;
    }

    public boolean isGoal(Cell cell) {
        return cell == this.goal;
    }

    public void moveGoal(int mouseX, int mouseY) {
        Cell cell = getCellFromPosition(mouseX, mouseY);

        if (cell == null || cell.isObstacle() || this.isStart(cell))
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

    void setAlgorithm(Algorithm algo)
    {
        this.algorithm = algo;
        this.algorithm.setup(this);
    }

    void iterate()
    {
        if (this.algorithm == null)
            return;

        if (!this.algorithm.isSolved())
            this.algorithm.iterate();
    }

    Cell getStart() {
        return this.start;
    }

    Cell getGoal() {
        return this.goal;
    }

    int getSize() {
        return this.cols * this.rows;
    }

    ArrayList<Cell> getNeighbours(int col, int row) {
        ArrayList<Cell> neighbours = new ArrayList<Cell>();

        if (row > 0 && !cells[col][row - 1].isObstacle()) {
            neighbours.add(cells[col][row - 1]);
        }

        if (row < this.rows - 1 && !cells[col][row + 1].isObstacle()) {
            neighbours.add(cells[col][row + 1]);
        }

        if (col > 0 && !cells[col - 1][row].isObstacle()) {
            neighbours.add(cells[col - 1][row]);
        }

        if (col < this.cols - 1 && !cells[col + 1][row].isObstacle()) {
            neighbours.add(cells[col + 1][row]);
        }

        if (diagonalMovement)
        {
            if (col - 1 > 0 && row - 1 > 0 && !cells[col - 1][row - 1].isObstacle())
                neighbours.add(cells[col - 1][row - 1]);

            if (col + 1 < this.cols && row - 1 > 0 && !cells[col + 1][row - 1].isObstacle())
                neighbours.add(cells[col + 1][row - 1]);

            if (col - 1 > 0 && row + 1 < this.rows && !cells[col - 1][row + 1].isObstacle())
                neighbours.add(cells[col - 1][row + 1]);

            if (col + 1 < this.cols && row + 1 < this.rows && !cells[col + 1][row + 1].isObstacle())
                neighbours.add(cells[col + 1][row + 1]);       
        }

        return neighbours;
    }

    ArrayList<Cell> getNeighbours(Cell cell) {
        return getNeighbours(cell.col, cell.row);
    }

    void drawPath() {
        ArrayList<Cell> path = this.algorithm.getPath();

        fill(0, 0, 255);
        strokeWeight(4);

        for (int i = 0; i < path.size() - 2; ++i)
        {
            // Ugly code
            line(path.get(i).col * cellsize + cellsize/2, path.get(i).row * cellsize + cellsize/2, path.get(i + 1).col * cellsize + cellsize/2, path.get(i + 1).row * cellsize + cellsize/2);
        }
    }

    void solvePath() {
        while (!algorithm.isSolved())
        {
            algorithm.iterate();
        }
    }

    boolean isSolved() {
        return algorithm.isSolved();
    }

    ArrayList<Cell> getPath() {
        return algorithm.getPath();
    }

    void restart() {
        algorithm.restart();
    }

    void allowDiagonal(boolean allow)
    {
        this.diagonalMovement = allow;
    }
}