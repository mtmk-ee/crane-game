"""This module contains the Display class,
used to create and manage a pygame window.
"""
from typing import Tuple

import pygame

from crane import globals


class Display:
    _DEPTH = 32

    def __init__(self, caption: str, size: tuple=globals.SCREEN_SIZE_P):
        """The window where everything in the game is drawn to.
        The `Display` class is also a context manager, so you can
        enter it and place rendering code inside `with` block.

        Only one display can be used at a time!

        Args:
            caption (str): the title of the window.
            size (tuple): the size of the window.
        """
        self._surface = pygame.display.set_mode(size, pygame.RESIZABLE, self._DEPTH)
        self._clear_color = (255, 255, 255, 255)

        pygame.display.set_caption(caption)

    def __enter__(self) -> pygame.surface.Surface:
        """Starts the rendering process.

        Returns:
            The display surface
        """
        self.clear()
        return self._surface

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Finishes the rendering process.

        Args:
            A bunch of stuff used for handling exceptions
        """
        self.finish()
        return True

    @property
    def surface(self) -> pygame.surface.Surface:
        """The display surface, can be rendered to.

        Make sure not to draw between when the display
        is flipped to when it is cleared, since nothing
        will show up.

        Returns:
            The display surface.
        """
        return self._surface

    @property
    def size(self) -> Tuple[int, int]:
        """The size of the display as a tuple (w, h) of pixles
        """
        return pygame.display.get_window_size()

    def clear(self):
        """Clears the surface by filling it with a uniform color.
        """
        self._surface.fill(self._clear_color)

    def finish(self):
        """Finishes the rendering of a single frame and updates
        the window.
        """
        pygame.display.flip()
