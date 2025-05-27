import pygame
from settings import Settings   #Settings class from settings module
from ship import Ship #Ship class from ship module
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats #Game_stats class from game_stats module

def run_game():
    #initialize game create a screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #Create an instance to store gam statistics
    stats = GameStats(ai_settings)

    # Make ship group of bullets and group of aliens
    ship = Ship(ai_settings,screen)
    bullets = Group()
    aliens = Group()

    #create fleet of aliens
    gf.create_fleet(ai_settings, screen,ship, aliens)

    #Game Loop
    while True:
        # Watch for keyboard and mouse events
        gf.check_events(ai_settings, screen, ship, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings,stats, screen, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)
        
        
run_game() 