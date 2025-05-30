import pygame
from settings import Settings   #Settings class from settings module
from ship import Ship #Ship class from ship module
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats #Game_stats class from game_stats module
from button import Button
from scoreboard import Scoreboard

def run_game():
    #initialize game create a screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    #Make the play button
    play_button = Button(ai_settings, screen, "Play")

    #Create an instance to store game statistics and create a scoreboard
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    gf.load_stats(stats)  # Load saved stats if available

    # Make ship group of bullets and group of aliens
    ship = Ship(ai_settings,screen)
    bullets = Group()
    aliens = Group()

    #create fleet of aliens
    gf.create_fleet(ai_settings, screen,ship, aliens, bullets  )

    #Game Loop
    while True:
        # Watch for keyboard and mouse events
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb,   ship, aliens, bullets)
            gf.update_aliens(ai_settings,screen, stats, sb, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)
        
        
run_game() 