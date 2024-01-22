import pygame
import random
import time

# 初始化 Pygame
pygame.init()

# 設置遊戲視窗
screen_width, screen_height = 700, 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('打蚊子遊戲')

# 載入背景圖片
background_img = pygame.image.load('background.png')  # 確保將 'background.png' 替換為你的背景圖片文件名
# 得到圖案的長寬
background_width, background_height = background_img.get_size()
# 根據圖案根據視窗大小調整圖案大小
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

# 載入並調整蚊子圖片大小
mosquito_img = pygame.image.load('mosquito.png')
mosquito_img = pygame.transform.scale(mosquito_img, (100, 100))

# 載入手的圖片
hand_img = pygame.image.load('hand.png')
hand_img = pygame.transform.scale(hand_img, (200, 200))  # 根據需要調整手的大小

# 蚊子列表
max_mosquitoes = 10
mosquitoes = []

# 添加蚊子的函數
def add_mosquito():
    x = random.randint(0, screen_width - 100)
    y = random.randint(0, screen_height - 100)
    mosquitoes.append([x, y])

# 遊戲主循環
running = True
last_mosquito_added = time.time()

while running:
    # 繪製背景圖片
    screen.blit(background_img, (0, 0))
    # screen.fill((255, 255, 255))  # 清屏為白色

    # 每隔一段時間添加一隻新蚊子
    if time.time() - last_mosquito_added > 1:  # 每隔1秒添加一隻蚊子
        if len(mosquitoes) < max_mosquitoes:
            add_mosquito()
        last_mosquito_added = time.time()

    # 獲取當前鼠標位置並調整手的位置
    hand_pos = pygame.mouse.get_pos()
    hand_pos = (hand_pos[0] - 100, hand_pos[1] - 100)  # 調整手的位置以符合實際的中心點

    # 檢查事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 檢查是否打中任何一隻蚊子
            hand_rect = pygame.Rect(hand_pos[0]+70, hand_pos[1]+70, 80, 80)
            mosquitoes[:] = [m for m in mosquitoes if not hand_rect.colliderect(pygame.Rect(m[0], m[1], 100, 100))]

    # 繪製所有蚊子
    for m in mosquitoes:
        screen.blit(mosquito_img, m)

    # 隱藏標準游標並顯示手的圖片
    pygame.mouse.set_visible(False)
    screen.blit(hand_img, hand_pos)

    # 更新屏幕
    pygame.display.flip()

pygame.quit()
