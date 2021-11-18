from typing import Tuple
import pygame

from crane import globals


class Display:
    _DEPTH = 32

    def __init__(self, caption: str, size=globals.SCREEN_SIZE_P):
        self._surface = pygame.display.set_mode(size, pygame.RESIZABLE, self._DEPTH)
        pygame.display.set_caption(caption)
        self._clear_color = (255, 255, 255, 255)

    def __enter__(self) -> 'Display':
        self.clear()
        return self._surface

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.finish()
        return True

    @property
    def surface(self) -> pygame.surface.Surface:
        return self._surface

    @property
    def size(self) -> Tuple[int, int]:
        return pygame.display.get_window_size()

    def clear(self):
        self._surface.fill(self._clear_color)

    def finish(self):
        pygame.display.flip()
