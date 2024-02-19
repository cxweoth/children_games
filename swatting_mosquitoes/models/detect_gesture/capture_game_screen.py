import cv2
import numpy as np

def capture_game_screen():
    cap = cv2.VideoCapture(0)  # 打开摄像头

    # 根据实际情况可能需要调整这些阈值
    canny_lower_threshold = 50
    canny_upper_threshold = 150

    while True:
        ret, frame = cap.read()
        if not ret:
            print("无法接收帧，退出中...")
            break

        # 将图像转换为灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # 应用高斯模糊，消除噪声
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # 应用 Canny 边缘检测
        edges = cv2.Canny(blurred, canny_lower_threshold, canny_upper_threshold)

        # 找到边缘的轮廓
        contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # 假设游戏画面是最大的轮廓
        if len(contours) > 0:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # 画出游戏画面的边界
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # 显示原始图像和边缘检测结果
        cv2.imshow('Frame', frame)
        cv2.imshow('Edges', edges)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

capture_game_screen()
