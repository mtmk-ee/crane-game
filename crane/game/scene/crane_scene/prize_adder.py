from crane.engine.scene.scene import PhysicsScene
from crane.engine.scene.scene_object import UpdateableSceneObject
from crane.game.scene.crane_scene.prize_object import PrizeObject


class PrizeAdder(UpdateableSceneObject):

    def __init__(self, scene: PhysicsScene):
        super(PrizeAdder, self).__init__()
        self._scene = scene
        self._num_prizes = 0
        self._running = False
        self._prizes_added = 0
        self._interval = 0.05
        self._countdown = 0

    def add_prizes(self, num_prizes: int):
        self._running = True
        self._num_prizes += num_prizes

    def update(self, dt: float):
        if self._running:
            self._countdown -= dt
            if self._countdown <= 0:
                self._num_prizes -= 1
                self._scene.add(PrizeObject(self._scene._world))
                self._countdown = self._interval

            if self._num_prizes == 0:
                self._running = False
                self._countdown = 0
