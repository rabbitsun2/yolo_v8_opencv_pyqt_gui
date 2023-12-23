# Project: pixmapTest 프로젝트(pyQt, urllib, OpenCV 적용)
# Filename: pixmapTest.py
# Created Date: 2023-11-15(수)
# Author: 대학원생 석사과정 정도윤(2학기)
# Description:
# 1. 
#
# Reference:
# 1. CCTV 출처 (충청남도 천안시 교통관제CCTV) - 데이터정보포털(data.go.kr)
#
import cv2
import datetime
from time import sleep
from threading import Thread, Event
import sys
import urllib.request
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5 import QtGui
from ultralytics import YOLO

form_class = uic.loadUiType("pixmapTest.ui")[0]

class WindowClass(QMainWindow, form_class):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btn_loadFromStart.clicked.connect(self.loadImageFromStart)
        self.btn_loadFromStop.clicked.connect(self.loadImageFromStop)
        self.btn_loadFromWeb.clicked.connect(self.loadImageFromWeb)
        self.btn_loadFromImage.clicked.connect(self.loadImageFromImage)
        self.btn_savePicture.clicked.connect(self.saveImageFromWeb)

    def run(self):

        CONFIDENCE_THRESHOLD = 0.6
        GREEN = (0, 255, 0)
        WHITE = (255, 255, 255)

        coco128 = open('classes_fire.txt', 'r')
        data = coco128.read()
        class_list = data.split('\n')
        coco128.close()

        model = YOLO('best.pt')

        cap = cv2.VideoCapture("rtsp://210.99.70.120:1935/live/cctv001.stream")
        #cap = cv2.VideoCapture(0)
        #cap = cv2.imread("apple2.jpg")
        #cap = cv2.VideoCapture("sample4.avi")
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        while self.running:
            start = datetime.datetime.now()

            ret, img = cap.read()

            detection = model(img)[0]

            if ret:

                # lbl_picture 크기 얻기
                label_width = self.lbl_picture.width()
                label_height = self.lbl_picture.height()

                for data in detection.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
                    confidence = float(data[4])
                    if confidence < CONFIDENCE_THRESHOLD:
                        continue

                    xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
                    label = int(data[5])
                    cv2.rectangle(img, (xmin, ymin), (xmax, ymax), GREEN, 2)
                    cv2.putText(img, class_list[label]+' '+str(round(confidence, 2)) + '%', (xmin, ymin), cv2.FONT_ITALIC, 1, WHITE, 2)

                end = datetime.datetime.now()

                total = (end - start).total_seconds()
                print(f'Time to process 1 frame: {total * 1000:.0f} milliseconds')

                # Resize 이미지 조절
                img = cv2.resize(img, (label_height, label_height))

                fps = f'FPS: {1 / total:.2f}'
                cv2.putText(img, fps, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                h,w,c = img.shape
                qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(qImg)
                self.lbl_picture.setPixmap(pixmap)
            else:
                QtWidgets.QMessageBox.about(self, "Error", "Cannot read frame.")
                print("cannot read frame.")
                break

        cap.release()
        print("Thread end.")


    def start(self):
        self.running = True
        th = Thread(target=self.run)
        th.start()
        print("started..")

    def stop(self):
        self.running = False
        print("stopped..")


    def loadImageFromStart(self):
        #QPixmap 객체 생성 후 이미지 파일을 이용하여 QPixmap에 사진 데이터 Load하고, Label을 이용하여 화면에 표시
        #self.qPixmapFileVar = QPixmap()
        #self.qPixmapFileVar.load("testImage.jpg")
        #self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(600)
        #self.lbl_picture.setPixmap(self.qPixmapFileVar)
        
        self.start()

    
    def loadImageFromStop(self):

        self.stop()


    def loadImageFromWeb(self) :

        #Web에서 Image 정보 로드
        urlString = "https://www.navercorp.com/img/ko/naver/img_spot_summary_v2.jpg"
        imageFromWeb = urllib.request.urlopen(urlString).read()

        #웹에서 Load한 Image를 이용하여 QPixmap에 사진데이터를 Load하고, Label을 이용하여 화면에 표시
        self.qPixmapWebVar = QPixmap()
        self.qPixmapWebVar.loadFromData(imageFromWeb)
        self.qPixmapWebVar = self.qPixmapWebVar.scaledToWidth(600)
        self.lbl_picture.setPixmap(self.qPixmapWebVar)

    def loadImageFromImage(self) :

        CONFIDENCE_THRESHOLD = 0.6
        GREEN = (0, 255, 0)
        WHITE = (255, 255, 255)

        #coco128 = open('classes_apple_orange.txt', 'r')
        coco128 = open('classes_fire.txt', 'r')
        data = coco128.read()
        class_list = data.split('\n')
        coco128.close()

        model = YOLO('best.pt')

        #Web에서 Image 정보 로드
        img = cv2.imread("fire.jpg")
        
        detection = model(img)[0]

        for data in detection.boxes.data.tolist(): # data : [xmin, ymin, xmax, ymax, confidence_score, class_id]
            confidence = float(data[4])
            if confidence < CONFIDENCE_THRESHOLD:
                continue

            xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
            label = int(data[5])
            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), GREEN, 2)
            cv2.putText(img, class_list[label]+' '+str(round(confidence, 2)) + '%', (xmin, ymin), cv2.FONT_ITALIC, 1, WHITE, 2)

        # BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # lbl_picture 크기 얻기
        label_width = self.lbl_picture.width()
        label_height = self.lbl_picture.height()

        # Resize 이미지 조절
        img = cv2.resize(img, (label_height, label_height))
        

        h,w,c = img.shape
        qImg = QtGui.QImage(img.data, w, h, w*c, QtGui.QImage.Format_RGB888)

        pixmap = QtGui.QPixmap.fromImage(qImg)
        
        self.lbl_picture.setPixmap(pixmap)

    def saveImageFromWeb(self) :
        #Label에서 표시하고 있는 사진 데이터를 QPixmap객체의 형태로 반환받은 후, save함수를 이용해 사진 저장
        self.qPixmapSaveVar = self.lbl_picture.pixmap()
        self.qPixmapSaveVar.save("SavedImage.jpg")

    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # 멀티쓰레드를 종료하는 stop 메소드를 실행함
            self.stop()
            event.accept()
        else:
            event.ignore()

if __name__ == "__main__" :
    event = Event()
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_() 
    event.set()