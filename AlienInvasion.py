import sys
import pygame
from settings import Settings

class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    
    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.screen = pygame.display.set_mode(self.settings.screen_width, self.settings.screen_height)
        pygame.display.set_caption("Alien Invasion")
        
        #Set background color
        self.bg_color = (0, 0, 255)
        
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.screen.fill(self.bg_color)
            pygame.display.flip()
            

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()