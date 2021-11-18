import threading
import time

import pygame

from crane.engine.display import Display
from crane.engine.scene.scene import Scene


class Engine:

    def __init__(self, display: Display, target_fps: int, target_ups: int):
        self._display = display

        self._ups = 0
        self._fps = 0
        self._target_fps = target_fps
        self._target_ups = target_ups

        self._last_fps_print_time = 0
        self._last_ups_print_time = 0

        self._running = False
        self._update_clock = pygame.time.Clock()
        self._render_clock = pygame.time.Clock()
        self._update_thread: threading.Thread = None

        self._scene = None

    # ============================== Properties ==============================
    @property
    def display(self) -> Display:
        return self._display

    @property
    def scene(self) -> Scene:
        return self._scene

    @scene.setter
    def scene(self, scene: Scene):
        self._scene = scene

    @property
    def ups(self) -> float:
        return self._ups

    @property
    def fps(self) -> float:
        return self._fps

    @property
    def target_ups(self) -> float:
        return self._target_ups

    @target_ups.setter
    def target_ups(self, target_ups: float):
        self._target_ups = target_ups

    @property
    def target_fps(self) -> float:
        return self._target_fps

    @target_fps.setter
    def target_fps(self, target_fps: float):
        self._target_fps = target_fps

    # ============================== Public ==============================
    def start(self):
        self._running = True
        self._run_update_loop()
        self._run_render_loop()

    def stop(self):
        self._running = False
        self._update_thread.join()

    # ============================== Private ==============================
    def _run_update_loop(self):
        self._update_thread = threading.Thread(target=self._update_loop)
        self._update_thread.start()

    def _update_loop(self):
        while self._running:
            delta = self._update_clock.tick(self._target_ups)
            self._update(delta / 1000)
            self._ups = self._update_clock.get_fps()

            if time.perf_counter() - self._last_ups_print_time > 1:
                self._last_ups_print_time = time.perf_counter()
                print('UPS:', self.ups)

    def _run_render_loop(self):
        while self._running:
            self._poll_events()
            self._render()
            self._render_clock.tick(self._target_fps)
            self._fps = self._render_clock.get_fps()

            if time.perf_counter() - self._last_fps_print_time > 1:
                self._last_fps_print_time = time.perf_counter()
                print('FPS:', self.fps)

    def _update(self, dt: float):
        if self._scene:
            self._scene.update(dt)

    def _render(self):
            try:
                with self.display as surface:
                    if self._scene:
                        self._scene.render(surface)
            except:
                raise

    def _poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
