# Project: Penguin Platformer
# Version :  0.1
# Date    :  3/10/2025
# Author: Jody Ingram
# Pre-reqs: Requires PyGame libraries - https://pypi.org/project/pygame
# Fun platformer starring a Penguin

import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -12
PLAYER_SPEED = 5
SNOWFLAKE_COUNT = 100

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
SKY_BLUE = (135, 206, 235)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (25, 25, 112)
ICE_BLUE = (220, 240, 255)
GRAY = (128, 128, 128)

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2

class Penguin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.facing_right = True
        self.animation_count = 0
        self.jump_count = 0
        self.health = 100
        
    def update(self, platforms):
        # Apply gravity
        self.vel_y += GRAVITY
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Check boundaries
        if self.x < 0:
            self.x = 0
        if self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
        
        # Reset on_ground
        self.on_ground = False
        
        # Check collision with platforms
        for platform in platforms:
            if self.check_collision(platform):
                # Collision from top
                if self.vel_y > 0 and self.y + self.height - self.vel_y <= platform.y:
                    self.y = platform.y - self.height
                    self.vel_y = 0
                    self.on_ground = True
                    self.jump_count = 0
                # Collision from bottom
                elif self.vel_y < 0 and self.y - self.vel_y >= platform.y + platform.height:
                    self.y = platform.y + platform.height
                    self.vel_y = 0
                # Collision from left
                elif self.vel_x > 0 and self.x + self.width - self.vel_x <= platform.x:
                    self.x = platform.x - self.width
                    self.vel_x = 0
                # Collision from right
                elif self.vel_x < 0 and self.x - self.vel_x >= platform.x + platform.width:
                    self.x = platform.x + platform.width
                    self.vel_x = 0
        
        # Animation counter
        if self.vel_x != 0:
            self.animation_count = (self.animation_count + 1) % 30
        else:
            self.animation_count = 0
            
        # Update facing direction
        if self.vel_x > 0:
            self.facing_right = True
        elif self.vel_x < 0:
            self.facing_right = False
    
    def jump(self):
        if self.on_ground and self.jump_count < 2:
            self.vel_y = JUMP_STRENGTH
            self.jump_count += 1
            self.on_ground = False
    
    def check_collision(self, platform):
        return (
            self.x < platform.x + platform.width and
            self.x + self.width > platform.x and
            self.y < platform.y + platform.height and
            self.y + self.height > platform.y
        )
    
    def draw(self, screen):
        # Body (dark blue oval)
        pygame.draw.ellipse(screen, DARK_BLUE, 
                           (self.x, self.y + 10, self.width, self.height - 10))
        
        # Belly (white oval)
        belly_width = self.width * 0.7
        belly_height = (self.height - 10) * 0.7
        belly_x = self.x + (self.width - belly_width) / 2
        belly_y = self.y + 20
        pygame.draw.ellipse(screen, WHITE, 
                           (belly_x, belly_y, belly_width, belly_height))
        
        # Head (dark blue circle)
        head_radius = self.width // 2
        head_x = self.x + self.width // 2
        head_y = self.y + 5
        pygame.draw.circle(screen, DARK_BLUE, (head_x, head_y), head_radius)
        
        # Eyes (white circles)
        eye_radius = head_radius // 4
        eye_y = head_y - 2
        
        # Adjust eye position based on direction
        if self.facing_right:
            left_eye_x = head_x - head_radius // 2
            right_eye_x = head_x + head_radius // 3
        else:
            left_eye_x = head_x - head_radius // 3
            right_eye_x = head_x + head_radius // 2
            
        pygame.draw.circle(screen, WHITE, (left_eye_x, eye_y), eye_radius)
        pygame.draw.circle(screen, WHITE, (right_eye_x, eye_y), eye_radius)
        
        # Pupils (black circles)
        pupil_radius = eye_radius // 2
        if self.facing_right:
            pygame.draw.circle(screen, BLACK, (left_eye_x + 1, eye_y), pupil_radius)
            pygame.draw.circle(screen, BLACK, (right_eye_x + 1, eye_y), pupil_radius)
        else:
            pygame.draw.circle(screen, BLACK, (left_eye_x - 1, eye_y), pupil_radius)
            pygame.draw.circle(screen, BLACK, (right_eye_x - 1, eye_y), pupil_radius)
        
        # Beak (orange triangle)
        beak_color = (255, 165, 0)  # Orange
        beak_y = head_y + 2
        if self.facing_right:
            beak_points = [
                (head_x + head_radius - 5, beak_y - 5),
                (head_x + head_radius + 10, beak_y),
                (head_x + head_radius - 5, beak_y + 5)
            ]
        else:
            beak_points = [
                (head_x - head_radius + 5, beak_y - 5),
                (head_x - head_radius - 10, beak_y),
                (head_x - head_radius + 5, beak_y + 5)
            ]
        pygame.draw.polygon(screen, beak_color, beak_points)
        
        # Feet
        feet_color = (255, 165, 0)  # Orange
        feet_y = self.y + self.height - 5
        
        # Walking animation (move feet back and forth)
        if self.vel_x != 0:
            feet_offset = math.sin(self.animation_count * 0.2) * 5
        else:
            feet_offset = 0
            
        if self.facing_right:
            left_foot_x = self.x + self.width // 3 - feet_offset
            right_foot_x = self.x + 2 * self.width // 3 + feet_offset
        else:
            left_foot_x = self.x + self.width // 3 + feet_offset
            right_foot_x = self.x + 2 * self.width // 3 - feet_offset
            
        pygame.draw.polygon(screen, feet_color, [
            (left_foot_x, feet_y),
            (left_foot_x - 10, feet_y + 5),
            (left_foot_x + 10, feet_y + 5)
        ])
        
        pygame.draw.polygon(screen, feet_color, [
            (right_foot_x, feet_y),
            (right_foot_x - 10, feet_y + 5),
            (right_foot_x + 10, feet_y + 5)
        ])
        
        # Flippers
        flipper_color = DARK_BLUE
        flipper_y = self.y + 30
        flipper_height = 10
        flipper_width = 15
        
        # Flipper animation
        if self.vel_x != 0:
            flipper_angle = math.sin(self.animation_count * 0.2) * 20
        else:
            flipper_angle = 0
            
        if self.facing_right:
            flipper_x = self.x + self.width
            pygame.draw.ellipse(screen, flipper_color, 
                              pygame.Rect(flipper_x - 5, flipper_y, flipper_width, flipper_height))
        else:
            flipper_x = self.x
            pygame.draw.ellipse(screen, flipper_color, 
                              pygame.Rect(flipper_x - flipper_width + 5, flipper_y, flipper_width, flipper_height))

