class GameStats():
    '''Statisitcs for the game'''
    def __init__(self, ai_settings):
        '''Initialize statistics'''
        self.ai_settings = ai_settings
        self.reset_stats()

        #Start game in an inactive state
        self.game_active = False
        #High score should be static
        self.high_score = 0



    def reset_stats(self):
        '''Initialize the statistics that can change during the game'''
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1