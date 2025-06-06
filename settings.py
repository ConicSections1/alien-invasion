class Settings():
    '''A class to store all settings of alien invasion.'''

    def __init__(self):
        '''Initializing the game's static settings.'''

        #screen settings
        self.screen_height = 800
        self.screen_width = 1200
        self.bg_color = (230,230,230)

        # Ship settings
        self.ship_limit = 3

        # Bullet Settings
        self.bullet_width = 10
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 6

        # Alien Settings
        self.fleet_drop_speed = 15

        #Speed up settings
        self.speedup_scale = 1.1
        #How quickly the alien point value increases
        self.score_scale =1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''Initialize settings that change throughout the game'''
        self.ship_speed_factor = 0.5
        self.bullet_speed_factor = 2
        self.alien_speed_factor = 0.5
        # Fleet direction of 1 represents right -1 represents left
        self.fleet_direction = 1
        #Scoring
        self.alien_points = 50

    def increase_speed(self):
        '''Increase speed settings and alien points'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points *self.score_scale)