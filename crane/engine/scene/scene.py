import abc
from typing import List

import Box2D
import pygame

from crane.engine.scene.scene_object import RenderableSceneObject, SceneObject, UpdateableSceneObject
from crane.globals import PIXELS_PER_METER



class Scene(UpdateableSceneObject, RenderableSceneObject):

    def __init__(self):
        super(Scene, self).__init__()
        self._children: List[SceneObject] = []

    def add(self, object: SceneObject):
        self._children.append(object)

    def remove(self, object: SceneObject):
        self._children.remove(object)

    def update(self, dt: float):
        for child in self._children:
            if isinstance(child, UpdateableSceneObject):
                child.update(dt)

    def render(self, surface: pygame.surface.Surface):
        for child in self._children:
            if isinstance(child, RenderableSceneObject):
                child.render(surface)


class SceneManager(UpdateableSceneObject, RenderableSceneObject):

    def __init__(self):
        super(SceneManager, self).__init__()
        self._current_scene: Scene = None

    @property
    def current_scene(self) -> Scene:
        return self._current_scene

    @current_scene.setter
    def current_scene(self, current_scene: Scene):
        self._current_scene = current_scene

    def update(self, dt: float):
        if self.current_scene:
            self.current_scene.update(dt)

    def render(self, surface: pygame.surface.Surface):
        if self.current_scene:
            self.current_scene.render(surface)


class PhysicsScene(Scene):

    def __init__(self, gravity: float=-9.81):
        super(PhysicsScene, self).__init__()
        self._world = Box2D.b2World(gravity=(0, gravity), doSleep=True)
        self._wireframe = True

    def step(self, count=1):
        dt = 0.016
        for _ in range(count):
            self._world.Step(dt, 10, 10)


    @property
    def wireframe(self) -> bool:
        return self._wireframe

    @wireframe.setter
    def wireframe(self, enabled: bool):
        self._wireframe = enabled

    def add(self, object: SceneObject):
        self._children.append(object)

    def remove(self, object: SceneObject):
        self._children.remove(object)

    def update(self, dt: float):
        self._world.Step(dt, 10, 10)
        super().update(dt)
