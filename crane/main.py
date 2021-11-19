import pygame
from crane.engine.display import Display
from crane.engine.engine import Engine
from crane.game.resources import ICON
from crane.game.resources import save_config
from crane.game.scene.game import Game


TARGET_FPS = 60
TARGET_UPS = 60


def main():
    # Set up display, used to draw on
    display = Display("Kelly's Favorite Game :)")
    pygame.display.set_icon(ICON)

    # Set up engine, used to handle game logic/timing
    engine = Engine(display, TARGET_FPS, TARGET_UPS)
    engine.scene = Game()
    engine.start()

    # Save & quit
    save_config()
    pygame.quit()


if __name__ == '__main__':
    main()
