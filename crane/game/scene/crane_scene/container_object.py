import enum

import Box2D
import pygame

from crane.engine.scene.scene_object import PhysicsObject
from crane import globals
from crane.game.resources import use_money


class CraneState(enum.Enum):
    Ready=0
    Dropping=1
    Grabbing=2
    Rising=3


class ContainerObject(PhysicsObject):
    _ROPE_COLOR = (135, 86, 56)
    _CLASP_COLOR = (85, 86, 82)
    def __init__(self, world: Box2D.b2World, center=globals.SCREEN_CENTER_M, dimensions=(20, 20)):
        super(ContainerObject, self).__init__(world)

        self._crane_state = CraneState.Ready
        self._dimensions = dimensions

        w, h = dimensions
        hw, hh = w / 2, h / 2
        cx, cy = center
        self._boundary_thickness = 0.25
        self._support_thickness = 0.25
        drop_zone_width = 4
        drop_separator_height = self._dimensions[1] / 4

        bl = world.CreateStaticBody(position=(cx - hw + self._boundary_thickness, cy))
        bl.CreatePolygonFixture(box=(self._boundary_thickness, hh), friction=0.9)
        br = world.CreateStaticBody(position=(cx + hw - self._boundary_thickness, cy))
        br.CreatePolygonFixture(box=(self._boundary_thickness, hh), friction=0.9)
        bt = world.CreateStaticBody(position=(cx, cy + hh - self._boundary_thickness))
        bt.CreatePolygonFixture(box=(hw, self._boundary_thickness),friction=0.9)
        bb = world.CreateStaticBody(position=(cx + drop_zone_width / 2, cy - hh + self._boundary_thickness))
        bb.CreatePolygonFixture(box=(hw - drop_zone_width / 2, self._boundary_thickness), friction=0.9)
        bs = world.CreateStaticBody(position=(cx - hw + drop_zone_width, cy - hh + drop_separator_height))
        bs.CreatePolygonFixture(box=(self._boundary_thickness, drop_separator_height), friction=0.9)
        self._box_bodies = [bl, br, bt, bb, bs]

        support_size = (self._support_thickness, self._support_thickness)
        self._support = world.CreateKinematicBody(position=(cx, cy + hh - self._boundary_thickness * 2 - support_size[1]))
        self._support.CreatePolygonFixture(box=support_size, friction=0.5)

        rope_len = 2
        rope_elems = 20
        rope_thickness = 0.125
        rope_elem_len = rope_len / rope_elems
        shape = Box2D.b2PolygonShape(box=(rope_thickness, rope_elem_len))
        fd = Box2D.b2FixtureDef(
            shape=shape,
            friction=0.9,
            density=1,
            categoryBits=0x0001,
            maskBits=(0xFFFF & ~0x0002),
        )

        prevBody = self._support
        self._rope_bodies = []
        y = cy + hh - self._boundary_thickness * 2 - support_size[1] - rope_elem_len
        for i in range(rope_elems):
            body = self._world.CreateDynamicBody(
                position=(cx, y - i * rope_elem_len * 2),
                fixtures=fd,
                angularDamping=1000,
            )

            self._world.CreateRevoluteJoint(
                bodyA=prevBody,
                bodyB=body,
                anchor=(cx, y - i * rope_elem_len * 2),
                collideConnected=False,
            )

            prevBody = body
            self._rope_bodies.append(body)

        try:
            arm_w, arm_h = 1, 3
            arm_t = 0.5
            arm_y = y - rope_elems * rope_elem_len * 2

            arm_lt_verts = [(0, 0), (-arm_w, -arm_h/2), (-arm_w+arm_t, -arm_h/2)]
            arm_lb_verts = [(-arm_w, -arm_h/2), (-arm_w+arm_t, -arm_h/2), (0, -arm_h)]
            arm_rt_verts = [(0, 0), (arm_w, -arm_h/2), (arm_w-arm_t, -arm_h/2)]
            arm_rb_verts = [(arm_w, -arm_h/2), (arm_w-arm_t, -arm_h/2), (0, -arm_h)]

            self._arm_left = world.CreateDynamicBody(position=(cx, arm_y), angularDamping=10)
            self._arm_left.CreatePolygonFixture(vertices=arm_lt_verts, friction=0.5, density=1)
            self._arm_left.CreatePolygonFixture(vertices=arm_lb_verts, friction=0.5, density=1)
            self._arm_right = world.CreateDynamicBody(position=(cx, arm_y), angularDamping=10)
            self._arm_right.CreatePolygonFixture(vertices=arm_rt_verts, friction=0.5, density=1)
            self._arm_right.CreatePolygonFixture(vertices=arm_rb_verts, friction=0.5, density=1)

            self._world.CreateRevoluteJoint(
                bodyA=body,
                bodyB=self._arm_left,
                anchor=(cx, arm_y),
                collideConnected=False,
            )
            self._world.CreateRevoluteJoint(
                bodyA=body,
                bodyB=self._arm_right,
                anchor=(cx, arm_y),
                collideConnected=False,
            )

            self._arm_bodies = [self._arm_left, self._arm_right]
        except BaseException as e:
            print(e)

    def update(self, dt: float):
        try:
            self._update_support()
        except BaseException as e:
            print(e)

    def _update_support(self):
        pos = self._support.position

        keys = pygame.key.get_pressed()

        min_x = globals.SCREEN_CENTER_M[0] - self._dimensions[0] / 2 + self._boundary_thickness * 2 + self._support_thickness
        max_x = globals.SCREEN_CENTER_M[0] + self._dimensions[0] / 2 - self._boundary_thickness * 2 - self._support_thickness
        max_y = globals.SCREEN_CENTER_M[1] + self._dimensions[1] / 2 - self._boundary_thickness * 2 - self._support_thickness
        min_y = globals.SCREEN_CENTER_M[1]

        vx_mag = 3
        vy_mag = 3
        torque_mag = 8

        torque = 0
        vx, vy = 0, 0
        if self._crane_state == CraneState.Dropping:
            torque = torque_mag
            vy = -vy_mag
            if pos[1] < min_y:
                self._crane_state = CraneState.Grabbing
        elif self._crane_state == CraneState.Grabbing:
            torque = -torque
        elif self._crane_state == CraneState.Rising:
            torque = -torque
            vy = +vy_mag
            if pos[1] > max_y:
                self._crane_state = CraneState.Ready
        elif self._crane_state == CraneState.Ready:
            if keys[pygame.K_d] and pos[0] < max_x:
                vx = vx_mag
            elif keys[pygame.K_a] and pos[0] > min_x:
                vx = -vx_mag
            if keys[pygame.K_SPACE]:
                torque = torque_mag

        if keys[pygame.K_s] and self._crane_state == CraneState.Ready:
            self._crane_state = CraneState.Dropping
            use_money()
        elif keys[pygame.K_w] and self._crane_state in [CraneState.Dropping, CraneState.Grabbing]:
            self._crane_state = CraneState.Rising

        self._support.linearVelocity = vx, vy
        self._arm_left.ApplyTorque(-torque, True)
        self._arm_right.ApplyTorque(torque, True)

    def render(self, surface: pygame.surface.Surface):
        for body in self._box_bodies:
            self.render_body(surface, body)

        for body in self._rope_bodies:
            self.render_body(surface, body, self._ROPE_COLOR)

        for body in self._arm_bodies:
            self.render_body(surface, body, self._CLASP_COLOR)

        self.render_body(surface, self._support)


        try:
            verts = [
                self._support.position[0] - self._support_thickness / 2,
                surface.get_height() / globals.PIXELS_PER_METER - (globals.SCREEN_CENTER_M[1] + self._dimensions[1] / 2),
                self._support_thickness,
                globals.SCREEN_CENTER_M[1] + self._dimensions[1] / 2 - self._support.position[1],
            ]
            verts = [
                vert * globals.PIXELS_PER_METER
                for vert in verts
            ]
            pygame.draw.rect(
                surface,
                (255, 255, 255),
                tuple(verts)
            )
        except BaseException as e:
            print(e)
