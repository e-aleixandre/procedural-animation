class FruitManager {
  constructor()
  {
    // The location of the fruit / target
    this.fruitLocation = null;
    this.hasFruit = false;
    this.timer = millis();
    
    this.consumerDistance = 2;
    
    // Times in milliseconds
    this.maxTimeBetweenFruits = 5000;
    this.minTimeBetweenFruits = 2000;
    this.fruitExpirationTime = 3500;
    
    // Time between fruits varies between 0 and maxTimeBetweenFruits to add dynamism
    this.currentTimeBetweenFruits = 0;
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
        this.currentTimeBetweenFruits = random(this.minTimeBetweenFruits, this.maxTimeBetweenFruits);
      }
    } else {
      // No fruit and time to spawn one
      if (millis() - this.timer >= this.currentTimeBetweenFruits)
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
  
  // Fruit gets consumed if consumer is close enough
  consume(consumerLocation)
  {
    // This is checked on main file, but just in case...
    if (!this.hasFruit) return false;
    
    const distance = p5.Vector.sub(this.fruitLocation, consumerLocation).mag();
    
    if (distance < this.consumerDistance)
    {
      this.hasFruit = false;
      this.fruitLocation = null;
      this.timer = millis();
      this.currentTimeBetweenFruits = random(this.minTimeBetweenFruits, this.maxTimeBetweenFruits);
      return true;
    } else {
      return false;
    }
  }
}
