#!/usr/bin/python3
import cv2 as cv
import os
import numpy as np


def demo(src):
    img = src.copy()
    cv.imshow("img", img)
    cv.waitKey()

    # # 1. Canny边缘检测
    # canny = cv.Canny(src, 0, 255)
    # cv.imshow("canny", canny)
    # cv.waitKey()

    # 1. 边缘处理
    # 计算图片梯度
    # grad_x = cv.Sobel(src, cv.CV_64F, 1, 0)
    # grad_y = cv.Sobel(src, cv.CV_64F, 0, 1)
    grad_x = cv.Scharr(src, cv.CV_64F, 1, 0)  # 增强版（Sobel）图像
    grad_y = cv.Scharr(src, cv.CV_64F, 0, 1)
    gradx = cv.convertScaleAbs(grad_x)  # 转变
    grady = cv.convertScaleAbs(grad_y)
    gradxy = cv.addWeighted(gradx, 0.5, grady, 0.5, 0)
    cv.imshow("gradient", gradxy)
    cv.waitKey()

    # 2. 平滑处理
    # 均值滤波或者高斯滤波
    # blur = cv.blur(gradxy, (3, 3))
    # blur = cv.blur(blur, (3, 3))
    blur = cv.GaussianBlur(gradxy, (7, 7), 0)  # 高斯滤波
    # blur = cv.blur(blur, (3, 3))
    cv.imshow("gradient_blur", blur)
    cv.waitKey()

    # 3. 转化灰度图
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)
    cv.imshow("gray", gray)
    cv.waitKey()

    # 4. 阈值化
    _, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    cv.imshow("binary", binary)
    cv.waitKey()

    # 5. 平滑处理
    binary = cv.blur(binary, (3, 3))
    blur = cv.GaussianBlur(binary, (7, 7), 0)
    cv.imshow("binary_blur", blur)
    cv.waitKey()

    # 6. 形态学滤波：腐蚀和膨胀
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (24, 24))
    morphology = cv.morphologyEx(blur, cv.MORPH_CLOSE, kernel)
    cv.imshow("morphology", morphology)
    cv.waitKey()

    # 7. 检测轮廓并找出最外围轮廓
    contours, _ = cv.findContours(morphology, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv.contourArea)
    contour = contours[-1]

    # 8. 根据最外围轮廓生成mask
    mask = np.zeros(src.shape[0:2], np.uint8)
    mask = cv.drawContours(mask, contours, -1, (255, 255, 255), cv.FILLED)
    cv.imshow("mask", mask)
    cv.waitKey()

    # 9. 利用mask生成透明背景图片
    new_img = cv.cvtColor(img, cv.COLOR_BGR2BGRA)
    new_img[:, :, 3] = mask

    # 10. 截取最外围轮廓生成图片
    x, y, w, h = cv.boundingRect(contour)
    result = new_img[y : y + h, x : x + w]
    cv.imshow("result", result)
    cv.waitKey()

    # # 保存图片
    cv.imwrite("result.png", result)


if __name__ == "__main__":
    src = cv.imread("./src/images/sign.jpeg")
    # src = cv.imread("./pikachu.jpeg")
    # src = cv.imread("./computer.jpeg")
    # src = cv.imread("./lena.png")

    demo(src)
