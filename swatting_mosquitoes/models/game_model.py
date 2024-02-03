# models/game_model.py

import random
import time

class GameModel:
    
    def __init__(self, screen_width, screen_height, game_duration, max_mosquitoes):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.game_duration = game_duration
        self.max_mosquitoes = max_mosquitoes

        self.mosquitoes = []
        self.game_started = False
        self.game_over = False
        self.start_time = None
        self.time_left = game_duration
        self.score = 0  # 添加分数追踪
        self.last_mosquito_added = time.time()
        self.high_scores = []  # 用于存储分数
        
    def reset_game(self):
        self.mosquitoes = []
        self.game_started = False
        self.game_over = False
        self.start_time = None
        self.time_left = self.game_duration
        self.score = 0
        self.last_mosquito_added = time.time()

    def add_mosquito(self):
        if len(self.mosquitoes) < self.max_mosquitoes:
            x = random.randint(0, self.screen_width - 100)
            y = random.randint(0, self.screen_height - 100)
            self.mosquitoes.append([x, y])

    def update(self):
        # 檢查遊戲時間
        if self.game_started and not self.game_over:
            if self.start_time is None:
                self.start_time = time.time()
            else:
                self.time_left = self.game_duration - (time.time() - self.start_time)
                if self.time_left <= 0:
                    self.end_game()

            # 每隔一段時間添加一隻新蚊子
            if time.time() - self.last_mosquito_added > 1:
                self.add_mosquito()
                self.last_mosquito_added = time.time()

    def start_game(self):
        self.game_started = True
        self.game_over = False
        self.mosquitoes.clear()
        self.start_time = None
        self.time_left = self.game_duration

    def check_mosquito_hit(self, hand_pos):
        hand_rect = (hand_pos[0]-80, hand_pos[1]-80, 80, 80)
        for m in self.mosquitoes:
            if self._colliderect(m, hand_rect):
                self.score += 10  # 每打中一隻蚊子加 10 分
        self.mosquitoes[:] = [m for m in self.mosquitoes if not self._colliderect(m, hand_rect)]

    def _colliderect(self, mosquito, hand_rect):
        mosquito_rect = (mosquito[0], mosquito[1], 100, 100)
        return self._rect_overlap(mosquito_rect, hand_rect)

    def _rect_overlap(self, rect_a, rect_b):
        ax1, ay1, aw, ah = rect_a
        ax2, ay2 = ax1 + aw, ay1 + ah
        bx1, by1, bw, bh = rect_b
        bx2, by2 = bx1 + bw, by1 + bh
        return ax1 < bx2 and ax2 > bx1 and ay1 < by2 and ay2 > by1
    
    def end_game(self):
        self.game_over = True

    def save_score(self, name):
        self.high_scores.append((name, self.score))
        self.high_scores.sort(key=lambda x: x[1], reverse=True)  # 根据分数排序
        # only keep top 10 scores
        self.high_scores = self.high_scores[:10]
