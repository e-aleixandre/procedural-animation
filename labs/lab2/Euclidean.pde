class Euclidean implements Heuristic {
    float calculate(Cell a, Cell b)
    {
        return sqrt(pow(a.col - b.col, 2) + pow(a.row - b.row, 2));
    }
}