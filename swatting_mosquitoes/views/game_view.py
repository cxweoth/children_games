# view.py
import os
import time
import pygame
from .components.virtual_keyboard import VirtualKeyboard

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

        # 设置字体用于显示时间
        self.font = pygame.font.SysFont(None, 36)

        self.virtual_keyboard = VirtualKeyboard(screen, self.font, 100, model.screen_height // 3 + 50)

    def update(self, game_started, mosquitoes, game_over, time_left, score):
        self.game_started = game_started
        self.mosquitoes = mosquitoes
        self.game_over = game_over
        self.time_left = time_left
        self.score = score
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

        if self.game_started and not self.game_over:
            # 显示时间
            time_text = self.font.render(f"Time: {int(self.time_left)}", True, (255, 255, 255))
            self.screen.blit(time_text, (10, 10))  # 将时间文本渲染在屏幕的左上角
            # 显示分数
            score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 40))  # 将分数文本渲染在屏幕左上角，下方时间

        pygame.display.flip()

    def show_game_over_screen(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 55)

        # 游戏结束文本
        game_over_text = font.render('Game Over!', True, (255, 255, 255))
        game_over_rect = game_over_text.get_rect(center=(self.model.screen_width // 2, self.model.screen_height // 2 - 30))
        self.screen.blit(game_over_text, game_over_rect)

        # 分数文本
        score_text = font.render(f"Score: {self.model.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(self.model.screen_width // 2, self.model.screen_height // 2 + 30))
        self.screen.blit(score_text, score_rect)

        pygame.display.flip()
        time.sleep(3)  # 显示3秒结束画面后退出

    def get_player_name(self):
        # 创建一个输入框供玩家输入名字
        input_box = pygame.Rect(self.model.screen_width // 2 - 100, self.model.screen_height // 3, 200, 32)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        font = pygame.font.Font(None, 32)
        done = False

        pygame.mouse.set_visible(True)
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = True
                    else:
                        key = self.virtual_keyboard.get_key(event.pos)
                        if key:
                            if key == 'BACK':
                                text = text[:-1]
                            elif key == 'ENTER':
                                done = True  # 当用户点击 Enter 键时完成输入
                            else:
                                text += key
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode

            self.screen.fill((30, 30, 30))
            txt_surface = font.render(text, True, color)
            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            self.screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pygame.draw.rect(self.screen, color, input_box, 2)
            self.virtual_keyboard.draw()  # 绘制虚拟键盘

            pygame.display.flip()
        return text
    
    def show_high_scores(self):
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont(None, 36)

        title = font.render("High Scores", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.model.screen_width // 2, self.model.screen_height // 3 - 40))
        self.screen.blit(title, title_rect)

        start_y = self.model.screen_height // 3 # 排行榜开始的 Y 坐标
        for i, score in enumerate(self.model.high_scores[:10]):  # 显示前10名
            text = font.render(f"{i+1}. {score[0]}: {score[1]}", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.model.screen_width // 2, start_y + i * 30))
            self.screen.blit(text, text_rect)

        pygame.display.flip()
        pygame.time.wait(5000)  # 显示5秒