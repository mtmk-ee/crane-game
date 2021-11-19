import math
import random
from typing import List, Tuple

import Box2D
import pygame

from crane import globals
from crane.engine.scene.scene_object import TexturedPhysicsObject
from crane.game.resources import get_prize_image, get_prize_names, get_prize_path


class PrizeObject(TexturedPhysicsObject):

    def __init__(self, world: Box2D.b2World, prize_name: str=None):
        """One of the prizes that goes in the crane machine.

        Adds a polygon body to the world at roughly the center of
        the screen.

        Args:
            world (b2World): the world to add bodies into
            prize_name (str): the name of the prize to add, or `None`
                for a random one.
        """
        self._prize_name = prize_name or random.choice(get_prize_names())
        super(PrizeObject, self).__init__(world, get_prize_image(self._prize_name), scale=2)

        # Add a polygon body to the world
        cx, cy = globals.SCREEN_CENTER_M
        self._body = world.CreateDynamicBody(position=(cx + 3 * random.random(), cy))
        self._body.CreatePolygonFixture(vertices=self._get_polygon_vertices(), density=0.1, friction=0.9)

    def _get_polygon_vertices(self, num_sides=6, radius=1) -> List[Tuple[float, float]]:
        """Returns vertices for a regular polygon.

        Returns:
            A list of coordinates (x, y)
        """
        c = 2 * math.pi / num_sides
        return [
            (radius * math.cos(c * i), radius * math.sin(c * i))
            for i in range(num_sides)
        ]

    def render(self, surface: pygame.surface.Surface):
        """Renders the body to the surface with the appropriate texture.

        Args:
            surface (Surface): the surface to render to.
        """
        self.render_body(surface, self._body)

    def _get_image(self, name: str) -> pygame.surface.Surface:
        """Gets an image corresponding to the given pokemon name.

        Args:
            name (str): the name, or `None` for a randomized
                type of pokemon.

        Returns:
            The image as a pygame Surface.
        """
        if not name:
            name = random.choice(get_prize_names())
        return pygame.image.load(get_prize_path(name))
