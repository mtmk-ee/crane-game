import math
import time

import pygame

from crane.engine.scene.scene import Scene
from crane.game.resources import get_prize_count, get_prize_image, get_prize_names
from crane.helpers import draw_text


class ProgressScene(Scene):

    COLUMNS = 4
    ROWS = 3
    CELL_SIZE = 75
    MARGIN_X = 40
    MARGIN_Y = 75

    def __init__(self):
        """A scene containing images of all the pokemon and their
        names/win count.
        """
        super(ProgressScene, self).__init__()
        self._page = 0
        self._num_pages = math.ceil(len(get_prize_names()) / (self.ROWS * self.COLUMNS))

        self._key_press_time = 0

    def update(self, dt: float):
        """Updates which page is currently being shown
        based on key presses.

        Args:
            dt (float): the time in seconds since the last update
        """
        super().update(dt)

        # Navigate pages, and prevent the keys from being repeated too fast
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and time.time() - self._key_press_time > 0.25:
            self._key_press_time = time.time()
            self._page = max(self._page - 1, 0)
        elif keys[pygame.K_d] and time.time() - self._key_press_time > 0.25:
            self._key_press_time = time.time()
            self._page = min(self._page + 1, self._num_pages - 1)

    def render(self, surface: pygame.surface.Surface):
        """Renders all the pokemon stuff to the surface.

        Args:
            surface (Surface): the surface to render to.
        """
        super().render(surface)

        r, c = 0, 0
        start_idx = self._page * self.COLUMNS * self.ROWS
        end_idx = start_idx + self.COLUMNS * self.ROWS

        # Add one cell for each type of pokemon
        names = get_prize_names()
        for i in range(start_idx, end_idx):
            if i >= len(names):
                break
            elif c >= self.COLUMNS:
                r += 1
                c = 0

            x = c * (self.CELL_SIZE + self.MARGIN_X) + (surface.get_width() / 2 - (self.COLUMNS - 0.25) * (self.CELL_SIZE + self.MARGIN_X) / 2)
            y = r * (self.CELL_SIZE + self.MARGIN_Y) + (surface.get_height() / 2 - (self.ROWS - 0.25) * (self.CELL_SIZE + self.MARGIN_Y) / 2)
            c += 1

            prize_name = names[i]
            count = get_prize_count(prize_name)
            image = get_prize_image(prize_name)

            image = pygame.transform.smoothscale(image, (self.CELL_SIZE, self.CELL_SIZE))
            surface.blit(image, (x, y))

            # Draw labels
            draw_text(surface, prize_name, 'Comic Sans MS', 20, (255, 255, 255), (x, y + self.CELL_SIZE))
            draw_text(surface, f'{count}', 'Comic Sans MS', 20, (255, 255, 255), (x, y + self.CELL_SIZE + 20))

        draw_text(surface, f'Page {self._page + 1} / {self._num_pages}', 'Comic Sans MS', 20, (255, 255, 255), (0, 0))
