export class ElementShifter {
  target;
  maxOffsetX;
  maxOffsetY;
  offsetX = 0;
  offsetY = 0;
  directionX = 1;
  directionY = 1;
  stepX = 1;  // pixels per update
  stepY = 1;

  constructor(target, maxOffsetX = 8, maxOffsetY = 8, interval = 60_000) {
    this.target = target;
    this.maxOffsetX = maxOffsetX;
    this.maxOffsetY = maxOffsetY;
    this.stepX = 1;
    this.stepY = 1;

    // Start from a small random position around 0
    this.offsetX = Math.floor(Math.random() * 5) - 2; // e.g., -2 to +2
    this.offsetY = Math.floor(Math.random() * 3) - 1; // e.g., -1 to +1

    // Update viewport size
    this.updateViewportSize();
    window.addEventListener('resize', () => this.updateViewportSize());

    // Start shifter
    setInterval(() => this.moveElement(), interval);
  }

  updateViewportSize() {
    this.viewportWidth = window.innerWidth;
    this.viewportHeight = window.innerHeight;
  }

  moveElement() {
    // Predict next position
    const nextOffsetX = this.offsetX + this.directionX * this.stepX;
    const nextOffsetY = this.offsetY + this.directionY * this.stepY;

    const rect = this.target.getBoundingClientRect();
    const futureRect = {
      left: rect.left + (nextOffsetX - this.offsetX),
      right: rect.right + (nextOffsetX - this.offsetX),
      top: rect.top + (nextOffsetY - this.offsetY),
      bottom: rect.bottom + (nextOffsetY - this.offsetY),
    };

    const willHitEdgeX = futureRect.left < 0 || futureRect.right > this.viewportWidth;
    const willHitEdgeY = futureRect.top < 0 || futureRect.bottom > this.viewportHeight;

    // Check max offset and edges for X
    if (Math.abs(nextOffsetX) > this.maxOffsetX || willHitEdgeX) {
      this.directionX *= -1;
      // Clamp to max or edge (but since we're abrupt, just reverse next time)
    } else {
      this.offsetX = nextOffsetX;
    }

    // Same for Y
    if (Math.abs(nextOffsetY) > this.maxOffsetY || willHitEdgeY) {
      this.directionY *= -1;
    } else {
      this.offsetY = nextOffsetY;
    }

    // Apply instant shift (no transition for performance/simplicity)
    this.target.style.transform = `translate(${this.offsetX}px, ${this.offsetY}px)`;
  }
}