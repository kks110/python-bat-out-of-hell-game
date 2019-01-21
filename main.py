import pygame
from pygame.locals import *
import random

# Sets the FPS of the game
FPS = 60
fpsclock = pygame.time.Clock()

# Define the player and call super to give it the properties of pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # Loads the image, sets the background colour
        self.image = pygame.image.load('jet.png').convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(center=(0, 270))

    # These are the keys to move the player
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Keep the player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= 600:
            self.rect.bottom = 600

class Enemy(pygame.sprite.Sprite):
    # Keeps track of player score
    score = 0

    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.image.load('missile.png').convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(center=(1000, random.randint(0, 540)))
        self.speed = random.randint(5, 20)

    def update(self):
        # Will move toward the left, when it hits the left, it will increase the score by 1
        # if the player is alive
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            if alive:
                Enemy.score += 1

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.image = pygame.image.load('cloud.png').convert()
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect(center=(1000, random.randint(0, 540)))

    def update(self):
        self.rect.move_ip(-8, 0)
        if self.rect.right < 0:
            self.kill()

# Initialise the game
pygame.init()
pygame.font.init()

# Sets the game font
myfont = pygame.font.SysFont('Arial ', 40)

# Create the screen object
screen = pygame.display.set_mode((960, 540))

# Create a custom event to add an enemy + cloud
ADDENEMY = pygame.USEREVENT + 1
ADDCLOUD = pygame.USEREVENT + 2

# And create the event so it can be listened for every 250 miliseconds
pygame.time.set_timer(ADDENEMY, 250)
pygame.time.set_timer(ADDCLOUD, 1000)

# Instantiate the player
player = Player()

# Sets the background to be blue
background = pygame.Surface(screen.get_size())
background.fill((135, 206, 250))

# Creating sprite groups to store the game sprites
# Stores enemies
enemies = pygame.sprite.Group()
# Stores clouds
clouds = pygame.sprite.Group()
# Stores enemies and cloues
# This seprates the clouds to make sure they are drawn first
player_and_enemies = pygame.sprite.Group()
# Add the player to the group
player_and_enemies.add(player)



# Variable to keep the game running
# And to track if player is alive
running = True
alive = True

# Game Loop
while running:
    for event in pygame.event.get():
        # Check for keypress event
        if event.type == KEYDOWN:
            # Check is esc key was pressed
            # And if it is, quit the game
            if event.key == K_ESCAPE:
                running = False
            # Check if space was pressed
            elif event.key == K_SPACE:
                # If it is, remove player and enemy sprites
                for sprite in player_and_enemies:
                    sprite.kill()
                # Set the score back to 0
                Enemy.score = 0
                # Re-create the player, add them to the group, and set them to alive
                player = Player()
                player_and_enemies.add(player)
                alive = True
        # Check for quit event
        elif event.type == QUIT:
            runnig = False
        # Checks for the event to create an Enemy
        elif(event.type == ADDENEMY):
            # Creates the enemy from the class
            new_enemy = Enemy()
            # Adds it to the enemy sprite group
            enemies.add(new_enemy)
            # Adds it to the player and enemy sprite group
            player_and_enemies.add(new_enemy)
        # Checks the event to create a cloud
        elif(event.type == ADDCLOUD):
            # Creates and adds to the cloud group
            new_cloud = Cloud()
            clouds.add(new_cloud)


    # Loads the background again, otherwise the player paints the screen
    screen.blit(background, (0, 0))

    # Loads the score counter
    textsurface_score = myfont.render("Score: " + str(Enemy.score), False, (0, 0, 0))
    screen.blit(textsurface_score,(0, 0))
    # Loads the Ecs to exit text
    textsurface_exit = myfont.render("Press Esc to exit", False, (0, 0, 0))
    screen.blit(textsurface_exit,(700, 0))

    # Adds a message saying press space to restart if the player is dead
    if alive == False:
        textsurface_restart = myfont.render("Press space-bar to restart", False, (0, 0, 0))
        screen.blit(textsurface_restart,(300, 230))

    # This gets the key press and passes to the player class
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Moves the enemies
    enemies.update()
    clouds.update()

    # This draws all sprites on to the screen
    # Making sure clouds are drawn first
    for entity in clouds:
        screen.blit(entity.image, entity.rect)
    for entity in player_and_enemies:
        screen.blit(entity.image, entity.rect)

    # The the enemies and player collide, kill the player
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        alive = False

    # This updates the screen so its actaully shown
    pygame.display.flip()

    # This ticks the FPS clock
    fpsclock.tick(FPS)
