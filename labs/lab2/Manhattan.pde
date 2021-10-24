class Manhattan implements Heuristic {
    float calculate(Cell a, Cell b)
    {
        return abs(a.col - b.col) + abs(a.row - b.row);
    }
}