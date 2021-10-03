class Boid extends Vehicle {
  
  constructor(x, y, objective) {
    // This is the position of the letter this boid occupies
    super(x, y);
    this.objective = objective;
  }
  
  /**
  * If we provide a target, the function is equal to the Vehicle.arrive function
  * If not, the Boid will seek/arrive its objective position
  **/
  arrive(target) {
    if (target)
    {
      return super.arrive(target);
    } else {
      return super.arrive(this.objective);
    }
  }
  
  fleeOrArrive(target, minDistance) {
    const distance = p5.Vector.sub(target, this.location);
    
    if (distance.mag() < minDistance)
    {
      return super.flee(target);
    } else {
      return this.arrive();
    }
  }

  fleeIfClose(target, minDistance) {
    const distance = p5.Vector.sub(target, this.location);

    if (distance.mag() < minDistance)
    {
      return super.flee(target);
    } else {
      return createVector();
    }
  }
  
  display() {    
    fill(0);
    stroke(0);
    strokeWeight(2);
    
    point(this.location.x, this.location.y);
  }
}
