let grid;
let movingStart = false;
let movingGoal = false;

function setup() {
  createCanvas(400, 400);
  grid = new Grid(20, 20, 20);
}

function draw() {
  if (mouseIsPressed)
  {
    if (movingStart)
    {
      grid.setStart(mouseX, mouseY);
    } 
    else if (movingGoal)
    {
      grid.setGoal(mouseX, mouseY);
    } else {
      grid.handleClick(mouseX, mouseY, mouseButton === LEFT);
    }
  }

  background(220);
  grid.draw();
}

function mousePressed()
{
   // TODO: Change Grid.isGoal and isStart to take a cell, so I can first get the cell, check it exists and then check if it's start / goal
   if (!movingStart && grid.isStart(mouseX, mouseY))
   {
     movingStart = true;
   }
   else if (!movingGoal && grid.isGoal(mouseX, mouseY))
   {
     movingGoal = true;
   }
}

function mouseReleased()
{
  movingGoal = movingStart = false;
}