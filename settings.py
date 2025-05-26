class Settings():
    '''A class to store all settings of alien invasion.'''

    def __init__(self):
        '''Initializing the game's setting.'''

        #screen settings
        self.screen_height = 800
        self.screen_width = 1200
        self.bg_color = (230,230,230)

        # Ship settings
        self.ship_speed_factor = 0.5

        # Bullet Settings
        self.bullet_speed_factor = 0.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3