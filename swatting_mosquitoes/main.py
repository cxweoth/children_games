# main.py
import os
import pygame
from models import GameModel
from views import GameView
from presenters import GamePresenter
from settings import *

def main():
    # get root path
    root_path = os.path.dirname(__file__)

    # set img path
    img_path = os.path.join(root_path, "assets", "img")

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(GAME_CAPTION)

    model = GameModel(SCREEN_WIDTH, SCREEN_HEIGHT, GAME_DURATION, MAX_MOSQUITOES)
    view = GameView(screen, model, img_path)
    presenter = GamePresenter(model, view)

    presenter.run_game_loop()

if __name__ == "__main__":
    main()
