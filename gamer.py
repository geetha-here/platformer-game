import pygame
import random

# Initialize pygame
pygame.init()

# Game settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
GRAVITY = 1
PLAYER_SPEED = 5
JUMP_STRENGTH = 15

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Advanced Platformer")

# Clock
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.velocity_y = 0
        self.jumping = False

    def update(self):
        keys = pygame.key.get_pressed()

        # Horizontal movement
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        # Jumping
        if keys[pygame.K_SPACE] and not self.jumping:
            self.velocity_y = -JUMP_STRENGTH
            self.jumping = True

        # Gravity
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Check ground
        if self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.velocity_y = 0
            self.jumping = False

        # Screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.direction = random.choice([-1, 1])
    
    def update(self):
        self.rect.x += self.direction * 3
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.direction *= -1

# Setup
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)

platform_group = pygame.sprite.Group()
platforms = [
    Platform(100, SCREEN_HEIGHT - 200, 200, 20),
    Platform(400, SCREEN_HEIGHT - 300, 200, 20),
    Platform(200, SCREEN_HEIGHT - 400, 200, 20)
]
platform_group.add(*platforms)

enemy_group = pygame.sprite.Group()
for i in range(5):
    enemy = Enemy(random.randint(0, SCREEN_WIDTH - 40), random.randint(0, SCREEN_HEIGHT - 300))
    enemy_group.add(enemy)

# Game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    player.update()
    enemy_group.update()

    # Collisions
    if pygame.sprite.spritecollide(player, platform_group, False):
        player.velocity_y = 0
        player.jumping = False
    
    if pygame.sprite.spritecollide(player, enemy_group, False):
        print("Game Over!")
        running = False

    # Draw
    platform_group.draw(screen)
    enemy_group.draw(screen)
    player_group.draw(screen)

    # Update display
    pygame.display.flip()

pygame.quit()
