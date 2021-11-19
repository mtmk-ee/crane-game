import pygame

from crane.engine.scene.scene import PhysicsScene
from crane.game.resources import (
    get_prize_names,
    get_total_prizes,
    get_total_spent,
    get_total_won,
    get_unique_prizes,
    increment_prize,
)
from crane.game.scene.crane_scene.container_object import ContainerObject
from crane.game.scene.crane_scene.prize_adder import PrizeAdder
from crane.game.scene.crane_scene.prize_object import PrizeObject
from crane.helpers import draw_text


class CraneScene(PhysicsScene):

    def __init__(self, num_prizes=30):
        """A physics scene containing the crane and prizes.
        """
        super(CraneScene, self).__init__()

        # Add prizes
        prize_adder = PrizeAdder(self)
        prize_adder.add_prizes(num_prizes)
        self.add(prize_adder)

        # Add crane
        self.add(ContainerObject(self._world))

    def update(self, dt: float):
        """Updates the crane scene and its children.

        Removes any prizes that go off-screen and increments
        the prize count.

        Args:
            dt (float): the time in seconds since the last update
        """
        super().update(dt)

        for object in self._children:
            # If a prize falls off the screen, we have a winner!
            if isinstance(object, PrizeObject) and object._body.position[1] < 0:
                increment_prize(object._prize_name)
                self.remove(object)


    def _draw_stat_text(self, surface: pygame.surface.Surface, text: str, pos: tuple):
        """Draws the given text onto a surface.

        Args:
            surface (Surface): the surface to render to.
            text (str): the text to show.
            pos (Tuple[int, int]): the position to draw the text at.
        """
        draw_text(
            surface,
            text=text,
            font_name='Comic Sans MS',
            size=20,
            color=(255, 255, 255),
            pos=pos,
        )

    def render(self, surface: pygame.surface.Surface):
        """Renders the crane scene and its children.

        Also draws some stats at the top of the screen

        Args:
            surface (Surface): the surface to render to.
        """
        super().render(surface)

        spent = get_total_spent()
        won = get_total_won()
        ratio = 1 if spent == 0 else won / spent

        # Bunch of text
        self._draw_stat_text(
            surface,
            text=f'Unique Pokemon: {get_unique_prizes()} / {len(get_prize_names())}',
            pos=(10, 0),
        )
        self._draw_stat_text(
            surface,
            text=f'Total Pokemon: {get_total_prizes()}',
            pos=(10, 40),
        )
        self._draw_stat_text(
            surface,
            text=f'Spent: ${get_total_spent():.2f}',
            pos=(300, 0),
        )
        self._draw_stat_text(
            surface,
            text=f'Won: ${get_total_won():.2f}',
            pos=(300, 40),
        )
        self._draw_stat_text(
            surface,
            text=f'Ratio: {ratio:.2f}',
            pos=(300, 80),
        )
