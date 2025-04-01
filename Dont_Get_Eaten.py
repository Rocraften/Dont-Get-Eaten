# Made by Rocraften
# Don't Get Eaten V2
import pygame
import random
import sys
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Don't Get Eaten!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (40, 40, 40)
GOLD = (255, 215, 0)
NEON_BLUE = (80, 200, 255)

PLAYER_SIZE = 20
player_x = WIDTH // 2
player_y = HEIGHT // 2
player_speed = 4
player_score = 0
high_score = 0

SNAKE_SIZE = 25
snake_segments = [(100, 100)]
snake_base_speed = 1
snake_length = 3

FOOD_SIZE = 15
food_x = random.randint(50, WIDTH - 50)
food_y = random.randint(50, HEIGHT - 50)

def draw_rounded_rect(surface, color, rect, radius):
    pygame.draw.rect(surface, color, rect.inflate(-radius * 2, 0))
    pygame.draw.rect(surface, color, rect.inflate(0, -radius * 2))
    pygame.draw.circle(surface, color, (rect.left + radius, rect.top + radius), radius)
    pygame.draw.circle(surface, color, (rect.right - radius, rect.top + radius), radius)
    pygame.draw.circle(surface, color, (rect.left + radius, rect.bottom - radius), radius)
    pygame.draw.circle(surface, color, (rect.right - radius, rect.bottom - radius), radius)

