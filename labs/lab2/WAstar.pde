/**
* A* algorithm
**/
import java.text.DecimalFormat;
import java.math.RoundingMode;

class WAstar implements Algorithm {
    Grid grid;
    PriorityQueue<Cell> pending;
    HashSet<Cell> computed;
    HashMap<Cell, Float> gScore;
    HashMap<Cell, Float> fScore;
    HashMap<Cell, Cell> cameFrom;
    Heuristic heuristic;
    boolean solved;
    Cell lastChecked;
    DecimalFormat df;

    void setup(Grid grid)
    {
        this.grid = grid;
        this.solved = false;
        this.computed = new HashSet<Cell>();
        this.cameFrom = new HashMap<Cell, Cell>();

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

        df = new DecimalFormat("#.##");
        df.setRoundingMode(RoundingMode.DOWN);
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

            float tentative_gScore = gScore.get(current) + heuristic.calculate(current, neighbour);

            if (tentative_gScore < gScore.get(neighbour))
            {
                cameFrom.put(neighbour, current);
                gScore.put(neighbour, tentative_gScore);

                fScore.put(neighbour, tentative_gScore + neighbour.weight * heuristic.calculate(neighbour, this.grid.getGoal()));

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

        path.add(grid.getStart());

        return path;
    }

    void restart()
    {
        // Restart gScore / fScore
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

        // Increment weight of current path cells, if solved
        if (this.solved)
        {
            ArrayList<Cell> path = getPath();

            for (Cell cell : path)
            {
                cell.weight *= 1.25;
            }
        } else {
            // if not completed, clear the pending set
            pending.clear();
        }

        // Add start node on top of pending
        pending.add(grid.getStart());

        // Clear other maps/sets
        cameFrom.clear();
        computed.clear();
        cameFrom.clear();

        // Set as not solved
        solved = false;
    }

    /**
    * For this algo, relevant info is gScore, fScore and maybe Heuristic
    **/
    void info(Cell cell)
    {
        textAlign(CENTER, CENTER);
        text(this.heuristic.calculate(cell, this.grid.getGoal()), cell.center.x, cell.center.y - 20);
        if (this.gScore.get(cell) == Float.MAX_VALUE)
            text("inf", cell.center.x, cell.center.y - 10);
        else
            text(this.gScore.get(cell), cell.center.x, cell.center.y - 10);

        if (this.fScore.get(cell) == Float.MAX_VALUE)
            text("inf", cell.center.x, cell.center.y);
        else
            text(this.fScore.get(cell), cell.center.x, cell.center.y);
    }
}
