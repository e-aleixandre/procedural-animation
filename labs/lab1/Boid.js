class Boid extends Vehicle {
  
  constructor(x, y, objective) {
    // This is the position of the letter this boid occupies
    super(x, y);
    this.objective = objective;
    this.color = color(random(0, 255), random(0, 255), random(0, 255));
    this.size = random(1, 10);
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

  separate(boids, desiredSeparation) {
    const sum = createVector();
    let count = 0;

    for (let i = 0; i < boids.length; ++i) {
      const vec = p5.Vector.sub(this.location, boids[i].location);
      const distance = vec.mag();

      if (distance > 0 && distance < boids[i].radius + this.radius) {
        vec.normalize()
        vec.div(distance);
        sum.add(vec);
        ++count;
      }
    }

    if (count > 0)
    {
      sum.div(count);

      sum.setMag(this.maxspeed);
      
      const steer = p5.Vector.sub(sum, this.velocity);
      steer.limit(this.maxforce);

      return steer;
    } else {
      return createVector();
    }
  }

  align(boids, neighbourDistance) {
    const sum = createVector();
    let count = 0;

    for (let i = 0; i < boids.length; ++i)
    {
      const distance = p5.Vector.sub(this.location, boids[i].location).mag();

      if (distance > 0 && distance < neighbourDistance) {
        sum.add(boids[i].velocity);
        ++count;
      }
    }

    if (count > 0)
    {
      sum.div(count);
      sum.setMag(this.maxspeed);
      
      const steer = p5.Vector.sub(sum, this.velocity);
      steer.limit(this.maxforce);
      return steer;
    } else {
      return sum;  // Which is (0, 0)
    }
  }

  cohesion(boids, neighbourDistance) {
    const sum = createVector();
    let count = 0;

    for (let i = 0; i < boids.length; ++i)
    {
      const distance = p5.Vector.sub(this.location, boids[i].location).mag();

      if (distance > 0 && distance < neighbourDistance)
      {
        sum.add(boids[i].location);
        ++count;
      }
    }

    if (count > 0) {
      sum.div(count);
      return this.seek(sum);
    } else {
      return sum;  // Which is (0, 0);
    }
  }

  display() {    
    fill(this.color);
    stroke(0);
    strokeWeight(2);
    
    circle(this.location.x, this.location.y, this.size);
  }
}