def draw_menu():
    for y in range(HEIGHT):
        color_value = int(255 * (1 - y/HEIGHT))
        pygame.draw.line(WINDOW, (color_value//8, 0, color_value//2), (0, y), (WIDTH, y))
    
    # animated background elements
    current_time = pygame.time.get_ticks()
    for i in range(20):  # Add some stars/particles
        x = (current_time // 20 + i * 40) % WIDTH
        y = (i * 30 + current_time // 50) % HEIGHT
        size = 2 + math.sin(current_time / 500 + i) * 2
        pygame.draw.circle(WINDOW, (255, 255, 255), (x, y), size)
    
    # fonts
    title_font = pygame.font.Font(None, 120)
    button_font = pygame.font.Font(None, 72)
    
    # title glow effect
    glow_colors = [(0, 50, 100), (0, 70, 140), (0, 90, 180)]
    title_text = "Don't Get Eaten!"
    
    for i, color in enumerate(glow_colors):
        glow = title_font.render(title_text, True, color)
        offset = 6 - i*2  # Decreasing offset for inner glow layers
        WINDOW.blit(glow, (WIDTH//2 - glow.get_width()//2 + offset, HEIGHT//4 + offset))
    
    title = title_font.render(title_text, True, NEON_BLUE)
    WINDOW.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))
    
    # button design
    play_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2, 300, 70)
    quit_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 + 100, 300, 70)
    
    for rect, text in [(play_rect, "Play Game"), (quit_rect, "Quit")]:
        # Add button shadow
        shadow_rect = rect.copy()
        shadow_rect.x += 4
        shadow_rect.y += 4
        draw_rounded_rect(WINDOW, (20, 20, 30), shadow_rect, 20)
        
        if rect.collidepoint(pygame.mouse.get_pos()):
            # Animated highlight for hovered buttons
            highlight = abs(math.sin(current_time * 0.005)) * 50 + 150
            draw_rounded_rect(WINDOW, (0, highlight//3, highlight), rect, 20)
            text_color = WHITE
        else:
            draw_rounded_rect(WINDOW, (40, 40, 80), rect, 20)
            text_color = (200, 200, 200)
        
        # Add button border
        pygame.draw.rect(WINDOW, NEON_BLUE, rect, 2, border_radius=20)
            
        text_surf = button_font.render(text, True, text_color)
        WINDOW.blit(text_surf, (rect.centerx - text_surf.get_width()//2,
                               rect.centery - text_surf.get_height()//2))
    
    # controls text with icon hints
    controls_font = pygame.font.Font(None, 48)
    controls_text = "Controls: Arrow Keys or WASD"
    controls_surf = controls_font.render(controls_text, True, (180, 180, 220))
    WINDOW.blit(controls_surf, (WIDTH//2 - controls_surf.get_width()//2, HEIGHT - 80))
    
    if high_score > 0:
        score_font = pygame.font.Font(None, 56)
        score_text = f"High Score: {high_score}"
        # Add trophy icon or animation for high score
        glow = abs(math.sin(current_time * 0.003)) * 55 + 200
        score_surf = score_font.render(score_text, True, (glow, glow//1.5, 0))
        WINDOW.blit(score_surf, (WIDTH//2 - score_surf.get_width()//2, HEIGHT//4 + 80))
    
    return play_rect, quit_rect

def game_loop():
    global player_x, player_y, player_score, food_x, food_y, snake_length, high_score
    
    running = True
    clock = pygame.time.Clock()
    snake_segments = [(100, 100)]
    
    # Add particle effects for player movement
    particles = []
    
    while running:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return True

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 0:
            player_x -= player_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < WIDTH - PLAYER_SIZE:
            player_x += player_speed
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player_y > 0:
            player_y -= player_speed
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_y < HEIGHT - PLAYER_SIZE:
            player_y += player_speed

        snake_speed = snake_base_speed + (player_score // 50) * 0.2
        
        head_x, head_y = snake_segments[0]
        if head_x < player_x:
            head_x += snake_speed
        if head_x > player_x:
            head_x -= snake_speed
        if head_y < player_y:
            head_y += snake_speed
        if head_y > player_y:
            head_y -= snake_speed
        
        snake_segments.insert(0, (head_x, head_y))
        if len(snake_segments) > snake_length:
            snake_segments.pop()

        if (abs(player_x - food_x) < PLAYER_SIZE + 5 and 
            abs(player_y - food_y) < PLAYER_SIZE + 5):
            player_score += 10
            snake_length += 1
            food_x = random.randint(50, WIDTH - 50)
            food_y = random.randint(50, HEIGHT - 50)

        for segment in snake_segments[3:]:
            if (abs(player_x - segment[0]) < PLAYER_SIZE - 5 and 
                abs(player_y - segment[1]) < PLAYER_SIZE - 5):
                high_score = max(high_score, player_score)
                game_over()
                return True
                
        if (player_x <= 0 or player_x >= WIDTH - PLAYER_SIZE or 
            player_y <= 0 or player_y >= HEIGHT - PLAYER_SIZE):
            high_score = max(high_score, player_score)
            game_over()
            return True

        # Add player trail effect
        if random.random() > 0.7:
            particles.append([player_x + PLAYER_SIZE//2, player_y + PLAYER_SIZE//2, 
                             random.randint(3, 8), (80, 180, 255), 30])
        
        # Update particles
        for particle in particles[:]:
            particle[2] -= 0.2
            particle[4] -= 1
            if particle[2] <= 0 or particle[4] <= 0:
                particles.remove(particle)
        
        # Draw background with subtle grid pattern
        WINDOW.fill((10, 10, 20))
        for x in range(0, WIDTH, 40):
            for y in range(0, HEIGHT, 40):
                pygame.draw.rect(WINDOW, (20, 20, 30), (x, y, 39, 39))
        
        # Draw particles
        for particle in particles:
            pygame.draw.circle(WINDOW, particle[3], (particle[0], particle[1]), particle[2])
        
        # Draw snake visuals
        for i, segment in enumerate(snake_segments):
            color_intensity = 255 - (i * (255 // max(1, len(snake_segments))))
            color_intensity = max(100, color_intensity)
            
            # Add glowing effect to snake head
            if i == 0:
                glow_size = 5 + math.sin(current_time * 0.01) * 2
                pygame.draw.circle(WINDOW, (color_intensity//2, 0, 0), 
                                 (segment[0] + SNAKE_SIZE//2, segment[1] + SNAKE_SIZE//2), 
                                 SNAKE_SIZE//2 + glow_size)
            
            # Draw rounded snake segments
            pygame.draw.rect(WINDOW, (color_intensity, 0, 0), 
                           (segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE), 
                           border_radius=8)
            
            # Add eyes to snake head
            if i == 0:
                eye_size = 4
                pygame.draw.circle(WINDOW, WHITE, 
                                 (segment[0] + SNAKE_SIZE//3, segment[1] + SNAKE_SIZE//3), 
                                 eye_size)
                pygame.draw.circle(WINDOW, WHITE, 
                                 (segment[0] + SNAKE_SIZE*2//3, segment[1] + SNAKE_SIZE//3), 
                                 eye_size)
        
        pygame.draw.rect(WINDOW, (0, 50, 100),
                       (player_x-3, player_y-3, PLAYER_SIZE+6, PLAYER_SIZE+6),
                       border_radius=10)
        pygame.draw.rect(WINDOW, NEON_BLUE,
                       (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE),
                       border_radius=8)
        
        # food appearance
        pulse = abs(math.sin(current_time * 0.005)) * 3
        food_center = (food_x + FOOD_SIZE//2, food_y + FOOD_SIZE//2)
        
        # Outer glow
        pygame.draw.circle(WINDOW, (0, 100, 0), food_center, FOOD_SIZE + pulse + 5)
        # Inner circle
        pygame.draw.circle(WINDOW, GREEN, food_center, FOOD_SIZE + pulse)
        # Highlight
        pygame.draw.circle(WINDOW, (200, 255, 200), 
                         (food_center[0]-FOOD_SIZE//4, food_center[1]-FOOD_SIZE//4), 
                         FOOD_SIZE//4)
        
        # score display
        score_font = pygame.font.Font(None, 56)
        score_text = f'Score: {player_score}'
        score_surface = score_font.render(score_text, True, WHITE)
        score_bg = pygame.Rect(20, 15, score_surface.get_width() + 30, 60)
        draw_rounded_rect(WINDOW, (0, 0, 0, 150), score_bg, 10)
        WINDOW.blit(score_surface, (35, 25))

        pygame.display.flip()
        clock.tick(60)
def game_over():
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.fill(BLACK)
    for alpha in range(0, 255, 5):
        fade_surface.set_alpha(alpha)
        WINDOW.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(5)
    
    font = pygame.font.Font(None, 120)
    score_font = pygame.font.Font(None, 72)
    
    text = font.render('Game Over!', True, RED)
    score_text = score_font.render(f'Score: {player_score}', True, WHITE)
    
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 40))
    score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 40))
    
    WINDOW.blit(text, text_rect)
    WINDOW.blit(score_text, score_rect)
    
    continue_font = pygame.font.Font(None, 48)
    continue_text = continue_font.render('Press any key to continue', True, WHITE)
    continue_rect = continue_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 120))
    
    alpha = 255
    alpha_change = -5
    
    waiting = True
    clock = pygame.time.Clock()
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
        
        WINDOW.fill(BLACK)
        WINDOW.blit(text, text_rect)
        WINDOW.blit(score_text, score_rect)
        
        continue_surface = continue_text.copy()
        continue_surface.set_alpha(abs(alpha))
        WINDOW.blit(continue_surface, continue_rect)
        
        alpha += alpha_change
        if alpha <= 0 or alpha >= 255:
            alpha_change *= -1
            
        pygame.display.flip()
        clock.tick(60)

running = True
in_menu = True

while running:
    if in_menu:
        play_button, quit_button = draw_menu()
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_button.collidepoint(mouse_pos):
                    in_menu = False
                    player_score = 0
                    player_x = WIDTH // 2
                    player_y = HEIGHT // 2
                    snake_length = 3
                elif quit_button.collidepoint(mouse_pos):
                    running = False
                    pygame.quit()
                    sys.exit()
    else:
        in_menu = game_loop()

pygame.quit()
sys.exit()
