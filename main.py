import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Bullets")

# Clock
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_COLOR = (0, 200, 255)
CANON_COLOR = (150, 0, 0)

# Fonts
font = pygame.font.SysFont(None, 60)
small_font = pygame.font.SysFont(None, 40)

# Player settings
player_width = 50
player_height = 60
player_x = 100
player_y = HEIGHT - player_height - 50
player_vel = 5
jumping = False
jump_vel = 10
gravity = 0.5
y_velocity = 0

# Canon settings
canon_x = WIDTH - 60
canon_y = HEIGHT - 100
canon_width = 40
canon_height = 60

# Bullet settings
bullet_width = 10
bullet_height = 10
bullet_speed = 4
bullet_timer = 0
bullet_interval = 60  # frames between shots
bullets = []

# Timer and level
start_time = pygame.time.get_ticks()
level = 1
LEVEL_DURATION = 60  # seconds
total_game_time = 3 * LEVEL_DURATION  # 3 levels

# Game state
game_over = False
won_game = False

# Game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic (only if not game over)
    if not game_over:
        # Timer update
        current_time = (pygame.time.get_ticks() - start_time) // 1000

        # Level progression logic
        if current_time < LEVEL_DURATION:
            level = 1
            bullet_speed = 4
            bullet_interval = 60
        elif current_time < LEVEL_DURATION * 2:
            level = 2
            bullet_speed = 6
            bullet_interval = 40
        elif current_time < LEVEL_DURATION * 3:
            level = 3
            bullet_speed = 8
            bullet_interval = 30
        else:
            won_game = True
            game_over = True

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_vel
        if keys[pygame.K_RIGHT]:
            player_x += player_vel
        if keys[pygame.K_UP] and not jumping:
            jumping = True
            y_velocity = -jump_vel

        # Gravity/jumping
        if jumping:
            player_y += y_velocity
            y_velocity += gravity
            if player_y >= HEIGHT - player_height - 50:
                player_y = HEIGHT - player_height - 50
                jumping = False

        # Update player rect
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

        # Bullet logic
        bullet_timer += 1
        if bullet_timer >= bullet_interval:
            bullet_timer = 0
            bullets.append({
                "x": canon_x,
                "y": canon_y + canon_height // 2 - bullet_height // 2,
                "rect": pygame.Rect(canon_x, canon_y + canon_height // 2 - bullet_height // 2, bullet_width, bullet_height)
            })

        for bullet in bullets:
            bullet["x"] -= bullet_speed
            bullet["rect"].x = bullet["x"]

        # Remove off-screen bullets
        bullets = [b for b in bullets if b["x"] + bullet_width > 0]

        # Collision detection
        for bullet in bullets:
            if player_rect.colliderect(bullet["rect"]):
                game_over = True
                break

    # Draw player
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)

    # Draw canon
    pygame.draw.rect(screen, CANON_COLOR, (canon_x, canon_y, canon_width, canon_height))

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, BLACK, bullet["rect"])

    # Game Over or Win Screen
    if game_over:
        if won_game:
            win_text = font.render("YOU HAVE BEAT THE MASTER!", True, (0, 150, 0))
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2 - 60))
        else:
            game_over_text = font.render("Game Over", True, (200, 0, 0))
            screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 60))

        retry_text = small_font.render("Press R to Play Again", True, (0, 0, 0))
        screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 20))

        # Restart logic
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reset all game state
            player_x = 100
            player_y = HEIGHT - player_height - 50
            jumping = False
            y_velocity = 0
            bullets = []
            bullet_timer = 0
            game_over = False
            won_game = False
            start_time = pygame.time.get_ticks()

    # Update display
    pygame.display.flip()

pygame.quit()
sys.exit()