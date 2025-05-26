import pygame
from settings import Settings   #Settings class from settings module
from ship import Ship #Ship class from ship module
import game_functions as gf
from pygame.sprite import Group
from alien import Alien

def run_game():
    #initialize game create a screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make ship
    ship = Ship(ai_settings,screen)
    #Make a group to store the live bullets
    bullets = Group()
    #Make an alien
    alien = Alien(ai_settings, screen)

    #Game Loop
    while True:
        # Watch for keyboard and mouse events
        gf.check_events(ai_settings, screen, ship, bullets)
        ship.update()
        gf.update_bullets(bullets)
        gf.update_screen(ai_settings, screen, ship, alien, bullets)
        
run_game()