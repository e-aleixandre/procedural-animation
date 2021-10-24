/**
* A* algorithm
**/

class Astar implements Algorithm {
    Grid grid;
    PriorityQueue<Cell> pending;
    HashSet<Cell> computed = new HashSet<Cell>();
    HashMap<Cell, Float> gScore;
    HashMap<Cell, Float> fScore;
    HashMap<Cell, Cell> cameFrom = new HashMap<Cell, Cell>();
    Heuristic heuristic;
    Boolean solved = false;
    Cell lastChecked;

    void setup(Grid grid)
    {
        this.grid = grid;

        // Using a custom comparator to order the PriorityQueue
        pending = new PriorityQueue<Cell>(new Comparator<Cell>() {
            @Override
            public int compare(Cell a, Cell b) {
                return fScore.get(a).compareTo(fScore.get(b));
            }
        });

        gScore = new HashMap<Cell, Float>(grid.getSize());
        fScore = new HashMap<Cell, Float>(grid.getSize());

        for (Cell[] col : grid.cells)
        {
            for (Cell cell : col)
            {
                gScore.put(cell, Float.MAX_VALUE);
                fScore.put(cell, Float.MAX_VALUE);
            }
        }

        gScore.put(grid.getStart(), 0.0);
        fScore.put(grid.getStart(), heuristic.calculate(grid.getStart(), grid.getGoal()));

        pending.add(grid.getStart());
    }

    void setHeuristic(Heuristic heuristic)
    {
        this.heuristic = heuristic;
    }

    void iterate()
    {
        if (pending.isEmpty() || this.solved)
            return;

        Cell current = pending.poll();

        this.lastChecked = current;

        if (current == grid.getGoal())
        {
            this.solved = true;
            return;
        }

        computed.add(current);
 
        for (Cell neighbour : this.grid.getNeighbours(current))
        {
            if (computed.contains(neighbour))
                continue;

            float tentative_gScore = gScore.get(current) + neighbour.weight;       

            if (tentative_gScore < gScore.get(neighbour))
            {
                cameFrom.put(neighbour, current);
                gScore.put(neighbour, tentative_gScore);
                fScore.put(neighbour, tentative_gScore + heuristic.calculate(neighbour, this.grid.getGoal()));

                if (!pending.contains(neighbour))
                    pending.add(neighbour);
            }
        }

    }

    boolean isSolved()
    {
        return this.solved;
    }

    boolean isComputed(Cell cell)
    {
        return this.computed.contains(cell);
    }

    ArrayList<Cell> getPath()
    {
        ArrayList<Cell> path = new ArrayList<Cell>();
        
        Cell cell = this.lastChecked;
        path.add(cell);
        
        while (cameFrom.containsKey(cell))
        {
            cell = cameFrom.get(cell);
            path.add(cell);
        }

        return path;
    }
}
