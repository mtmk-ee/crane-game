"""This module contains a variety of specialized
scene objects.
"""
from typing import List

import Box2D
import pygame

from crane.engine.scene.scene_object import (
    RenderableSceneObject,
    SceneObject,
    UpdateableSceneObject,
)


class Scene(UpdateableSceneObject, RenderableSceneObject):

    def __init__(self):
        """A updateable, renderable scene object that contains
        child scene objects.

        When this object is updated, the child objects are updated.
        When this object is rendered, the child objects are rendered.
        """
        super(Scene, self).__init__()

        # Contains all the child objects
        self._children: List[SceneObject] = []

    def add(self, object: SceneObject):
        """Adds a child object to this scene.
        """
        self._children.append(object)

    def remove(self, object: SceneObject):
        """Removes a child object from this scene.

        Will raise an exception if the object was not
        previously added!
        """
        self._children.remove(object)

    def update(self, dt: float):
        """Updates all the objects in this scene.

        Args:
            dt (float): time since last update.
        """
        for child in self._children:
            # Not all children can be updated
            if isinstance(child, UpdateableSceneObject):
                child.update(dt)

    def render(self, surface: pygame.surface.Surface):
        """Renders all the objects in this scene.

        Args:
            surface (Surface): the surface to draw on.
        """
        for child in self._children:
            # Not all children can be rendered
            if isinstance(child, RenderableSceneObject):
                child.render(surface)


class SceneManager(UpdateableSceneObject, RenderableSceneObject):

    def __init__(self):
        """A special scene object that manages scenes.

        Only one scene can be used at a time.
        """
        super(SceneManager, self).__init__()
        self._current_scene: Scene = None

    @property
    def current_scene(self) -> Scene:
        """Get/set the scene that is being updated/rendered.

        Returns:
            The scene object
        """
        return self._current_scene

    @current_scene.setter
    def current_scene(self, current_scene: Scene):
        self._current_scene = current_scene

    def update(self, dt: float):
        """Updates the current scene, if it exists.

        Args:
            dt (float): time since last update.
        """
        if self.current_scene:
            self.current_scene.update(dt)

    def render(self, surface: pygame.surface.Surface):
        """Renders the current scene, if it exists.

        Args:
            surface (Surface): the surface to draw the scene to.
        """
        if self.current_scene:
            self.current_scene.render(surface)


class PhysicsScene(Scene):

    def __init__(self, gravity: float=-9.81):
        """A special scene with physics capabilities.

        Contains a Box2D world to which bodies can be added.

        Args:
            gravity (float): Gravitation acceleration in m/s^2. Defaults to -9.81.
        """
        super(PhysicsScene, self).__init__()
        self._world = Box2D.b2World(gravity=(0, gravity), doSleep=True)

    def update(self, dt: float):
        """Updates the scene, and steps the world by `dt`.

        Args:
            dt (float): time in seconds since last update.
        """
        self._world.Step(dt, 10, 10)
        super().update(dt)
