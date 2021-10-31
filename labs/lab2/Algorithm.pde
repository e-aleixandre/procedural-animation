/**
*  Interface that all algorithms must implement
**/
interface Algorithm {
    // Every algorithm receives the Grid so it can setup everything it needs
    void setup(Grid grid);

    // Iterate should perform one "round" of calculations
    void iterate();

    // Should return if the path is already calculated
    boolean isSolved();

    // Should set the heuristic used to calculate the fScore
    void setHeuristic(Heuristic heuristic);

    // Should return if the algorithm is completed
    boolean isComputed(Cell cell);

    // Should return computed path
    ArrayList<Cell> getPath();

    // For debuggin purposes, should draw info on screen relevant to the given cell
    void info(Cell cell);

    // Should re-setup the algorithm to calculate a new path
    void restart();
}
