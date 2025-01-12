import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("2D Fighting Game")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BUTTON_COLOR = (0, 255, 0)
BUTTON_HOVER_COLOR = (0, 200, 0)

# Define game variables
player_width = 50
player_height = 50
player_x = 100
player_y = 500
player_speed = 5
player_health = 100
enemy_width = 50
enemy_height = 50
enemy_x = 600
enemy_y = 500
enemy_speed = 2
enemy_health = 100
enemy_attack_range = 50
enemy_attack_cooldown = 1

# Set up fonts
font = pygame.font.SysFont(None, 36)
button_font = pygame.font.SysFont(None, 48)
winner_font = pygame.font.SysFont(None, 72, bold=True)

# Set up the clock
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((player_width, player_height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.speed = player_speed
        self.health = player_health
        self.attack_range = 50
        self.attack_cooldown = 1
        self.last_attack_time = time.time()

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def update_health(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def attack(self, enemy):
        current_time = time.time()
        if current_time - self.last_attack_time >= self.attack_cooldown:
            if abs(self.rect.x - enemy.rect.x) < self.attack_range and abs(self.rect.y - enemy.rect.y) < self.attack_range:
                enemy.update_health(10)  # Player damage
                self.last_attack_time = current_time

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((enemy_width, enemy_height))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = enemy_x
        self.rect.y = enemy_y
        self.speed = enemy_speed
        self.health = enemy_health
        self.last_attack_time = time.time()

    def move(self):
        if abs(self.rect.x - player.rect.x) > enemy_attack_range:
            if self.rect.x > player.rect.x:
                self.rect.x -= self.speed
            elif self.rect.x < player.rect.x:
                self.rect.x += self.speed

        if abs(self.rect.y - player.rect.y) > enemy_attack_range:
            if self.rect.y > player.rect.y:
                self.rect.y -= self.speed
            elif self.rect.y < player.rect.y:
                self.rect.y += self.speed

    def attack(self, player):
        current_time = time.time()
        if current_time - self.last_attack_time >= enemy_attack_cooldown:
            if abs(self.rect.x - player.rect.x) < enemy_attack_range and abs(self.rect.y - player.rect.y) < enemy_attack_range:
                player.update_health(10)  # Enemy damage
                self.last_attack_time = current_time

    def update_health(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

# Initialize player and enemy
player = Player()
enemy = Enemy()

# Create sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(enemy)

def draw_button(text, x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = button_font.render(text, True, BLACK)
    screen.blit(text_surface, (x + (width - text_surface.get_width()) // 2, y + (height - text_surface.get_height()) // 2))

def check_button_click(x, y, width, height, mouse_x, mouse_y):
    if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
        return True
    return False

def main_menu():
    while True:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        mouse_x, mouse_y = pygame.mouse.get_pos()
        draw_button("1v1", screen_width // 2 - 150, screen_height // 2 - 50, 300, 50, BUTTON_COLOR)
        draw_button("Quit", screen_width // 2 - 150, screen_height // 2 + 50, 300, 50, BUTTON_COLOR)

        if pygame.mouse.get_pressed()[0]:
            if check_button_click(screen_width // 2 - 150, screen_height // 2 - 50, 300, 50, mouse_x, mouse_y):
                start_1v1_mode()
            elif check_button_click(screen_width // 2 - 150, screen_height // 2 + 50, 300, 50, mouse_x, mouse_y):
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(60)

def start_1v1_mode():
    player.health = 100
    enemy.health = 100
    game_active = True
    while game_active:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move(0, -player.speed)
        if keys[pygame.K_s]:
            player.move(0, player.speed)
        if keys[pygame.K_a]:
            player.move(-player.speed, 0)
        if keys[pygame.K_d]:
            player.move(player.speed, 0)

        if pygame.mouse.get_pressed()[0]:
            player.attack(enemy)

        enemy.move()
        if abs(player.rect.x - enemy.rect.x) < 50 and abs(player.rect.y - enemy.rect.y) < 50:
            enemy.attack(player)

        all_sprites.update()
        all_sprites.draw(screen)

        player_health_text = font.render(f"Player Health: {player.health}", True, BLACK)
        enemy_health_text = font.render(f"Enemy Health: {enemy.health}", True, BLACK)
        screen.blit(player_health_text, (20, 20))
        screen.blit(enemy_health_text, (screen_width - enemy_health_text.get_width() - 20, 20))

        pygame.display.flip()

        if player.health <= 0:
            show_end_screen("Game Over")
            game_active = False
        elif enemy.health <= 0:
            show_end_screen("You Won!")
            game_active = False

        clock.tick(60)

def show_end_screen(message):
    end_screen_text = winner_font.render(message, True, GREEN if message == "You Won!" else RED)
    screen.blit(end_screen_text, (screen_width // 2 - end_screen_text.get_width() // 2, screen_height // 2 - end_screen_text.get_height() // 2))
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if check_button_click(screen_width // 2 - 150, screen_height // 2 + 50, 300, 50, mouse_x, mouse_y):
                    start_1v1_mode()
                    waiting_for_input = False
                elif check_button_click(screen_width // 2 - 150, screen_height // 2 + 150, 300, 50, mouse_x, mouse_y):
                    pygame.quit()
                    sys.exit()

        draw_button("Play Again", screen_width // 2 - 150, screen_height // 2 + 50, 300, 50, BUTTON_COLOR)
        draw_button("Quit", screen_width // 2 - 150, screen_height // 2 + 150, 300, 50, BUTTON_COLOR)
        pygame.display.flip()

main_menu()