class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = ICE_BLUE
        self.border_color = LIGHT_BLUE
        
    def draw(self, screen):
        # Main platform
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # Top edge highlight
        pygame.draw.line(screen, WHITE, (self.x, self.y), (self.x + self.width, self.y), 2)
        
        # Left edge highlight
        pygame.draw.line(screen, WHITE, (self.x, self.y), (self.x, self.y + self.height), 2)
        
        # Bottom edge shadow
        pygame.draw.line(screen, self.border_color, 
                        (self.x, self.y + self.height - 1), 
                        (self.x + self.width, self.y + self.height - 1), 2)
        
        # Right edge shadow
        pygame.draw.line(screen, self.border_color, 
                        (self.x + self.width - 1, self.y), 
                        (self.x + self.width - 1, self.y + self.height), 2)
        
        # Ice crystals (small details)
        for i in range(int(self.width / 20)):
            crystal_x = self.x + 10 + i * 20
            crystal_y = self.y + 3
            
            if random.random() < 0.3:  # Only draw some crystals
                size = random.randint(2, 4)
                pygame.draw.rect(screen, WHITE, (crystal_x, crystal_y, size, size))

class Snowflake:
    def __init__(self):
        self.reset()
        self.y = random.randint(0, SCREEN_HEIGHT)
        
    def reset(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = -10
        self.speed = random.uniform(1, 3)
        self.size = random.randint(1, 4)
        self.wobble = random.uniform(-0.5, 0.5)
        self.wobble_speed = random.uniform(0.01, 0.05)
        self.wobble_counter = random.uniform(0, 6.28)  # Random start in the sin wave
        
    def update(self):
        self.y += self.speed
        self.wobble_counter += self.wobble_speed
        self.x += math.sin(self.wobble_counter) * self.wobble
        
        if self.y > SCREEN_HEIGHT:
            self.reset()
        
        if self.x < 0 or self.x > SCREEN_WIDTH:
            self.reset()
            
    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size)

