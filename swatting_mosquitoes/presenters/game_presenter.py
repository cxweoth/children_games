# presenter.py
import pygame

class GamePresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run_game_loop(self):
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_button_down(event)

            self.model.update()
            self.view.update(self.model.game_started, self.model.mosquitoes, 
                             self.model.game_over, self.model.time_left, 
                             self.model.score)

            if self.model.game_over:
                self.view.show_game_over_screen()
                player_name = self.view.get_player_name()
                self.model.save_score(player_name)
                self.view.show_high_scores()
                self.model.reset_game()

        pygame.quit()

    def handle_mouse_button_down(self, event):
        if not self.model.game_started and self.view.start_button_rect.collidepoint(event.pos):
            self.model.start_game()
            self.view.background_img.set_alpha(180)
        elif self.model.game_started:
            self.model.check_mosquito_hit(event.pos)
