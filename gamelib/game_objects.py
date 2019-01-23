import pygame
from pygame.locals import *
import random


# Define the player and call super to give it the properties of pygame.sprite.Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self, display_size):
        super(Player, self).__init__()
        # Loads the sprite images
        self.images = []
        self.images.append(pygame.image.load('images/bat1.png').convert())
        self.images.append(pygame.image.load('images/bat2.png').convert())
        self.images.append(pygame.image.load('images/bat3.png').convert())
        self.images.append(pygame.image.load('images/bat4.png').convert())
        self.index = 0
        self.counter = 0
        # Sets it to the first image
        self.image = self.images[self.index]
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
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
        if self.counter % 3 == 0:
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            self.image.set_colorkey((255, 255, 255), RLEACCEL)
            self.counter += 1
        else:
            self.counter += 1
        if self.counter >= 9:
            self.counter = 0

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
        self.images.append(pygame.image.load('images/fireball1.png').convert())
        self.images.append(pygame.image.load('images/fireball2.png').convert())
        self.images.append(pygame.image.load('images/fireball3.png').convert())
        self.images.append(pygame.image.load('images/fireball4.png').convert())
        self.images.append(pygame.image.load('images/fireball5.png').convert())
        self.images.append(pygame.image.load('images/fireball6.png').convert())
        self.index = 0
        self.counter = 0
        # Sets the first image
        self.image = self.images[self.index]
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(center=(display_size["display_w"] + 50, random.randint(0, display_size["display_h"])))
        self.speed = random.randint(5, 20)

    def update(self, alive):
        # Changes the sprite image
        # Will do it at a quater of the FPS clock
        if self.counter % 4 == 0:
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]
            self.image.set_colorkey((255, 255, 255), RLEACCEL)
            self.counter += 1
        else:
            self.counter += 1
        if self.counter >= 8:
            self.counter = 0

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
        self.images.append(pygame.image.load('images/cloud1.png').convert())
        self.images.append(pygame.image.load('images/cloud2.png').convert())
        self.images.append(pygame.image.load('images/cloud3.png').convert())
        self.images.append(pygame.image.load('images/cloud4.png').convert())
        self.images.append(pygame.image.load('images/cloud5.png').convert())
        self.images.append(pygame.image.load('images/cloud6.png').convert())
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
        self.images.append(pygame.image.load('images/gem1.png').convert())
        self.images.append(pygame.image.load('images/gem2.png').convert())
        self.images.append(pygame.image.load('images/gem3.png').convert())
        self.images.append(pygame.image.load('images/gem4.png').convert())
        self.images.append(pygame.image.load('images/gem5.png').convert())
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
        self.images.append(pygame.image.load('images/heart_full.png').convert())
        self.images.append(pygame.image.load('images/heart_empty.png').convert())
        if full:
            self.image = self.images[0]
        else:
            self.image = self.images[1]
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(center=(0 + x_value, 40))

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
