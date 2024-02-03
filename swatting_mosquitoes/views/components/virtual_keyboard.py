import pygame

class VirtualKeyboard:
    
    def __init__(self, screen, font, x, y):
        self.screen = screen
        self.font = font
        self.x = x
        self.y = y
        self.keys = [
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L'],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M'],
            ['BACK', 'ENTER']  # 单独的行
        ]
        self.key_size = 40
        self.key_spacing = 10
        self.special_key_width = self.key_size * 2 + self.key_spacing  # 特殊键的宽度

    def draw(self):
        for row_index, row in enumerate(self.keys):
            x_offset = 0
            for col_index, key in enumerate(row):
                key_width = self.special_key_width if key in ['BACK', 'ENTER'] else self.key_size
                key_x = self.x + x_offset
                key_y = self.y + row_index * (self.key_size + self.key_spacing)
                pygame.draw.rect(self.screen, (255, 255, 255), (key_x, key_y, key_width, self.key_size))
                text_surface = self.font.render(key, True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(key_x + key_width / 2, key_y + self.key_size / 2))
                self.screen.blit(text_surface, text_rect)

                x_offset += key_width + self.key_spacing

    def get_key(self, mouse_pos):
        for row_index, row in enumerate(self.keys):
            x_offset = 0
            for col_index, key in enumerate(row):
                key_width = self.special_key_width if key in ['BACK', 'ENTER'] else self.key_size
                key_x = self.x + x_offset
                key_y = self.y + row_index * (self.key_size + self.key_spacing)
                key_rect = pygame.Rect(key_x, key_y, key_width, self.key_size)

                if key_rect.collidepoint(mouse_pos):
                    return key

                x_offset += key_width + self.key_spacing

        return None
        
