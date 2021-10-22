class Cell {
    int x;
    int y;
    boolean obstacle;
    float weight;

    Cell(int x, int y) {
        this(x, y, 1.0);
    }

    Cell(int x, int y, float weight)
    {
        this.x = x;
        this.y = y;
        this.weight = weight;
        this.obstacle = false;
    }

    public boolean isObstacle() {
        return obstacle;
    }
}