class Chebyshev implements Heuristic {
    float calculate(Cell a, Cell b) {
        return max(abs(b.col - a.col), abs(b.row - a.row));
    }
}