def draw_background(screen):
    # Create a gradient sky
    for y in range(SCREEN_HEIGHT):
        # Calculate color based on y position
        r = int(135 - (y / SCREEN_HEIGHT * 50))
        g = int(206 - (y / SCREEN_HEIGHT * 100))
        b = int(235)
        
        color = (max(0, r), max(0, g), b)
        pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))
    
    # Draw distant mountains
    mountain_color = (220, 220, 255)  # Light bluish-white
    for i in range(4):
        base_x = SCREEN_WIDTH * i / 3
        width = random.randint(200, 400)
        height = random.randint(100, 200)
        
        points = [
            (base_x - width/2, SCREEN_HEIGHT - 100),
            (base_x, SCREEN_HEIGHT - 100 - height),
            (base_x + width/2, SCREEN_HEIGHT - 100)
        ]
        
        pygame.draw.polygon(screen, mountain_color, points)
    
    # Draw snow on the ground
    ground_rect = pygame.Rect(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100)
    pygame.draw.rect(screen, WHITE, ground_rect)
    
    # Draw some snow mounds
    for i in range(10):
        x = random.randint(0, SCREEN_WIDTH)
        width = random.randint(50, 150)
        height = random.randint(10, 30)
        
        pygame.draw.ellipse(screen, WHITE, 
                          (x - width/2, SCREEN_HEIGHT - 100 - height/2, width, height))

def draw_menu(screen, font):
    title_font = pygame.font.Font(None, 64)
    title_text = title_font.render("Penguin Platformer", True, DARK_BLUE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
    
    instruction_text = font.render("Press SPACE to Start", True, BLACK)
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    
    credit_text = font.render("Use Arrow Keys or A/D to Move, SPACE to Jump", True, BLACK)
    credit_rect = credit_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT*2/3))
    
    screen.blit(title_text, title_rect)
    screen.blit(instruction_text, instruction_rect)
    screen.blit(credit_text, credit_rect)
    
    # Draw a cute penguin on the menu
    menu_penguin = Penguin(SCREEN_WIDTH/2 - 20, SCREEN_HEIGHT*3/4)
    menu_penguin.draw(screen)

def draw_game_over(screen, font, score):
    title_font = pygame.font.Font(None, 64)
    title_text = title_font.render("Game Over", True, DARK_BLUE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
    
    score_text = font.render(f"Final Score: {score}", True, BLACK)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    
    instruction_text = font.render("Press SPACE to Play Again", True, BLACK)
    instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT*2/3))
    
    screen.blit(title_text, title_rect)
    screen.blit(score_text, score_rect)
    screen.blit(instruction_text, instruction_rect)

def draw_hud(screen, font, score, health):
    # Draw score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (20, 20))
    
    # Draw health bar
    bar_width = 150
    bar_height = 20
    filled_width = (health / 100) * bar_width
    
    pygame.draw.rect(screen, GRAY, (SCREEN_WIDTH - bar_width - 20, 20, bar_width, bar_height))
    pygame.draw.rect(screen, (255, 0, 0), (SCREEN_WIDTH - bar_width - 20, 20, filled_width, bar_height))
    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - bar_width - 20, 20, bar_width, bar_height), 2)
    
    health_text = font.render(f"Health: {health}", True, BLACK)
    screen.blit(health_text, (SCREEN_WIDTH - bar_width - 20, 45))

