import sys
import cv2
import torch
from PyQt5.QtCore import QTimer, QThread, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt5.QtGui import QPixmap
from hand_view import Ui_MainWindow
import detect


class ImageProcessingThread(QThread):
    result_updated = pyqtSignal(object, str)

    def __init__(self, mode, file_path):
        super().__init__()
        self.mode = mode
        self.file_path = file_path

    def run(self):
        if self.file_path.endswith(('.png', '.jpeg', '.jpg', '.JPG')):
            result_img, report = detect.detect(self.mode, self.file_path)
            self.result_updated.emit(result_img, report)  # 触发信号
        elif self.file_path.endswith('.mp4'):
            cap = cv2.VideoCapture(self.file_path)
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                cv2.imwrite('result.jpg', frame)
                result_img, report = detect.detect(self.mode, 'result.jpg')
                self.result_updated.emit(result_img, report)
                cv2.waitKey(100)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # self.medio = 'img'
        self.setupUi(self)
        self.bind_slots()
        # 加载yolov5模型（本地训练好的）
        self.mode = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')
        self.mode.eval()
        self.mode.conf = 0.7  # 置信度
        print("yolov5模型加载完成")
        self.flag = False
        self.thread = None

    def btn_open_img(self):
        print("点击按钮")
        file_path, _ = QFileDialog.getOpenFileName(self, directory="./img",
                                                   filter="Image Files (*.png *.jpeg *.jpg *.JPG *.mp4)")
        # self.medio = 'img' if self.radioButton.isChecked() else 'video'
        if file_path:
            if self.thread is not None and self.thread.isRunning():
                # 如果有正在运行的线程，先停止它
                self.thread.quit()
                self.thread.wait()
            self.thread = ImageProcessingThread(self.mode, file_path)
            self.thread.result_updated.connect(self.update_labels)
            self.thread.start()

    def update_labels(self, result_img, report):
        self.label_2.setPixmap(result_img)
        self.label_3.setText(report)

    def bind_slots(self):
        self.pushButton.clicked.connect(self.btn_open_img)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
