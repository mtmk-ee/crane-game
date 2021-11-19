from crane.engine.scene.scene import PhysicsScene
from crane.engine.scene.scene_object import UpdateableSceneObject
from crane.game.scene.crane_scene.prize_object import PrizeObject


class PrizeAdder(UpdateableSceneObject):

    def __init__(self, scene: PhysicsScene):
        """An invisible scene object that adds prizes to the game
        over time.

        Args:
            scene (PhysicsScene): the scene to add the prizes to.
        """
        super(PrizeAdder, self).__init__()
        self._scene = scene

        self._num_prizes = 0 # number of prizes left to add

        self._interval = 0.05 # how long to wait between prizes
        self._countdown = 0 # time since last prize added
        self._running = False

    def add_prizes(self, num_prizes: int):
        """Adds the given number of prizes to the scene.

        Args:
            num_prizes (int): the number of prizes.
        """
        self._running = True
        self._num_prizes += num_prizes

    def update(self, dt: float):
        """Handles adding prizes over time.

        Args:
            dt (float): time since last update.
        """
        if self._running:
            self._countdown -= dt

            # Add prize if we waited long enough
            if self._countdown <= 0:
                self._num_prizes -= 1
                self._scene.add(PrizeObject(self._scene._world))
                self._countdown = self._interval

            # Stop adding prizes if there's none left
            if self._num_prizes == 0:
                self._running = False
                self._countdown = 0
