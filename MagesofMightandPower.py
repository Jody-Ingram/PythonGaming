# Project: Mages of Might and Power
# Version :  0.1
# Date    :  3/10/2025
# Author: Jody Ingram
# Pre-reqs: Requires PyGame libraries - https://pypi.org/project/pygame
# Select your specific mage; kill 20 enemies to win; get hit and loose

import pygame
import sys
import os
import random
from enemy import Enemy

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PLAYER_SPEED = 5
GRAVITY = 0.5
JUMP_STRENGTH = -10
PROJECTILE_SPEED = 7
ENEMY_SPAWN_RATE = 2000  # milliseconds

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Mages of Might and Power")
clock = pygame.time.Clock()

# Create placeholder images
def create_colored_surface(width, height, color):
    surface = pygame.Surface((width, height))
    surface.fill(color)
    return surface

# Projectile class
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, mage_type):
        super().__init__()
        self.mage_type = mage_type
        
        # Set properties based on mage type
        if mage_type == "fire":
            self.color = RED
            self.width, self.height = 20, 10
        elif mage_type == "water":
            self.color = BLUE
            self.width, self.height = 15, 15
        elif mage_type == "earth":
            self.color = GREEN
            self.width, self.height = 25, 25
        elif mage_type == "air":
            self.color = YELLOW
            self.width, self.height = 30, 8
            
        # Create the projectile image
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        
        # Set position and direction
        self.rect.center = (x, y)
        self.direction = direction
        self.speed = PROJECTILE_SPEED
        
    def update(self):
        # Move in the correct direction
        if self.direction == "right":
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed
            
        # Remove if off screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self, mage_type):
        super().__init__()
        self.mage_type = mage_type
        
        # Set properties based on mage type
        if mage_type == "fire":
            self.color = RED
            self.attack_type = "fire bolt"
        elif mage_type == "water":
            self.color = BLUE
            self.attack_type = "water blast"
        elif mage_type == "earth":
            self.color = GREEN
            self.attack_type = "boulder"
        elif mage_type == "air":
            self.color = YELLOW
            self.attack_type = "wind streak"
        
        # Create temporary sprite
        self.image = create_colored_surface(40, 60, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        
        # Movement attributes
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.facing_right = True
        self.kills = 0
    
    def update(self):
        # Apply gravity
        if not self.on_ground:
            self.velocity_y += GRAVITY
        
        # Update position
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Check boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        
        # Simple ground collision (temporary)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0
            self.on_ground = True
    
    def move_left(self):
        self.velocity_x = -PLAYER_SPEED
        self.facing_right = False
    
    def move_right(self):
        self.velocity_x = PLAYER_SPEED
        self.facing_right = True
    
    def stop(self):
        self.velocity_x = 0
    
    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_STRENGTH
            self.on_ground = False
    
    def shoot(self):
        # Create a new projectile
        direction = "right" if self.facing_right else "left"
        if self.facing_right:
            projectile = Projectile(self.rect.right, self.rect.centery, direction, self.mage_type)
        else:
            projectile = Projectile(self.rect.left, self.rect.centery, direction, self.mage_type)
            
        return projectile

# Character selection screen
def character_selection_screen():
    title_font = pygame.font.SysFont("Arial", 40)
    option_font = pygame.font.SysFont("Arial", 24)
    
    title_text = title_font.render("Select Your Mage", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
    
    mage_types = ["fire", "water", "earth", "air"]
    mage_colors = [RED, BLUE, GREEN, YELLOW]
    mage_names = ["Fire Mage", "Water Mage", "Earth Mage", "Air Mage"]
    
    mage_rects = []
    
    selected = None
    
    while selected is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, rect in enumerate(mage_rects):
                    if rect.collidepoint(pos):
                        selected = mage_types[i]
        
        screen.fill(BLACK)
        screen.blit(title_text, title_rect)
        
        # Draw mage options
        mage_rects = []
        for i, (mage_type, color, name) in enumerate(zip(mage_types, mage_colors, mage_names)):
            # Create rectangle for selection
            rect_x = 100 + i * 150
            rect_y = 200
            rect_width = 120
            rect_height = 180
            
            mage_rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
            mage_rects.append(mage_rect)
            
            # Draw mage preview
            pygame.draw.rect(screen, color, mage_rect)
            
            # Draw mage name
            name_text = option_font.render(name, True, WHITE)
            name_rect = name_text.get_rect(center=(rect_x + rect_width // 2, rect_y + rect_height + 30))
            screen.blit(name_text, name_rect)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    return selected

# Main game loop
def game_loop(player):
    # Game state
    game_over = False
    victory = False
    score = 0
    
    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    all_sprites.add(player)
    
    # Enemy spawning timer
    last_enemy_spawn = pygame.time.get_ticks()
    enemy_spawn_delay = ENEMY_SPAWN_RATE
    
    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if not game_over and not victory:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.move_left()
                    if event.key == pygame.K_RIGHT:
                        player.move_right()
                    if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                        player.jump()
                    if event.key == pygame.K_z:
                        new_projectile = player.shoot()
                        projectiles.add(new_projectile)
                        all_sprites.add(new_projectile)
                
                if event.type == pygame.KEYUP:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        player.stop()
        
        # Update
        # Update
        if not game_over and not victory:
            all_sprites.update()
            
            # Spawn enemies
            current_time = pygame.time.get_ticks()
            if current_time - last_enemy_spawn > enemy_spawn_delay:
                new_enemy = Enemy(SCREEN_WIDTH, SCREEN_HEIGHT, player)
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
                last_enemy_spawn = current_time
                
                # Gradually decrease spawn time as game progresses (to a minimum of 500ms)
                enemy_spawn_delay = max(500, ENEMY_SPAWN_RATE - player.kills * 50)
            
            # Check for collisions between player and enemies
            if pygame.sprite.spritecollide(player, enemies, False):
                game_over = True
                
            # Check for collisions between projectiles and enemies
            hits = pygame.sprite.groupcollide(projectiles, enemies, True, True)
            for hit in hits:
                player.kills += 1
                
            # Check for game over or victory
            if player.kills >= 20:
                victory = True
        # Draw
        screen.fill(BLACK)
        
        # Draw level (placeholder)
        pygame.draw.rect(screen, WHITE, [0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20])
        
        # Draw sprites
        all_sprites.draw(screen)
        
        # Draw UI
        font = pygame.font.SysFont("Arial", 20)
        kill_text = font.render(f"Enemies Defeated: {player.kills}/20", True, WHITE)
        screen.blit(kill_text, (10, 10))
        
        # Draw game over or victory message
        if game_over:
            message = font.render("Game Over! Press R to restart or Q to quit", True, RED)
            screen.blit(message, (SCREEN_WIDTH // 2 - message.get_width() // 2, SCREEN_HEIGHT // 2))
        
        if victory:
            message = font.render("Victory! Press R to restart or Q to quit", True, GREEN)
            screen.blit(message, (SCREEN_WIDTH // 2 - message.get_width() // 2, SCREEN_HEIGHT // 2))
        
        pygame.display.flip()
        clock.tick(FPS)
        
        # Handle game over or victory
        if game_over or victory:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                return "restart"
            elif keys[pygame.K_q]:
                return "quit"
    
    return "quit"

# Main game function
def main():
    running = True
    
    while running:
        # Start with character selection screen
        selected_mage = character_selection_screen()
        
        # Create player with selected mage type
        player = Player(selected_mage)
        
        # Start game loop
        result = game_loop(player)
        
        if result == "quit":
            running = False

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()

