class Boid {
  
  PVector acceleration;
  PVector velocity;
  PVector location;
  float radius;
  float maxspeed;
  float maxforce;
  ArrayList<Cell> path;
  int current;
  int ttl;

  Boid(float x, float y) {
    acceleration = new PVector();
    velocity = new PVector();
    location = new PVector(x, y);
    radius = 5.0;
    maxspeed = 4.0;
    maxforce = 1.0;
    ttl = 30;
  }

  Boid(ArrayList<Cell> path) {
    this(path.get(path.size() - 1).center.x, path.get(path.size() - 1).center.y);
    this.path = path;
    this.current = path.size() - 2;
  }
  
  void update() {
    velocity.add(acceleration);
    velocity.limit(maxspeed);
    location.add(velocity);
    acceleration.set(0, 0);
  }

  void applyForce(PVector force)
  {
    acceleration.add(force);
  }

  PVector seek(Cell cell) {
    PVector desired = PVector.sub(cell.center, location);
    desired.normalize();
    desired.mult(maxspeed);
    PVector steer = PVector.sub(desired, velocity);
    steer.limit(maxforce);

    return steer;
  }

  PVector arrive(Cell cell) {
    PVector desired = PVector.sub(cell.center, location);

    float d = desired.mag();

    desired.normalize();

    if (d < 50) {
      float m = map(d, 0, 50, 0, maxspeed);
      desired.mult(m);
    } else {
      desired.mult(maxspeed);
    }

    return PVector.sub(desired, velocity).limit(maxforce);
  }

  public float angleBetween(PVector v1, PVector v2)
  {
    float dot = v1.dot(v2);
    float theta = (float) Math.acos(dot / (v1.mag() * v2.mag()));
    return theta;
  }
  
  void draw() {
    float theta = this.velocity.heading() + PI / 2;
    
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

  void setPath(ArrayList<Cell> path) {
    this.path = path;
    this.current = path.size() - 2;
  }

  void followPath() {
    Cell cell = path.get(current);

    if (cell == null)
      return;

    if (PVector.sub(cell.center, location).magSq() < 5 && current > 0)
    {
      current--;
      cell = path.get(current);
    }
    
    if (current == 0)
    {
      applyForce(arrive(cell));
      ttl--;
    }
    else
      applyForce(seek(cell));
  }

  boolean isDead() {
    return ttl == 0;
  }
  
}
