import abc

import Box2D
import pygame
from pygame import gfxdraw

from crane.globals import PIXELS_PER_METER


class SceneObject(abc.ABC):

    def __init__(self):
        super(SceneObject, self).__init__()


class UpdateableSceneObject(SceneObject):

    def __init__(self):
        super(UpdateableSceneObject, self).__init__()

    @abc.abstractmethod
    def update(self, dt: float): ...


class RenderableSceneObject(SceneObject):

    def __init__(self):
        super(RenderableSceneObject, self).__init__()

    @abc.abstractmethod
    def render(self, surface: pygame.surface.Surface): ...


class PhysicsObject(UpdateableSceneObject, RenderableSceneObject):

    def __init__(self, world: Box2D.b2World):
        super(PhysicsObject, self).__init__()
        self._world = world

    def update(self, dt: float): ...

    def render_body(self, surface: pygame.surface.Surface, body: Box2D.b2Body, color=(255, 255, 255)):
        try:
            for fixture in body.fixtures:
                shape = fixture.shape
                vertices = []
                for v in shape.vertices:
                    v = Box2D.b2Vec2(v[0], v[1])
                    v = body.transform * v * PIXELS_PER_METER
                    vertices.append((v[0], surface.get_size()[1] - v[1]))

                # Draw twice to properly anti-alias
                gfxdraw.aapolygon(surface, vertices, color)
                gfxdraw.filled_polygon(surface, vertices, color)
        except BaseException as e:
            print(e)


class TexturedPhysicsObject(PhysicsObject):

    def __init__(self, world: Box2D.b2World, image: pygame.surface.Surface, scale=1, angle=0):
        super(TexturedPhysicsObject, self).__init__(world)
        self._image = image
        self._angle = angle
        self._scale = (scale * PIXELS_PER_METER, scale * PIXELS_PER_METER)

    def render_body(self, surface: pygame.surface.Surface, body: Box2D.b2Body):
        try:
            pos, angle = body.position, body.angle + self._angle
            pos = pos[0] * PIXELS_PER_METER, pos[1] * PIXELS_PER_METER

            image = self._image
            image = pygame.transform.smoothscale(image, self._scale)
            image = pygame.transform.rotate(image, angle * 180 / 3.14159)

            surface.blit(image, (pos[0] - image.get_width() / 2, surface.get_height() - pos[1] - image.get_height() / 2))
        except BaseException as e:
            print(e)



class GroundObject(PhysicsObject):
    def __init__(self, world: Box2D.b2World):
        super(GroundObject, self).__init__(world)
        self._body = world.CreateStaticBody(position=(0, 0))
        self._body.CreatePolygonFixture(box=(200, 1), density=1, friction=0)


    def render(self, surface: pygame.surface.Surface):
        self.render_body(surface, self._body)
