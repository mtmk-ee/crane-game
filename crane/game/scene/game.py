import enum
import time

import pygame

from crane.engine.scene.scene import Scene, SceneManager
from crane.game.resources import get_background
from crane.game.scene.crane_scene.crane_scene import CraneScene
from crane.game.scene.progress_scene.progress_scene import ProgressScene


class GameState:
    Playing=0
    ProgressView=1

class Game(SceneManager):

    def __init__(self):
        super(Game, self).__init__()

        self._crane_scene = CraneScene()
        self._progress_scene = ProgressScene()
        self.current_scene = self._crane_scene
        self._press_time = 0

    def update(self, dt: float):
        super().update(dt)
        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE] and time.time() - self._press_time > 0.25:
            self._press_time = time.time()
            if self.current_scene == self._crane_scene:
                self.current_scene = self._progress_scene
            else:
                self.current_scene = self._crane_scene
        elif keys[pygame.K_r] and time.time() - self._press_time > 0.25:
            self._press_time = time.time()
            self._crane_scene = CraneScene()
            self.current_scene = self._crane_scene

    def render(self, surface: pygame.surface.Surface):

        image = get_background()
        height = surface.get_height()
        width = height * image.get_width() / image.get_height()

        image = pygame.transform.smoothscale(image, (width, height))
        surface.blit(image, (0, 0))

        # pygame.draw.rect(surface, (255, 255, 255), (0, 0, surface.get_width(), (20 + 20) * 3))
        super().render(surface)
