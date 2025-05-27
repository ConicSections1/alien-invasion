import pygame

class Ship:
    def __init__(self, ai_settings ,screen):
        '''Initialize the ship and set its starting position'''
        self.screen=screen
        self.ai_settings = ai_settings

        #load the image and get its rectangle
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #Start each new ship at the bottom of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's center
        self.center = float(self.rect.centerx)

        # Movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        '''Update the ship's position based on the movement flag'''
        #Update the ship's center value, not the rect.
        if self.moving_left:
            if (self.center >= 10):
                self.center-=self.ai_settings.ship_speed_factor

        if self.moving_right:
            if (self.center <= 1190):
                self.center+=self.ai_settings.ship_speed_factor
        #Update rect object from self.center
        self.rect.centerx = self.center

    def center_ship(self):
        '''Center the ship on the screen'''
        self.center = self.screen_rect.centerx

    def blitme(self):
        '''Draw the ship at its current location'''
        self.screen.blit(self.image, self.rect) 