#!/usr/bin/python3
import cv2 as cv
import os
import numpy as np


# Canny边缘检测
def canny(src):
    # 1. 转化灰度图
    gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)

    # 2. 高斯滤波
    blur = cv.GaussianBlur(gray, (3, 3), 0)

    # 3. Canny处理
    canny = cv.Canny(blur, 0, 200, 3)
    cv.imshow("canny", canny)
    cv.waitKey()

    return canny


# 增强版(Sobel)边缘检测
def scharr(src):
    # 1. 计算图片梯度
    # grad_x = cv.Sobel(src, cv.CV_64F, 1, 0)
    # grad_y = cv.Sobel(src, cv.CV_64F, 0, 1)
    grad_x = cv.Scharr(src, cv.CV_64F, 1, 0)
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
    blur = cv.GaussianBlur(gradxy, (3, 3), 0)  # 高斯滤波
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
    blur = cv.GaussianBlur(binary, (3, 3), 0)
    cv.imshow("binary_blur", blur)
    cv.waitKey()

    return blur


def laplacian(src):
    # 1. 高斯滤波
    blur = cv.GaussianBlur(src, (3, 3), 0)

    # 2. 转化灰度图
    gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)

    # 3. Laplacian处理
    laplacian = cv.Laplacian(gray, cv.CV_16S, 3)
    laplacian = cv.convertScaleAbs(laplacian)
    cv.imshow("laplacian", laplacian)
    cv.waitKey()

    return laplacian


def morphology(src):
    # 5. 形态学滤波：腐蚀和膨胀
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (24, 24))
    morphology = cv.morphologyEx(src, cv.MORPH_CLOSE, kernel)
    cv.imshow("morphology", morphology)
    cv.waitKey()

    _, binary = cv.threshold(morphology, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    cv.imshow("morphology_binary", binary)
    cv.waitKey()

    return binary


def findContours(img, src):
    # 1. 检测轮廓并找出最外围轮廓
    contours, _ = cv.findContours(src, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv.contourArea)
    contour = contours[-1]

    # 2. 根据最外围轮廓生成mask
    mask = np.zeros(src.shape[0:2], np.uint8)
    mask = cv.drawContours(mask, contours, -1, (255, 255, 255), cv.FILLED)
    cv.imshow("mask", mask)
    cv.waitKey()

    # 3. 利用mask生成透明背景图片
    new_img = cv.cvtColor(img, cv.COLOR_BGR2BGRA)
    new_img[:, :, 3] = mask

    # 4. 截取最外围轮廓生成图片
    x, y, w, h = cv.boundingRect(contour)
    result = new_img[y : y + h, x : x + w]
    cv.imshow("result", result)
    cv.waitKey()

    # 5. 保存图片
    cv.imwrite("result.png", result)

    f = open("path.svg", "w+")
    f.write(
        '<svg width="'
        + str(w)
        + '" height="'
        + str(h)
        + '" xmlns="http://www.w3.org/2000/svg">'
    )
    f.write('<path d="M')

    for i in range(len(contour)):
        x1, y1 = contour[i][0]
        f.write(str(x1 - x) + " " + str(y1 - y) + " ")
    f.write('"/>')
    f.write("</svg>")
    f.close()


if __name__ == "__main__":
    src = cv.imread("./src/images/mask.jpeg")
    # src = cv.imread("./src/images/pikachu.jpeg")
    # src = cv.imread("./src/images/computer.jpeg")
    # src = cv.imread("./src/images/user.jpeg")

    img1 = canny(src)
    img2 = morphology(img1)
    findContours(src, img2)
