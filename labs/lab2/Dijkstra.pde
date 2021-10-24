import java.util.*;

/**
* Dijkstra algorithm
**/
class Dijkstra /* implements Algorithm */ {
    //PriorityQueue<Cell> queue;
    HashMap<Cell, Float> distances = new HashMap<Cell, Float>();
    HashMap<Cell, Float> previous = new HashMap<Cell, Float>();
    Grid grid;

    void setup(Grid grid)
    {
        // Maybe we dont need a reference to the entire grid, consider this
        this.grid = grid;

        // Preallocating memory for the queue
        //this.queue = new PriorityQueue<Cell>(grid.getSize());

        for (Cell[] col : grid.cells)
        {
            for (Cell cell : col)
            {
                distances.put(cell, Float.MAX_VALUE);
                previous.put(cell, null);
            }
        }

        distances.put(grid.getStart(), 0.0);
        // Instead of adding an if in the foor loop, we add every cell and then remove the start
        //distances.remove(this.grid.getStart());
    }

    void iterate() {
        //if ()
    }

    boolean solved() {
        return false;
    }
}