def main():
    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Penguin Platformer")
    
    # Set up clock
    clock = pygame.time.Clock()
    
    # Set up font
    font = pygame.font.Font(None, 36)
    
    # Initialize game state
    game_state = MENU
    score = 0
    
    # Initialize penguin
    penguin = Penguin(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
    
    # Create platforms
    platforms = [
        # Ground
        Platform(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 20),
        
        # Floating platforms
        Platform(100, SCREEN_HEIGHT - 200, 150, 20),
        Platform(350, SCREEN_HEIGHT - 250, 150, 20),
        Platform(550, SCREEN_HEIGHT - 300, 150, 20),
        Platform(250, SCREEN_HEIGHT - 350, 150, 20),
        Platform(50, SCREEN_HEIGHT - 400, 150, 20),
        Platform(400, SCREEN_HEIGHT - 450, 150, 20),
    ]
    
    # Create snowflakes
    snowflakes = [Snowflake() for _ in range(SNOWFLAKE_COUNT)]
    
    # Collectible items for score
    class Collectible:
        def __init__(self, x, y):
            self.x = x
            self.y = y
            self.width = 15
            self.height = 15
            self.collected = False
            
        def draw(self, screen):
            if not self.collected:
                pygame.draw.circle(screen, (255, 215, 0), (self.x + self.width//2, self.y + self.height//2), self.width//2)
                pygame.draw.circle(screen, (255, 255, 0), (self.x + self.width//2, self.y + self.height//2), self.width//3)
                
        def check_collision(self, penguin):
            if not self.collected:
                if (penguin.x < self.x + self.width and
                    penguin.x + penguin.width > self.x and
                    penguin.y < self.y + self.height and
                    penguin.y + penguin.height > self.y):
                    self.collected = True
                    return True
            return False
    
    # Create collectibles
    collectibles = []
    for platform in platforms:
        for i in range(2):
            x = platform.x + random.randint(20, platform.width - 20)
            y = platform.y - 30
            collectibles.append(Collectible(x, y))
    
    # Game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                if game_state == MENU and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                    game_state = PLAYING
                    score = 0
                    penguin = Penguin(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
                    # Reset collectibles
                    for collectible in collectibles:
                        collectible.collected = False
                    
                if game_state == GAME_OVER and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                    game_state = PLAYING
                    score = 0
                    penguin = Penguin(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
                    # Reset collectibles
                    for collectible in collectibles:
                        collectible.collected = False
                
                if game_state == PLAYING:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                        penguin.jump()
        
        # Update game logic based on state
        if game_state == PLAYING:
            # Handle keyboard input
            keys = pygame.key.get_pressed()
            penguin.vel_x = 0
            
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                penguin.vel_x = -PLAYER_SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                penguin.vel_x = PLAYER_SPEED
                
            # Update penguin
            penguin.update(platforms)
            
            # Check collectibles
            for collectible in collectibles:
                if collectible.check_collision(penguin):
                    score += 10
            
            # Update snowflakes
            for snowflake in snowflakes:
                snowflake.update()
            
            # Check if player fell off the screen
            if penguin.y > SCREEN_HEIGHT:
                game_state = GAME_OVER
                
            # Check if health is depleted
            if penguin.health <= 0:
                game_state = GAME_OVER
        
        # Draw everything
        draw_background(screen)
        
        # Draw snowflakes
        for snowflake in snowflakes:
            snowflake.draw(screen)
        
        if game_state == MENU:
            draw_menu(screen, font)
        elif game_state == PLAYING:
            # Draw platforms
            for platform in platforms:
                platform.draw(screen)
                
            # Draw collectibles
            for collectible in collectibles:
                collectible.draw(screen)
                
            # Draw penguin
            penguin.draw(screen)
            
            # Draw HUD
            draw_hud(screen, font, score, penguin.health)
            
        elif game_state == GAME_OVER:
            draw_game_over(screen, font, score)
        
        # Update display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)
    
    # Quit pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
