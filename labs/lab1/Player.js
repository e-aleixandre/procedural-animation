class Player extends Vehicle {
  
  constructor(x, y, playerColor) {
    super(x, y);
    this.color = playerColor;
    this.points = 0;
  }
  
  // Same as Vehicle but uses color property
  display() {
    const theta = this.velocity.heading() + window.PI / 2;
    
    fill(this.color);
    stroke(0);
    push();
    {
      translate(this.location.x, this.location.y);
      rotate(theta);
      beginShape();
      vertex(0, -this.radius * 2);
      vertex(-this.radius, this.radius * 2);
      vertex(this.radius, this.radius * 2);
      endShape();
    }
    pop();
  }
  
  addPoint() {
    ++this.points;
  }
}
