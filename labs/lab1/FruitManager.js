class FruitManager {
  constructor()
  {
    // The location of the fruit / target
    this.fruitLocation = null;
    this.hasFruit = false;
    this.timer = millis();
    
    // Times in milliseconds
    this.timeBetweenFruits = 5000;
    this.fruitExpirationTime = 3500;
  }
  
  /**
  * Expected behaviour:
  *   - Generate a randomly placed fruit if enough time has passed
  *   - Remove a fruit if enough time has passed
  **/
  update()
  {
    if (this.hasFruit)
    {
      // Has fruit and has expired
      if (millis() - this.timer >= this.fruitExpirationTime)
      {
        this.hasFruit = false;
        this.fruitLocation = null;
        this.timer = millis();
      }
    } else {
      // No fruit and time to spawn one
      if (millis() - this.timer >= this.timeBetweenFruits)
      {
        this.hasFruit = true;
        this.fruitLocation = createVector(random(0, width), random(0, height));
        this.timer = millis();
      }
    }
  }
  
  display()
  {
    if (!this.hasFruit)
    {
      return;
    }
    
    stroke(0);
    strokeWeight(1);
    fill('orange');
    circle(this.fruitLocation.x, this.fruitLocation.y, 10);
  }
  
  // Fruit gets consumed
  consume()
  {
    this.hasFruit = false;
    this.fruitLocation = null;
    this.timer = millis();
  }
}
