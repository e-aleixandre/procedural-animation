class Grid {

    constructor(cols, rows, cellsize) {
        this.cols = cols;
        this.rows = rows;
        this.cellsize = cellsize;
        
        this.grid = new Array(cols);
        
        for (let i = 0; i < cols; i++)
        {
            this.grid[i] = new Array(rows);
            
            for (let j = 0; j < rows; ++j)
                this.grid[i][j] = {obstacle: false, weight: 1};
        }

        this.start = [0, 0];
        this.goal = [cols - 1, rows - 1];
    }

    draw() {
        strokeWeight(2);
        stroke(0);

        for (let i = 0; i < this.cols; ++i)
        {
            for (let j = 0; j < this.rows; ++j)
            {
                const cell = this.grid[i][j];
                
                // Fill the cell if it's an obstacle
                cell.obstacle ? fill(0) : noFill();
                
                square(i * this.cellsize, j * this.cellsize, this.cellsize);
                text(cell.weight, i * this.cellsize + this.cellsize / 2, j * this.cellsize + this.cellsize / 2);
            }
        }

        // It's simpler to just draw start / goal again
        fill(180, 51, 51);
        square(this.start[0] * this.cellsize, this.start[1] * this.cellsize, this.cellsize);
        text(this.grid[this.start[0], this.start[1]].weight, this.start[0] * this.cellsize + this.cellsize / 2, this.start[1] * this.cellsize + this.cellsize / 2);

        fill(51, 180, 51);
        square(this.goal[0] * this.cellsize, this.goal[1] * this.cellsize, this.cellsize);
    }

    handleClick(mouseX, mouseY, obstacle) {
        let cell = this.mapPositionToCell(new p5.Vector(mouseX, mouseY));
        if (!cell || cell == this.start || cell == this.goal)
            return;
        
        this.grid[cell[0]][cell[1]].obstacle = obstacle;
    }

    handleLeftClick(mouseX, mouseY) {
        this.handleClick(mouseX, mouseY, true);
    }

    handleRightClick(mouseX, mouseY) {
        this.handleClick(mouseX, mouseY, false);
    }

    setStart(posX, posY) {
        let cell = this.mapPositionToCell(new p5.Vector(posX, posY));

        if (cell)
        {
            this.start = cell;

            // Ensure it's not an obstacle
            this.grid[cell[0], cell[1]].obstacle = false;
        }    

    }

    isStart(posX, posY) {
        let cell = this.mapPositionToCell(new p5.Vector(posX, posY));

        if (cell)
        {
            if (this.start[0] == cell[0] &&  this.start[1] == cell[1])
                return true
        }

        return false;
    }

    setGoal(posX, posY) {
        let cell = this.mapPositionToCell(new p5.Vector(posX, posY));

        if (cell && !this.isGoal())
        {
            this.goal = cell;

            // Ensure it's not an obstacle
            this.grid[cell[0], cell[1]].obstacle = false;
        }
    }

    isGoal(posX, posY) {
        let cell = this.mapPositionToCell(new p5.Vector(posX, posY));

        if (cell)
        {
            if (this.goal[0] == cell[0] &&  this.goal[1] == cell[1])
                return true
        }

        return false;
    }

    mapPositionToCell(position)
    {
        let col, row;
        
        col = floor(position.x / this.cellsize);
        row = floor(position.y / this.cellsize);

        if (col > this.cols - 1 || row > this.rows - 1)
            return null;

        return [col, row];
    }
}