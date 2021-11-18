import math
import os
from pathlib import Path
import random

import Box2D
import pygame

import crane
from crane import globals
from crane.engine.scene.scene_object import PhysicsObject, TexturedPhysicsObject
from crane.game.resources import get_prize_image, get_prize_names, get_prize_path


class PrizeObject(TexturedPhysicsObject):

    def __init__(self, world: Box2D.b2World, prize_name: str=None):
        self._prize_name = prize_name or random.choice(get_prize_names())
        super(PrizeObject, self).__init__(world, get_prize_image(self._prize_name), scale=2)

        cx, cy = globals.SCREEN_CENTER_M

        self._body = world.CreateDynamicBody(position=(cx + 3 * random.random(), cy))
        # self._body.CreatePolygonFixture(box=(1, 1), density=1, friction=0.3)
        # self._body.CreateCircleFixture(radius=1, density=1, friction=0.9)

        num_sides = 6
        r = 1
        c = 2 * math.pi / num_sides
        vertices = [
            (r * math.cos(c * i), r * math.sin(c * i))
            for i in range(num_sides)
        ]

        self._body.CreatePolygonFixture(vertices=vertices, density=0.1, friction=0.9)

    def render(self, surface: pygame.surface.Surface):
        self.render_body(surface, self._body)

    def _get_image_path(self, name: str) -> str:
        if not name:
            name = random.choice(get_prize_names())
        return pygame.image.load(get_prize_path(name))
