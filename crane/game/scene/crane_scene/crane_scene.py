import pygame

from crane.engine.scene.scene import PhysicsScene
from crane.game.resources import get_prize_names, get_total_prizes, get_total_spent, get_total_won, get_unique_prizes, increment_prize
from crane.game.scene.crane_scene.container_object import ContainerObject
from crane.game.scene.crane_scene.prize_adder import PrizeAdder
from crane.game.scene.crane_scene.prize_object import PrizeObject
from crane.helpers import draw_text


class CraneScene(PhysicsScene):

    def __init__(self):
        super(CraneScene, self).__init__()

        num_prizes = 30
        prize_adder = PrizeAdder(self)
        prize_adder.add_prizes(num_prizes)
        self.add(prize_adder)

        self.add(ContainerObject(self._world))

    def update(self, dt: float):
        super().update(dt)

        for object in self._children:
            if isinstance(object, PrizeObject):
                if object._body.position[1] < 0:
                    increment_prize(object._prize_name)
                    self.remove(object)

    def render(self, surface: pygame.surface.Surface):
        super().render(surface)

        spent = get_total_spent()
        won = get_total_won()
        ratio = won / spent

        draw_text(
            surface,
            text=f'Unique Pokemon: {get_unique_prizes()} / {len(get_prize_names())}',
            font_name='Comic Sans MS',
            size=20,
            color=(255, 255, 255),
            pos=(10, 0),
        )
        draw_text(
            surface,
            text=f'Total Pokemon: {get_total_prizes()}',
            font_name='Comic Sans MS',
            size=20,
            color=(255, 255, 255),
            pos=(10, 40),
        )
        draw_text(
            surface,
            text=f'Spent: ${get_total_spent():.2f}',
            font_name='Comic Sans MS',
            size=20,
            color=(255, 255, 255),
            pos=(300, 0),
        )
        draw_text(
            surface,
            text=f'Won: ${get_total_won():.2f}',
            font_name='Comic Sans MS',
            size=20,
            color=(255, 255, 255),
            pos=(300, 40),
        )
        draw_text(
            surface,
            text=f'Ratio: ${ratio:.2f}',
            font_name='Comic Sans MS',
            size=20,
            color=(255, 255, 255),
            pos=(300, 80),
        )
