import sys

import cv2
import torch
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from torchvision.transforms import ToTensor

from hand_view import Ui_MainWindow
import detect


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.medio = 'img'
        self.setupUi(self)
        self.bind_slots()
        # 加载yolov5模型（本地训练好的）
        self.mode = torch.hub.load('../yolov5', 'custom', path='../yolov5/runs/train/traffic6/weights/best.pt',
                                   source='local')
        self.mode.eval()
        self.mode.conf = 0.7  # 置信度
        print("yolov5模型加载完成")
        self.result_img = None
        self.report = None
        self.flag = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_label)
        self.timer.start(100)

    # 信号槽函数
    def btn_open_img(self):
        print("点击按钮")
        file_path, _ = QFileDialog.getOpenFileName(self, directory="./img",
                                                   filter="Image Files (*.png *.jpeg *.jpg *.JPG *.mp4)")

        self.medio = 'img' if self.radioButton.isChecked() else 'video'

        if file_path and self.medio == 'img':
            # 选择图片
            print(file_path)

            result_img, report = detect.detect(self.mode, file_path)
            print(result_img.size())
            self.label_2.setPixmap(result_img)
            # 显示检测结果
            self.label_3.setText(report)

        if file_path and self.medio == 'video':
            # 选择图片
            print(file_path)
            cap = cv2.VideoCapture(file_path)

            while cap.isOpened():
                ret, frame = cap.read()

                if not ret:
                    break

                cv2.imwrite('result.jpg', frame)
                self.result_img, self.report = detect.detect(self.mode, 'result.jpg')
                self.flag = 1
                self.label_2.setPixmap(self.result_img)
                # 显示检测结果
                self.label_3.setText(self.report)
        self.flag = 0

    def update_label(self):
        if self.medio == 'video' and self.flag == 1:
            print("-------------------------------------------------------------")
            self.label_2.setPixmap(self.result_img)
            self.label_3.setText(self.report)

    # 绑定槽
    def bind_slots(self):
        self.pushButton.clicked.connect(self.btn_open_img)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
