// Global variables, consider these static class members
const arriveDistance = 100;
const maxWanderVariation = 0.39269908169872414;  // PI / 8, p5 isnt loaded when the class is imported so I predefined it

class Vehicle {
  
  constructor(x, y) {
    this.acceleration = createVector();
    this.velocity = createVector();
    this.location = createVector(x, y);
    this.radius = 5.0;
    this.maxspeed = 4.0;
    this.maxforce = 1.0;
    
    this.wanderAngle = 0.0;
    this.fleeDistance = 100;
  }
  
  update() {
    this.velocity.add(this.acceleration);
    this.velocity.limit(this.maxspeed);
    this.location.add(this.velocity);
    this.acceleration.set(0, 0);
  }
  
  applyForce(force)
  {
    // Should limit the force. For now considering it limited by other functions
    this.acceleration.add(force);
  }
  
  seek(target) {
    let desiredVelocity = p5.Vector.sub(target, this.location);
    desiredVelocity.setMag(this.maxspeed);
    
    let steer = p5.Vector.sub(desiredVelocity, this.velocity);
    
    steer.limit(this.maxforce);
    
    return steer;
  }
  
  flee(target) {
    return this.seek(target).mult(-1); 
  }
  
  /**
  * param draw is a boolean to draw the circle that illustrates the calculation of the next wandering angle
  **/
  fleeAndWander(target, draw)
  {
    let fleeVelocity = p5.Vector.sub(this.location, target);
    
    if (fleeVelocity.mag() < this.fleeDistance) {
      console.log("Should flee, distance: ", fleeVelocity.mag());
      return this.flee(target);
    } else {
      console.log("Should wander, distance: ", fleeVelocity.mag());
      return this.wander(draw);
    }
  }
  
  pursue(target) {
    let prediction = target.location.copy();
    
    // How many frames ahead? 20 (1/3) seems a reasonable number
    prediction.add(p5.Vector.mult(target.velocity, 20));
    
    return this.seek(prediction);
  }
  
  evade(target)
  {
    return this.pursue(target).mult(-1);
  }
  
  wander(draw)
  {
    // 1. Determine a circle that will contain the target
    // 2. Get a random angle variation and add it to the current angle
    // 3. Find the point in the circumference at that angle
    // 4. Call seek with that point as argument (?)

    // Step 1
    // Circle is at vehicle location + normalized velocity direction * circleDistance
    const radius = 25;
    const circleDistance = 75;
    const circleCenter = p5.Vector.add(this.location, this.velocity.copy().setMag(circleDistance));
    
    // Step 2
    this.wanderAngle += random(-maxWanderVariation, maxWanderVariation);
    
    // Step 3
    // Polar coordinates
    // x = r * cos(angle)
    // y = r * sin(angle)
    // NOTE: Reynolds actually displaces the circlePoint around a smaller circle and maps the point to the bigger circle
    const circlePoint = createVector(circleCenter.x + radius * cos(this.wanderAngle), circleCenter.y + radius * sin(this.wanderAngle));
    
    // This is kind of an anti-pattern, drawing in the update function
    if (draw)
    {
        noFill();
        stroke(255, 255, 255);
        circle(circleCenter.x, circleCenter.y, radius * 2);
        line(circleCenter.x, circleCenter.y, location.x, location.y);
        line(circleCenter.x, circleCenter.y, circlePoint.x, circlePoint.y);
        fill(255, 255, 255);
        circle(circlePoint.x, circlePoint.y, 5);
    }

    // Step 4
    return this.seek(circlePoint);
  }
  
  arrive(target) {
    let desiredVelocity = p5.Vector.sub(target, this.location);
    
    let distanceToTarget = desiredVelocity.mag();
    
    // Adjusting desiredVelocity magnitude depending on target distance
    let velocityMagnitude = distanceToTarget < arriveDistance ? distanceToTarget * this.maxspeed / arriveDistance : this.maxspeed;
    desiredVelocity.setMag(velocityMagnitude);
    
    let steer = p5.Vector.sub(desiredVelocity, this.velocity);
    steer.limit(this.maxforce);
    
    return steer;
  }
  
  display() {
    const theta = this.velocity.heading() + window.PI / 2;
    
    fill(175);
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
  
}
