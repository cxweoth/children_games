# view.py
import os
import time
import pygame

class GameView:
    def __init__(self, screen, model, img_path):
        self.screen = screen
        self.model = model

        # 加载图像
        self.background_img = pygame.image.load(os.path.join(img_path, 'faded_background.png'))
        self.background_img = pygame.transform.scale(self.background_img, (model.screen_width, model.screen_height))
        self.mosquito_img = pygame.image.load(os.path.join(img_path, 'mosquito.png'))
        self.mosquito_img = pygame.transform.scale(self.mosquito_img, (100, 100))
        self.hand_img = pygame.image.load(os.path.join(img_path, 'hand.png'))
        self.hand_img = pygame.transform.scale(self.hand_img, (200, 200))
        self.start_button_normal_img = pygame.image.load(os.path.join(img_path, 'start_button.png'))
        self.start_button_normal_img = pygame.transform.scale(self.start_button_normal_img, (220, 220))
        self.start_button_hover_img = pygame.image.load(os.path.join(img_path, 'start_button_hover.png'))
        self.start_button_hover_img = pygame.transform.scale(self.start_button_hover_img, (220, 220))

        # 设置开始按钮位置
        self.start_button_rect = self.start_button_normal_img.get_rect()
        self.start_button_rect.center = (model.screen_width // 2, model.screen_height // 2)

    def update(self, game_started, mosquitoes, game_over):
        self.game_started = game_started
        self.mosquitoes = mosquitoes
        self.game_over = game_over
        self.draw()

    def draw(self):
        if not self.game_started:
            self.screen.fill((255, 255, 255))
            mouse_pos = pygame.mouse.get_pos()
            button_img = self.start_button_hover_img if self.start_button_rect.collidepoint(mouse_pos) else self.start_button_normal_img
            self.screen.blit(button_img, self.start_button_rect.topleft)
        else:
            self.screen.blit(self.background_img, (0, 0))
            for mosquito in self.mosquitoes:
                self.screen.blit(self.mosquito_img, mosquito)

        hand_pos = pygame.mouse.get_pos()
        hand_pos = (hand_pos[0] - 100, hand_pos[1] - 100)
        pygame.mouse.set_visible(False)
        self.screen.blit(self.hand_img, hand_pos)

        pygame.display.flip()

    def show_game_over_screen(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 55)
        text = font.render('Game Over!', True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.model.screen_width // 2, self.model.screen_height // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()
        time.sleep(3)