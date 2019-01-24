import pygame
from pygame.locals import *
import random
from gamelib import game_objects
from gamelib import file_io

def main():
    # Initialise the game
    pygame.init()

    # Sets the FPS of the game
    FPS = 30
    fpsclock = pygame.time.Clock()

    # Create the game window
    screen = pygame.display.set_mode((1280, 720))
    # Gets the windows size to be used to ensure things stay in the window / where they can spawn
    display_info = pygame.display.Info()
    display_size = {
        "display_w" : display_info.current_w,
        "display_h" : display_info.current_h
    }

    # Sets the background
    background = pygame.image.load('images/background1.png').convert()

    # Set the game icon and name
    pygame.display.set_icon(pygame.image.load('images/game_icon.png'))
    pygame.display.set_caption('Bat Out of Hell')

    # Instantiates the text settings
    text = game_objects.TextSurface

    # Create a custom event to add an enemy + cloud
    ADDENEMY = pygame.USEREVENT + 1
    ADDCLOUD = pygame.USEREVENT + 2
    ADDGEM = pygame.USEREVENT + 3
    ADDWATER = pygame.USEREVENT + 4
    pygame.time.set_timer(ADDCLOUD, 1000)
    pygame.time.set_timer(ADDGEM, 4000)
    pygame.time.set_timer(ADDWATER, 10000)


    # Instantiate the player
    player = game_objects.Player(display_size)
    # Creating sprite groups to store the game sprites
    # Stores enemies
    enemies = pygame.sprite.Group()
    # Stores clouds
    clouds = pygame.sprite.Group()
    # Group for the gems
    gems = pygame.sprite.Group()
    # Groups for hearts
    hearts = pygame.sprite.Group()
    # Group for water
    water_drops = pygame.sprite.Group()
    # Start text
    startup = pygame.sprite.Group()
    # This seprates the clouds to make sure they are drawn first
    all_but_clouds = pygame.sprite.Group()



    # Variable to keep the game running
    # And to track if player is alive
    # Get score is used so it doesn't save the scores multiple times
    running = True
    alive = False
    get_score = False
    level_up = True
    # Used to diferentiate between start up screen and when the game starts
    start_game = False
    # Used to add the start up text to a group
    start_up = True
    help_screen = True


    # Game Loop
    while running:
        for event in pygame.event.get():
            # Check for keypress event
            if event.type == KEYDOWN:
                # Check is esc key was pressed
                # And if it is, quit the game
                if event.key == K_ESCAPE:
                    running = False
                # On pressing enter, it will give game info. If you haven't starter and you press it again
                # it will take you back to the start screen
                # If you have started, it will return you to the game
                elif event.key == K_RETURN:
                    for sprite in startup:
                        sprite.kill()
                        del sprite
                    if help_screen:
                        new_help_screen = game_objects.HelpScreen(display_size)
                        startup.add(new_help_screen)
                        help_screen = False
                    else:
                        help_screen = True
                        if start_game == False:
                            startup_text = game_objects.StartText(display_size)
                            startup.add(startup_text)
                # Check if space was pressed
                elif event.key == K_SPACE:
                    # If it is, remove player and enemy sprites
                    for sprite in all_but_clouds:
                        sprite.kill()
                        del sprite
                    # Set the score back to 0
                    game_objects.Enemy.score = 0
                    game_objects.Water.lives = 1
                    # Re-create the player, add them to the group, and set them to alive
                    player = game_objects.Player(display_size)
                    all_but_clouds.add(player)
                    for sprite in startup:
                        sprite.kill()
                        del sprite
                    alive = True
                    # Set the var to start_game
                    start_game = True
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
                all_but_clouds.add(new_enemy)
            # Checks the event to create a cloud
            elif(event.type == ADDCLOUD):
                # Creates and adds to the cloud group
                new_cloud = game_objects.Cloud(display_size)
                clouds.add(new_cloud)
            elif(event.type == ADDGEM):
                # Creates and adds to the gem group
                new_gem = game_objects.Gem(display_size)
                gems.add(new_gem)
                all_but_clouds.add(new_gem)
            elif(event.type == ADDWATER):
                # Creates and adds to water group
                new_water = game_objects.Water(display_size)
                water_drops.add(new_water)
                all_but_clouds.add(new_water)


        # This run when the game starts_up
        if alive == False and start_up:
            startup_text = game_objects.StartText(display_size)
            startup.add(startup_text)
            start_up = False

        # Increase the amount of bullets as you get more points
        while level_up:
            if game_objects.Enemy.score <= 100:
                pygame.time.set_timer(ADDENEMY, 250)
                level_up = False
            elif game_objects.Enemy.score >= 101 and game_objects.Enemy.score <= 500:
                pygame.time.set_timer(ADDENEMY, 200)
                level_up = False
            elif game_objects.Enemy.score > 500:
                pygame.time.set_timer(ADDENEMY, 150)
                level_up = False

        if game_objects.Enemy.score == 101:
            level_up = True
        elif game_objects.Enemy.score == 501:
            level_up = True



        # Draws the background
        screen.blit(background, (0, 0))
        # This draws all sprites on to the screen
        # Making sure clouds are drawn first
        clouds.draw(screen)
        if start_game:
            all_but_clouds.draw(screen)
            # Draws the score counter
            screen.blit(text.score(str(game_objects.Enemy.score)),(13, 50))
            # Draws the life counter
            screen.blit(text.life_counter(), (13, 5))
            # Draws the Ecs to exit text
            screen.blit(text.exit(),((display_size["display_w"] - 260), 5))
            # Draws the life heart on the screen
            # And increases and decreases when you get life / get
            for x in range(0 + game_objects.Water.lives):
                heart = game_objects.Heart((x + 1) * 25, True)
                screen.blit(heart.image, heart.rect)
                health_range = x + 1
            for x in range(10 - game_objects.Water.lives):
                heart = game_objects.Heart((health_range + x + 1) * 25, False)
                screen.blit(heart.image, heart.rect)
        startup.draw(screen)

        # Saves the score, then set to false to it doesn't run again
        while get_score:
            file_io.save_score(game_objects.Enemy.score)
            get_score = False

        # When the player dies, adds test to say press space to restart
        # And displays the scores, up to a max of 5
        if alive == False and start_game == True:
            screen.blit(text.restart(),((display_size["display_w"] / 2 - 180), ((display_size["display_h"] / 100) * 20)))
            screen.blit(text.top_scores_text(),((display_size["display_w"] / 2 - 80), ((display_size["display_h"] / 100) * 31)))
            top_scores = file_io.load_scores()
            counter = 0
            for score in top_scores:
                screen.blit(text.top_scores_number(score), ((display_size["display_w"] / 2 - 45), ((display_size["display_h"] / 100) * 43 + (40 * counter))))
                counter += 1

        # This gets the key press and passes to the player class
        if alive:
            pressed_keys = pygame.key.get_pressed()
            player.update(pressed_keys, display_size)
            # The the enemies and player collide, kill the player
            # and set get_score to true so that while loop activates
            if pygame.sprite.spritecollide(player, gems, False):
                for gem in pygame.sprite.spritecollide(player, gems, False):
                    if gem.name == "gem1":
                        game_objects.Enemy.score += 2
                    elif gem.name == "gem2":
                        game_objects.Enemy.score += 4
                    elif gem.name == "gem3":
                        game_objects.Enemy.score += 6
                    elif gem.name == "gem4":
                        game_objects.Enemy.score += 10
                    elif gem.name == "gem5":
                        game_objects.Enemy.score += 25
                gem.kill()
                del gem

            # Colision logic for the water
            if pygame.sprite.spritecollideany(player, water_drops):
                for water in pygame.sprite.spritecollide(player, water_drops, False):
                    if game_objects.Water.lives < 10:
                        game_objects.Water.lives += 1
                    hearts.empty()
                    water.kill()
                    del water
            # Colisio logic for the fire
            if pygame.sprite.spritecollideany(player, enemies):
                game_objects.Water.lives -= 1
                hearts.empty()
                for enemy in pygame.sprite.spritecollide(player, enemies, False):
                    enemy.kill()
                    del enemy
                if game_objects.Water.lives <= 0:
                    player.kill()
                    del player
                    alive = False
                    get_score = True

        # Moves the sprites (except player)
        enemies.update(alive)
        clouds.update()
        gems.update()
        water_drops.update()
        startup.update()

        # This updates the screen so its actaully shown
        pygame.display.flip()

        # This ticks the FPS clock
        fpsclock.tick(FPS)
