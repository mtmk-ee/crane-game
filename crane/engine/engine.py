"""This module contains the `Engine` class.

This class handles the timing of rendering and updating
the game. The updating portion is done in a separate
thread to avoid loading the main thread and dropping the FPS.
"""
import threading
import time

import pygame

from crane.engine.display import Display
from crane.engine.scene.scene import Scene


class Engine:

    def __init__(self, display: Display, target_fps: int, target_ups: int):
        """The Engine class, used to handle timing of updating/rendering.

        Timing is not exact, and the actual FPS/UPS may be lower
        than the given targets if the rendering or updating process
        is running slow.

        Args:
            display (Display): the game display.
            target_fps (int): the desired frames per second.
            target_ups (int): the desired updates per second.
        """
        self._display = display

        self._ups = 0
        self._fps = 0
        self._target_fps = target_fps
        self._target_ups = target_ups
        self._update_clock = pygame.time.Clock()
        self._render_clock = pygame.time.Clock()

        self._last_fps_print_time = 0
        self._last_ups_print_time = 0

        self._running = False
        self._update_thread: threading.Thread = None

        self._scene = None

    # ============================== Properties ==============================
    @property
    def display(self) -> Display:
        """Gets the display object
        """
        return self._display

    @property
    def scene(self) -> Scene:
        """Get/set the main scene to update/rendere.
        """
        return self._scene

    @scene.setter
    def scene(self, scene: Scene):
        self._scene = scene

    @property
    def ups(self) -> float:
        """The measured UPS in Hz.
        """
        return self._ups

    @property
    def fps(self) -> float:
        """The measured FPS in Hz.
        """
        return self._fps

    @property
    def target_ups(self) -> float:
        """Get/set the target UPS in Hz.
        """
        return self._target_ups

    @target_ups.setter
    def target_ups(self, target_ups: float):
        self._target_ups = target_ups

    @property
    def target_fps(self) -> float:
        """Get/set the target FPS in Hz.
        """
        return self._target_fps

    @target_fps.setter
    def target_fps(self, target_fps: float):
        self._target_fps = target_fps

    # ============================== Public ==============================
    def start(self):
        """Starts the game engine. This method blocks
        until the engine is stopped (display closed).

        Only call when the engine is not running!

        Raises:
            A `RuntimeError` if called while already running.
        """
        if self._running:
            raise RuntimeError('Bruh read the docstring')
        self._running = True
        self._run_update_loop()
        self._run_render_loop()

    def stop(self):
        """Stops the game engine. This method blocks
        until the update thread exits.

        Only call when the engine is running!

        Raises:
            A `RuntimeError` if called while not running.
        """
        if not self._running:
            raise RuntimeError('Bruh you really gotta read the docstring')
        self._running = False
        self._update_thread.join()

    # ============================== Private ==============================
    def _run_update_loop(self):
        """Runs the update loop in a separate thread.
        """
        self._update_thread = threading.Thread(target=self._update_loop)
        self._update_thread.start()

    def _update_loop(self):
        """The update loop. Handles the timing of when to call the
        `update()` function.
        """
        while self._running:
            delta = self._update_clock.tick(self._target_ups) # Returns ms
            self._ups = self._update_clock.get_fps()

            self._update(delta / 1000)

            # Periodically print out UPS
            if time.perf_counter() - self._last_ups_print_time > 1:
                self._last_ups_print_time = time.perf_counter()
                # print('UPS:', self.ups) <- annoying

    def _run_render_loop(self):
        """The render loop! Handles the timing of when to call the
        `render()` function.
        """
        while self._running:
            self._render_clock.tick(self._target_fps) # Returns ms
            self._fps = self._render_clock.get_fps()

            self._poll_events()
            self._render()

            # Periodically print out FPS
            if time.perf_counter() - self._last_fps_print_time > 1:
                self._last_fps_print_time = time.perf_counter()
                # print('FPS:', self.fps) <- annoying

    def _update(self, dt: float):
        """Calls the update function on the scene,
        if it exists.

        Args:
            dt (float): the time in seconds since the last update.
        """
        if self._scene:
            self._scene.update(dt)

    def _render(self):
        """Calls the render function on the scene,
        if it exists. Scene is rendered to display.
        """
        try:
            # Display is a context manager, all rendering done inside `with` block
            with self.display as surface:
                if self._scene:
                    self._scene.render(surface)
        except:
            raise

    def _poll_events(self):
        """Processes events from pygame.

        Calls the `stop()` function if the
        QUIT event is raised.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
