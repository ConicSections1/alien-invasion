import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep
import json

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Respond to the ship being hit by an alien'''
    if stats.ships_left > 0:
        #Decrement ships left
        stats.ships_left-=1

        #Update scoreboard
        sb.prep_ships()
        #Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()
        #Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens, bullets)
        ship.center_ship()
        #pause
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def update_aliens(ai_settings, screen,stats,sb, ship, aliens, bullets):
    '''Update the positions of all aliens in the fleet'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #Look out for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
        return
    
    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def get_number_rows(ai_settings, ship_height, alien_height):
    '''Determine the number of rows of aliens'''
    available_space_y = (ai_settings.screen_height-(3*alien_height)-ship_height)
    number_rows = int(available_space_y/(2*alien_height))
    return number_rows

def get_number_aliens_x(ai_settings, alien_width):
    '''Determine the number of aliens that fit in a row'''
    available_space_x = ai_settings.screen_width -2*alien_width
    number_aliens_x = int(available_space_x / (2*alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    '''Create an alien and place it in a row'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2*alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens, bullets):
    '''Create a full fleet of aliens'''
    bullets.empty()  # Empty the bullets group to start fresh
    #Create an alien to find the number of aliens in a row
    #Spacing between each alien is equal to one alien width
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    
    #Create the fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    '''Respond to keypresses and mouse events'''
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            stats.reset_stats()
            ai_settings.initialize_dynamic_settings()
            save_stats(stats)
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
            
        
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        
def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    '''Start a new game when the player hits the play button'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #Reset game settings
        ai_settings.initialize_dynamic_settings()
        #Hide the mouse cursor
        pygame.mouse.set_visible(False)
        #reset the game statistics
        stats.reset_stats()
        stats.game_active = True

        #Reset the scoreboard images
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #Empty the list of bullets and aliens
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens, bullets)
        ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    '''Update images on the screen and flip to the new screen'''
    #Redraw the screen
    screen.fill(ai_settings.bg_color)
    #Redraw all bullets
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    #Draw the score information
    sb.show_score()

    #Draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()

    #Make recently drawn screen visible    
    pygame.display.flip()

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    '''Respond to presses'''
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        #Move the ship to the right
        ship.moving_right = True

    #Move the ship to the left
    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.moving_left = True
    
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)

    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event,ship):
    '''Respond to key releases'''
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        #Stop moving the ship to the right
        ship.moving_right = False

    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
        #Stop moving the ship to the left
        ship.moving_left = False

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''Update position of bullets and get rid of old bullets'''
    # Update bullet positions
    bullets.update()

    check_collision(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # Get rid of bullets that have disappeared
    for bullet in bullets.copy():
        if (bullet.rect.bottom<=0):
            bullets.remove(bullet)


def check_collision(ai_settings, screen, stats, sb, ship, aliens, bullets):
    #Check for collisions
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for alien in collisions.values():
            stats.score += ai_settings.alien_points
            sb.prep_score()
        check_high_score(stats, sb)
    
    if len(aliens) == 0:
        #destroy existing bullets, speedup game and create new fleet
        bullets.empty()
        ai_settings.increase_speed()

        #Increase Level
        stats.level +=1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens, bullets)


def fire_bullet(ai_settings, screen, ship, bullets):
    '''Fire a bullet if limit has not been reached'''
    #Create a new bullet and add it to the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_fleet_edges(ai_settings, aliens):
    '''Respond appropriately if any aliens have reached an edge'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    '''Drop the entire fleet and change fleet's direction'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_high_score(stats, sb):
    '''Check to see if there's a new high score'''
    if stats.score>stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def save_stats(stats):
    '''Save the stats to a file'''
    with open('high_score.json', 'w') as f:
        json.dump(stats.high_score, f)

def load_stats(stats):
    '''Load the stats from a file'''
    try:
        with open('high_score.json', 'r') as f:
            stats.high_score = json.load(f)
    except FileNotFoundError:
        stats.high_score = 0
    except json.JSONDecodeError:
        stats.high_score = 0


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
 
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
         if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break