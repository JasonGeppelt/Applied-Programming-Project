# GAME
# Manages the overall game flow, including starting and ending the game,
# and handling transitions between game states (e.g., menus, gameplay, game over).

import pygame
import sys
from settings_manager import screen_height, screen_width, Colors, health, money
from level import maze
from enemy import Enemy
from tower import Tower
from grid_cell import GridCell

class Game:
    def __init__(self):
        """Initialize the game."""
        pygame.init()

        self.maze = maze  # Store the maze
        self.path = [(x * 20 + 10, 10) for x in range(10)]  # Define the path for the enemy

        # Screen properties
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Tower Defense Prototype")

        Tower(screen_width, screen_height) #Initialize Tower

        self.tower_colors = [Colors.RED, Colors.GREEN, Colors.BLUE]  # Colors associated with each tower option
        self.selected_tower = None  # The currently selected tower

        self.tower_size = 50  # Size of each tower

        GridCell(screen_width, screen_height, Colors)



        # Initialize game variables
        self.health = health
        self.money = money

        # Initialize enemies list
        self.enemies = []

        # Initialize exit button
        self.exit_button = pygame.Rect(self.screen_width - 120, 20, 100, 40)

        # Load font and colors for UI text
        self.font = pygame.font.Font(None, 30)  # Set font size to 30
        self.health_color = Colors.BLACK
        self.money_color = Colors.BLACK
        self.exit_button_color = Colors.RED
        self.exit_text_color = Colors.WHITE


        self.grid_colors = [[Colors.LIGHT_GREY if maze[row][col] == 1 else Colors.WHITE for col in range(self.grid_cols)] for row in range(self.grid_rows)]

        # Create an instance of the Enemy class with the predefined path
        self.enemy = Enemy(self.cell_size, self.start_x, self.start_y)


    # ---------------------
    # UI Manager
    # ---------------------
    def draw_ui(self):
        """Draws the user interface on the screen."""
        # Display health
        health_text = self.font.render("Health: {}".format(self.health), True, self.health_color)
        self.screen.blit(health_text, (20, 20))

        # Display money
        money_text = self.font.render("Money: ${}".format(self.money), True, self.money_color)
        self.screen.blit(money_text, (20, 60))

        # Draw exit button
        pygame.draw.rect(self.screen, self.exit_button_color, self.exit_button)
        exit_text = self.font.render("Exit", True, self.exit_text_color)
        self.screen.blit(exit_text, (self.screen_width - 100, 30))

        pygame.display.flip()

    # ---------------------
    # Input Manager
    # ---------------------
    def handle_mouse_click(self, mouse_x, mouse_y):
        """Handles mouse click events.

        Args:
            mouse_x (int): The x-coordinate of the mouse click.
            mouse_y (int): The y-coordinate of the mouse click.
        """        
        # Check if a tower option was clicked and update the selected color
        for i in range(3):
            if self.tower_options[i].collidepoint(mouse_x, mouse_y):
                self.selected_tower = self.tower_colors[i]
                break

        # Check if a grid cell was clicked and update its color
        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                if self.grid[row][col].collidepoint(mouse_x, mouse_y):
                    if self.selected_tower and self.maze[row][col] == 1:  # Check if it's a wall cell
                        self.grid_colors[row][col] = self.selected_tower
                        self.selected_tower = None

        # Check if exit button was clicked
        if self.exit_button.collidepoint(mouse_x, mouse_y):
            pygame.quit()
            sys.exit()

    # ---------------------
    # Game Loop
    # ---------------------
    def run(self):
        """Runs the game loop."""
        clock = pygame.time.Clock()  # Create a clock to control the frame rate
        enemy_spawn_interval = 2000  # Spawn a new enemy every 2000 milliseconds (2 seconds)
        last_enemy_spawn_time = 0  # Track the time of the last enemy spawn

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.handle_mouse_click(mouse_x, mouse_y)

            # Spawn a new enemy based on the spawn interval
            current_time = pygame.time.get_ticks()
            if current_time - last_enemy_spawn_time > enemy_spawn_interval:
                last_enemy_spawn_time = current_time
                new_enemy = Enemy(self.cell_size, self.start_x, self.start_y)  # Assuming self.cell_size is defined in Game class
                # Add the new enemy to your list of enemies (you'll need to maintain a list for all enemies)
                self.enemies.append(new_enemy)

            # Move all enemies
            for enemy in self.enemies:
                enemy.move()

            self.screen.fill(Colors.WHITE)

            # Draw grid with lines
            for row in range(self.grid_rows):
                for col in range(self.grid_cols):
                    pygame.draw.rect(self.screen, self.grid_colors[row][col], self.grid[row][col], 0)
                    pygame.draw.rect(self.screen, Colors.GREY, self.grid[row][col], 1)

            # Draw tower options
            for i in range(3):
                pygame.draw.rect(self.screen, self.tower_colors[i], self.tower_options[i])

            # Draw all enemies
            for enemy in self.enemies:
                enemy.draw(self.screen)

            # Draw UI
            self.draw_ui()

            pygame.display.flip()
            clock.tick(60)  # Limit the frame rate to 60 frames per second


if __name__ == "__main__":
    game = Game()
    game.run()
