import pygame
import random

# Initialize pygame
pygame.init()
      
# Constants
WIDTH, HEIGHT = 400, 600
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_WIDTH = 70
PIPE_GAP = 150
PIPE_SPEED = 3
FPS = 60

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Load assets
font = pygame.font.Font(None, 36)

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.width = 30
        self.height = 30
        self.velocity = 0
    
    def jump(self):
        self.velocity = JUMP_STRENGTH
    
    def move(self):
        self.velocity += GRAVITY
        self.y += self.velocity
    
    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, 400)
    
    def move(self):
        self.x -= PIPE_SPEED
    
    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        pygame.draw.rect(screen, GREEN, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT))
    
    def collide(self, bird):
        if (bird.x < self.x + PIPE_WIDTH and bird.x + bird.width > self.x and
           (bird.y < self.height or bird.y + bird.height > self.height + PIPE_GAP)):
            return True
        return False

def main():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe(WIDTH + i * 200) for i in range(3)]
    running = True
    score = 0

    while running:
        clock.tick(FPS)
        screen.fill(WHITE)
        
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()
        
        # Move bird
        bird.move()
        bird.draw()
        
        # Move pipes
        for pipe in pipes:
            pipe.move()
            pipe.draw()
            
            if pipe.collide(bird) or bird.y > HEIGHT or bird.y < 0:
                running = False  # End game on collision
            
            if pipe.x + PIPE_WIDTH < 0:
                pipes.remove(pipe)
                pipes.append(Pipe(WIDTH))
                score += 1
        
        # Display score
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    main()
