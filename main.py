import pygame
from pygame.locals import *
import random
import game_objects
import file_io

# Initialise the game
pygame.init()

# Sets the FPS of the game
FPS = 30
fpsclock = pygame.time.Clock()

# Create the screen object
screen = pygame.display.set_mode((1280, 720))
display_info = pygame.display.Info()
display_size = {
    "display_w" : display_info.current_w,
    "display_h" : display_info.current_h
}
# Sets the background to be blue
background = pygame.image.load('images/background.png').convert()
# background = pygame.Surface(screen.get_size())
# background.fill((135, 206, 250))
# Instantiates the text settings
text = game_objects.TextSurface

# Create a custom event to add an enemy + cloud
ADDENEMY = pygame.USEREVENT + 1
ADDCLOUD = pygame.USEREVENT + 2
# And create the event so it can be listened for every 250 miliseconds
pygame.time.set_timer(ADDENEMY, 250)
pygame.time.set_timer(ADDCLOUD, 1000)


# Instantiate the player
player = game_objects.Player(display_size)
# Creating sprite groups to store the game sprites
# Stores enemies
enemies = pygame.sprite.Group()
# Stores clouds
clouds = pygame.sprite.Group()
# This seprates the clouds to make sure they are drawn first
player_and_enemies = pygame.sprite.Group()
# Add the player to the group
player_and_enemies.add(player)


# Variable to keep the game running
# And to track if player is alive
# Get score is used to it doenst save the scores multiple times
running = True
alive = True
get_score = False

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
                game_objects.Enemy.score = 0
                # Re-create the player, add them to the group, and set them to alive
                player = game_objects.Player(display_size)
                player_and_enemies.add(player)
                alive = True
        # Check for quit event
        elif event.type == QUIT:
            runnig = False
        # Checks for the event to create an Enemy
        elif(event.type == ADDENEMY):
            # Creates the enemy from the class
            new_enemy = game_objects.Enemy(display_size)
            # Adds it to the enemy sprite group
            enemies.add(new_enemy)
            # Adds it to the player and enemy sprite group
            player_and_enemies.add(new_enemy)
        # Checks the event to create a cloud
        elif(event.type == ADDCLOUD):
            # Creates and adds to the cloud group
            new_cloud = game_objects.Cloud(display_size)
            clouds.add(new_cloud)


    # Loads the background
    screen.blit(background, (0, 0))
    # This draws all sprites on to the screen
    # Making sure clouds are drawn first
    for entity in clouds:
        screen.blit(entity.image, entity.rect)
    for entity in player_and_enemies:
        screen.blit(entity.image, entity.rect)
    # Loads the score counter
    screen.blit(text.score(str(game_objects.Enemy.score)),(0, 0))
    # Loads the Ecs to exit text
    screen.blit(text.exit(),((display_size["display_w"] - 260), 0))



    # Adds a message saying press space to restart if the player is dead
    while get_score:
        file_io.save_score(game_objects.Enemy.score)
        top_scores = file_io.load_scores()
        get_score = False

    if alive == False:
        screen.blit(text.restart(),((display_size["display_w"] / 2 - 180), ((display_size["display_h"] / 100) * 20)))
        screen.blit(text.top_scores_text(),((display_size["display_w"] / 2 - 80), ((display_size["display_h"] / 100) * 31)))
        top_scores = file_io.load_scores()
        counter = 0
        for score in top_scores:
            screen.blit(text.top_scores_number(score), ((display_size["display_w"] / 2 - 10), ((display_size["display_h"] / 100) * 43 + (40 * counter))))
            counter += 1

    # This gets the key press and passes to the player class
    if alive:
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys, display_size)
        # The the enemies and player collide, kill the player
        # Also adds the score to the score file
        if pygame.sprite.spritecollideany(player, enemies):
            player.kill()
            del player
            alive = False
            get_score = True

    # Moves the enemies
    enemies.update(alive)
    clouds.update()

    # This updates the screen so its actaully shown
    pygame.display.flip()

    # This ticks the FPS clock
    fpsclock.tick(FPS)
