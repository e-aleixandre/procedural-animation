class Target extends Vehicle {
  
  constructor(x, y) {
    super(x, y);
  }
  
  display() {    
    fill(204, 73, 73);
    stroke(0);
    
    circle(this.location.x, this.location.y, 20);
  }
}
