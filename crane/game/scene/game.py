"""This module contains the `Game` class, which
handles all of the crane/progress stuff.
"""
import enum
import time

import pygame

from crane.engine.scene.scene import SceneManager
from crane.game.resources import get_background
from crane.game.scene.crane_scene.crane_scene import CraneScene
from crane.game.scene.progress_scene.progress_scene import ProgressScene


class GameState(enum.Enum):
    """Litle enum representing the states the game can be in.

    ArcadeView: the main game state.
    ProgressView: the progress view state.
    """
    ArcadeState = 0
    ProgressState = 1


class Game(SceneManager):

    def __init__(self):
        """A scene manager containing two main scenes: the
        arcade (game) scene, and the progress (pokemon) scene.
        """
        super(Game, self).__init__()

        self._crane_scene = CraneScene()
        self._progress_scene = ProgressScene()
        self.current_scene = self._crane_scene

        self._toggle_press_time = 0 # Used to prevent rapid switching between states

    def update(self, dt: float):
        """Handles switching between the different scenes,
        and updates the current scene.

        Args:
            dt (float): the time in seconds since the last update.
        """
        super().update(dt)
        current_time = time.time()

        keys = pygame.key.get_pressed()

        # Toggle game state
        if keys[pygame.K_ESCAPE] and current_time - self._toggle_press_time > 0.25:
            self._toggle_press_time = current_time
            if self.current_scene == self._progress_scene:
                self.current_scene = self._crane_scene
            else:
                self.current_scene = self._progress_scene

        # Reset crane machine
        elif keys[pygame.K_r] and current_time - self._toggle_press_time > 0.25:
            self._toggle_press_time = current_time
            self._crane_scene = CraneScene()
            self.current_scene = self._crane_scene

    def render(self, surface: pygame.surface.Surface):
        """Renders the game in its current state.

        Args:
            surface (Surface): the surface to render to.
        """
        # Draw background image
        image = get_background()
        height = surface.get_height()
        width = height * image.get_width() / image.get_height()
        image = pygame.transform.smoothscale(image, (width, height))
        surface.blit(image, (0, 0))

        super().render(surface)
