import pygame
from crane.engine.display import Display
from crane.engine.engine import Engine
from crane.engine.scene.scene import PhysicsScene
from crane.engine.scene.scene_object import GroundObject
from crane.game.resources import ICON
from crane.game.resources import save_config
from crane.game.scene.crane_scene.container_object import ContainerObject
from crane.game.scene.crane_scene.prize_adder import PrizeAdder
from crane.game.scene.game import Game

pygame.font.init()


TARGET_FPS = 60
TARGET_UPS = 60

def main():
    display = Display("Kelly's Favorite Game :)")
    pygame.display.set_icon(ICON)
    engine = Engine(display, TARGET_FPS, TARGET_UPS)
    engine.scene = Game()
    engine.start()

    pygame.quit()

if __name__ == '__main__':
    main()
    save_config()
    pygame.quit()