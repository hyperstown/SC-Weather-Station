export class ElementShifter {
  target;
  maxOffsetX; // Maximum pixel offset
  maxOffsetY; // Maximum pixel offset
  offsetX = Math.floor(Math.random() * 5) + 2;
  offsetY = 1;
  directionX = 1;
  directionY = 1;

  constructor(target, offsetX = 5, offsetY = 5, interval = 60_000) {
    this.target = target;
    this.maxOffsetX = offsetX;
    this.maxOffsetY = offsetY;
    this.viewportHeight = window.innerHeight || document.documentElement.clientHeight;
    window.addEventListener('resize', () => { 
      this.viewportHeight = window.innerHeight || document.documentElement.clientHeight;
      this.offsetX = Math.floor(Math.random() * 5) + 2;
      this.offsetY = 1;
    })
    setInterval(this.moveElement.bind(this), interval);
  }

  moveElement() {
    this.offsetX += this.directionX;
    this.offsetY += this.directionY;
    const rect = this.target.getBoundingClientRect();
    
    if (
      (Math.abs(this.offsetX) >= this.maxOffsetX) || 
      (
        rect.left + this.directionX < 0 || 
        rect.right - this.directionX > this.viewportWidth
      )
    ) {
      this.directionX *= -1; // Reverse direction when reaching max offset
    }
    
    if (
      (Math.abs(this.offsetY) >= this.maxOffsetY) || 
      (
        rect.top + this.directionY < 0 || 
        rect.bottom - this.directionY > this.viewportHeight
      )
    ) {
      this.directionY *= -1; // Reverse direction when reaching max offset
    }
    
    this.target.style.transform = `translate(${this.offsetX}px, ${this.offsetY}px)`;
  }
}
