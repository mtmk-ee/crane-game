"""Contains some basic scene objects.

Derive from one of these classes to implement
game stuff.
"""
import abc

import Box2D
import pygame
from pygame import gfxdraw

from crane.globals import PIXELS_PER_METER


class SceneObject(abc.ABC):

    def __init__(self):
        """Base class of all scene objects.

        A scene object corresponds to one element of the game
        that acts independently, like a pokemon or something idk
        """
        super(SceneObject, self).__init__()


class UpdateableSceneObject(SceneObject):

    def __init__(self):
        """A scene object that can be periodically updated (or "ticked").
        """
        super(UpdateableSceneObject, self).__init__()

    @abc.abstractmethod
    def update(self, dt: float):
        """Call to update the scene object.

        Game logic should go here.

        Be careful not to touch the GUI since this method is called
        from a separate thread!

        Args:
            dt (float): the time in seconds since the last time this method
                was called.
        """


class RenderableSceneObject(SceneObject):

    def __init__(self):
        """A scene object that can be rendered to a surface.
        """
        super(RenderableSceneObject, self).__init__()

    @abc.abstractmethod
    def render(self, surface: pygame.surface.Surface):
        """Renders the object to a surface.

        Only call this method from the main thread!

        Args:
            surface (Surface): the surface to render to.
        """


class PhysicsObject(UpdateableSceneObject, RenderableSceneObject):

    def __init__(self, world: Box2D.b2World):
        """A scene object that exists in a physics scene. The object can
        be both updated and rendered.

        Instantiating a `PhysicsObject` adds bodies to the Box2D
        world, regardless of whether it was added to a PhysicsScene already.

        Args:
            world (Box2D.b2World): [description]
        """
        super(PhysicsObject, self).__init__()
        self._world = world

    def update(self, dt: float):
        """Updates the physics object.

        Calling this method does not step the object in the world, it only
        performs behavioral logic for a particular object.

        Args:
            dt (float): the time in seconds since the last update.
        """

    def render_body(self, surface: pygame.surface.Surface, body: Box2D.b2Body, color=(255, 255, 255)):
        """Renders all polygons comprising the given body as a solid color

        Args:
            surface (Surface): the surface to render to.
            body (b2Body): the body to render.
            color (tuple): The RGB color to use to render the body. Defaults to (255, 255, 255).
        """
        # A body can have multiple fixtures, so we need to draw all of 'em
        for fixture in body.fixtures:

            # Need a list of vertices to draw the polygon
            shape = fixture.shape
            vertices = []
            for v in shape.vertices:

                # `shape.vertices` is static, need to apply the body transform to get
                # the correct vertices
                v = Box2D.b2Vec2(v[0], v[1])
                v = body.transform * v * PIXELS_PER_METER

                # Flip vertices vertically, since pygame coordinates are flipped
                vertices.append((v[0], surface.get_size()[1] - v[1]))

            # Draw twice to properly anti-alias
            gfxdraw.aapolygon(surface, vertices, color)
            gfxdraw.filled_polygon(surface, vertices, color)


class TexturedPhysicsObject(PhysicsObject):

    def __init__(self, world: Box2D.b2World, image: pygame.surface.Surface, scale=1, angle=0):
        """A physics object that has a single texture drawn over it.

        Args:
            world (b2World): the physics world to add the object to.
            image (Surface): the texture to use in rendering.
            scale (int): the scale to apply to the texture.
            angle (int): the angle offset in degrees to apply to the texture.
        """
        super(TexturedPhysicsObject, self).__init__(world)
        self._image = image
        self._angle = angle
        self._scale = (scale * PIXELS_PER_METER, scale * PIXELS_PER_METER)

    def render_body(self, surface: pygame.surface.Surface, body: Box2D.b2Body):
        """Renders a single body using the texture given.

        Args:
            surface (Surface): the surface to render to.
            body (b2Body): the body object to render the texture over.
        """
        pos, angle = body.position, body.angle + self._angle
        pos = pos[0] * PIXELS_PER_METER, pos[1] * PIXELS_PER_METER

        # Rotate/scale image to match the body orientation
        image = self._image
        image = pygame.transform.smoothscale(image, self._scale)
        image = pygame.transform.rotate(image, angle * 180 / 3.14159)

        # Need to flip the y-axis since pygame coordinates are flipped
        coords = (
            pos[0] - image.get_width() / 2,
            surface.get_height() - pos[1] - image.get_height() / 2
        )
        surface.blit(image, coords)
