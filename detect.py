import cv2
import os
import torch
from PyQt5.QtGui import QImage, QPixmap
from torchvision import models
from torch import nn
import matplotlib.pyplot as plt
import numpy as np


def detect(model, path):
    results = model(path)
    # 提取检测结果的边界框、置信度和类别
    boxes = results.xyxy[0][:, :4].tolist()
    confidences = results.xyxy[0][:, 4].tolist()
    class_ids = results.xyxy[0][:, 5].tolist()

    print(boxes)
    print(class_ids)

    result_report = ''
    red_sum = 0
    green_sum = 0
    flag = 0
    new_class = []
    side = len(class_ids)
    if side == 0:
        result_report = '没有任何红绿灯'
    elif side == 1:
        if class_ids[0] == 0:
            result_report = '红灯！！ 禁止通行'
            red_sum += 1
        elif class_ids[0] == 1:
            result_report = '绿灯， 允许通行'
            green_sum += 1
        elif class_ids[0] == 2:
            result_report = '黄等， 请等一等'

    else:
        for item in class_ids:
            if item == 0:
                red_sum += 1
            if item == 1:
                green_sum += 1
            if item == 1 or item == 0:
                flag += 1
                new_class.append(item)
            else:
                continue

    if flag == 0 and side > 1:
        result_report = '红绿灯没有灯，无法分析'
    elif flag == 1 and side > 1:
        if new_class[0] == 0:
            result_report = '红灯！！ 禁止通行'
        elif new_class[0] == 1:
            result_report = '绿灯， 允许通行'
        elif new_class[0] == 2:
            result_report = '黄等， 请等一等'
    elif flag > 1 and side > 1:
        if new_class[0] == 0 and new_class[1] == 0:
            result_report = '均红灯！！ 禁止通行'
        elif new_class[0] == 1 and new_class[1] == 0:
            result_report = '左转(变道)绿灯， 允许通行\n直行红灯， 禁止通行'
        elif new_class[0] == 0 and new_class[1] == 1:
            result_report = '左转(变道)红灯， 禁止通行\n直行绿灯， 允许通行'
        elif new_class[0] == 1 and new_class[1] == 1:
            result_report = '均绿灯， 允许通行'

    output_image = results.render()[0]

    # 将图像数据转换为QPixmap格式
    h, w, c = output_image.shape
    q_image = QImage(output_image.data, w, h, c * w, QImage.Format_RGB888)
    q_pixmap = QPixmap.fromImage(q_image)

    result_report = '红灯个数： ' + str(red_sum) + '\n绿灯个数： ' + str(green_sum) + '\n' + result_report
    return q_pixmap, result_report
