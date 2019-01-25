import pygame
from pygame.locals import *
import random
from gamelib import file_io

# Used to animate sprites
def animator(object, value):
    if object.counter % value == 0:
        object.index += 1
        if object.index >= len(object.images):
            object.index = 0
        object.image = object.images[object.index]
        object.image.set_colorkey((255, 255, 255), RLEACCEL)
        object.counter += 1
    else:
        object.counter += 1
    if object.counter >= 100:
        object.counter = 0

class Player(pygame.sprite.Sprite):
    def __init__(self, display_size):
        super(Player, self).__init__()
        # Loads the sprite images
        self.images = []
        ss = file_io.Spritesheet('images/bat_spritesheet.png')
        self.images = ss.load_strip((0, 0, 39, 48), 4, colorkey=(255, 255, 255))
        self.index = 0
        self.counter = 0
        # Sets it to the first image
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(0, (display_size["display_h"] / 2)))

    # These are the keys to move the player
    def update(self, pressed_keys, display_size):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -10)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 10)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-10, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(10, 0)

        # Changes the sprite image
        # Will do it at a third of the FPS clock
        animator(self, 3)

        # Keep the player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > display_size["display_w"]:
            self.rect.right = display_size["display_w"]
        if self.rect.top <= 0:
            self.rect.top = 0
        elif self.rect.bottom >= display_size["display_h"]:
            self.rect.bottom = display_size["display_h"]

class Enemy(pygame.sprite.Sprite):
    # Keeps track of player score
    score = 0

    def __init__(self, display_size):
        super(Enemy, self).__init__()
        # Loads the sprite images
        self.images = []
        ss = file_io.Spritesheet('images/fireball_spritesheet.png')
        self.images = ss.load_strip((0, 0, 48, 32), 6, colorkey=(255, 255, 255))
        self.index = 0
        self.counter = 0
        # Sets the first image
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(display_size["display_w"] + 50, random.randint(0, display_size["display_h"])))
        self.speed = random.randint(5, 20)

    def update(self, alive):
        # Changes the sprite image
        # Will do it at a quater of the FPS clock
        animator(self, 4)

        # Will move toward the left, when it hits the left, it will increase the score by 1
        # if the player is alive
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
            alive = alive
            if alive:
                Enemy.score += 1

class Cloud(pygame.sprite.Sprite):
    def __init__(self, display_size):
        super(Cloud, self).__init__()
        # Sets the cloud sprites
        self.images = []
        for x in range(1, 7):
            self.images.append(pygame.image.load('images/cloud' + str(x) + '.png').convert())
        # Will pick an image at random to spawn
        self.image = self.images[random.randint(0, len(self.images)-1)]
        self.image.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.image.get_rect(center=(display_size["display_w"] + 150, random.randint(0, display_size["display_h"])))

    # Moved the cloud
    def update(self):
        self.rect.move_ip(-7, 0)
        if self.rect.right < 0:
            self.kill()

class Water(pygame.sprite.Sprite):
    # Keeps track of lives
    lives = 1

    def __init__(self, display_size):
        super(Water, self).__init__()
        self.image = pygame.image.load('images/water.png').convert()
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(center=(display_size["display_w"] + 50, random.randint(30, display_size["display_h"] - 30)))

    def update(self):
        self.rect.move_ip(-6, 0)
        if self.rect.right < 0:
            self.kill()

class Gem(pygame.sprite.Sprite):
    def __init__(self, display_size):
        super(Gem, self).__init__()
        # Sets the gem sprites
        self.images = []
        for x in range(1, 6):
            self.images.append(pygame.image.load('images/gem' + str(x) + '.png').convert())
        # Will pick an image at random to spawn
        weighted_list = [0] * 40 + [1] * 30 + [2] * 15 + [3] * 10 + [4] * 5
        choice = random.choice(weighted_list)
        # Sets the name of the gem so it can be used for different scores
        if choice == 0:
            self.name = "gem1"
        elif choice == 1:
            self.name = "gem2"
        elif choice == 2:
            self.name = "gem3"
        elif choice == 3:
            self.name = "gem4"
        elif choice == 4:
            self.name = "gem5"
        self.image = self.images[choice]
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(center=(display_size["display_w"] + 50, random.randint(30, display_size["display_h"] - 30)))
        self.speed = random.randint(5, 10)


    # Moves the gem
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Heart(pygame.sprite.Sprite):
    def __init__(self, x_value, full):
        super(Heart, self).__init__()
        self.images = []
        ss = file_io.Spritesheet('images/heart_spritesheet.png')
        self.images = ss.load_strip((0, 0, 30, 24), 2, colorkey=(255, 255, 255))
        if full:
            self.image = self.images[0]
        else:
            self.image = self.images[1]
        self.rect = self.image.get_rect(center=(0 + x_value, 40))

class StartText(pygame.sprite.Sprite):
    # Used for the start up screen
    def __init__(self, display_size):
        super(StartText, self).__init__()
        self.images = []
        ss = file_io.Spritesheet('images/start_text_spritesheet.png')
        self.images = ss.load_strip((0, 0, 884, 332), 2, colorkey=(255, 255, 255))
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(display_size["display_w"] / 2, display_size["display_h"] / 2))

    def update(self):
        animator(self, 16)

class HelpScreen(pygame.sprite.Sprite):
    # Used for the text at the start of the game.
    def __init__(self, display_size):
        super(HelpScreen, self).__init__()
        self.images = []
        ss = file_io.Spritesheet('images/help_screen_spritesheet.png')
        self.images = ss.load_strip((0, 0, 884, 625), 2, colorkey=(255, 255, 255))
        self.index = 0
        self.counter = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect(center=(display_size["display_w"] / 2, display_size["display_h"] / 2))

    def update(self):
        animator(self, 16)

# Used for the different messages
class TextSurface():
    pygame.font.init()
    myfont = pygame.font.SysFont('Consolas ', 25)

    def score(score):
        return TextSurface.myfont.render("Score: " + score, False, (0, 0, 0))

    def exit():
        return TextSurface.myfont.render("Press Esc to exit", False, (0, 0, 0))

    def restart():
        return TextSurface.myfont.render("Press space-bar to restart", False, (0, 0, 0))

    def top_scores_text():
        return TextSurface.myfont.render("Top Scores: ", False, (0, 0, 0))

    def top_scores_number(score):
        return TextSurface.myfont.render(f" {score}  ", False, (0, 0, 0))

    def life_counter():
        return TextSurface.myfont.render("Lives: ", False, (0, 0, 0))
