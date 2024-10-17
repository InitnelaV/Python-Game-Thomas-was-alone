import pygame
import sys

# Initialisation Pygame
pygame.init()

# Dimensions de la fenêtre du jeu
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Thomas Was not Alone - Code structure")

# Couleurs
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
PINK = (255, 105, 180)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Vitesse des protagonistes
speed_slow = 2
speed_fast = 4
gravity = 0.8
jump_strength = -12

# Définition des protagonistes
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, speed):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.vel_y = 0
        self.is_jumping = False

    def move(self, platforms, other_characters):
        keys = pygame.key.get_pressed()

        # Mouvement gauche/droite
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if self.check_collision(platforms + other_characters):
                self.rect.x += self.speed

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            if self.check_collision(platforms + other_characters):
                self.rect.x -= self.speed

        # Saut
        if not self.is_jumping:
            if keys[pygame.K_UP]:
                self.is_jumping = True
                self.vel_y = jump_strength

        # Gravité
        self.vel_y += gravity
        self.rect.y += self.vel_y

        # Gérer les collisions
        if self.check_collision(platforms + other_characters):
            self.rect.y -= self.vel_y
            self.vel_y = 0
            self.is_jumping = False

        # Pour ne pas glitcher  sous le sol
        if self.rect.bottom > HEIGHT - 50:
            self.rect.bottom = HEIGHT - 50
            self.is_jumping = False

    def check_collision(self, objects):
        for obj in objects:
            if self.rect.colliderect(obj.rect):
                return True
        return False

# Protagonistes
blue_square = Player(100, HEIGHT - 100, 100, 100, BLUE, speed_slow)
orange_square = Player(250, HEIGHT - 100, 50, 50, ORANGE, speed_fast)
pink_rectangle = Player(350, HEIGHT - 100, 30, 60, PINK, speed_fast)
yellow_rectangle = Player(450, HEIGHT - 100, 30, 120, YELLOW, speed_slow)

# Grouper les protagonistes
all_sprites = pygame.sprite.Group()
all_sprites.add(blue_square, orange_square, pink_rectangle, yellow_rectangle)

# Liste des protagonistes
characters = [blue_square, orange_square, pink_rectangle, yellow_rectangle]
current_character = 0  # On commence avec le premier personnage (gros carré bleu)

# Plateforme et escaliers
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((100, 100, 100))  # Couleur plateforme par défaut
        self.rect = self.image.get_rect(topleft=(x, y))

# Plateforme principale
platform = Platform(0, HEIGHT - 50, WIDTH, 50)

# Escalier à droite
stairs = [Platform(WIDTH - 200 + i*40, HEIGHT - 50 - i*40, 40, 40) for i in range(5)]

# Grouper les plateformes
platforms = [platform] + stairs
all_platforms = pygame.sprite.Group(platforms)

# Boucle principale du jeu
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Switcher au personnage suivant
                current_character = (current_character + 1) % len(characters)

    # Fond d'ecran par defaut
    screen.fill(WHITE)

    # Draw des plateformes
    all_platforms.draw(screen)

    # Draw et update du protagoniste selectionné
    all_sprites.update()
    all_sprites.draw(screen)

    # Liste des autres protagonistes PEC pour la collision
    other_characters = [char for i, char in enumerate(characters) if i != current_character]

    # Move du protagoniste sélectionné
    characters[current_character].move(platforms, other_characters)

    # Rafraîchir l'écran
    pygame.display.flip()

    # Contrôle de la vitesse de la boucle
    clock.tick(60)

# Quitter Pygame
pygame.quit()
sys.exit()
