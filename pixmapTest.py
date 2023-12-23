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
from time import sleep
from threading import Thread, Event
import sys
import urllib.request
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5 import QtGui

form_class = uic.loadUiType("pixmapTest.ui")[0]

class WindowClass(QMainWindow, form_class) :
    def __init__(self) :
        super().__init__()
        self.setupUi(self)

        self.btn_loadFromFile.clicked.connect(self.loadImageFromFile)
        self.btn_loadFromWeb.clicked.connect(self.loadImageFromWeb)
        self.btn_savePicture.clicked.connect(self.saveImageFromWeb)

    def run(self):

        cap = cv2.VideoCapture("rtsp://210.99.70.120:1935/live/cctv001.stream")
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        while self.running:

            ret, img = cap.read()

            if ret:

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

    def stop(self):
        self.running = False
        print("stoped..")

    def start(self):
        self.running = True
        th = Thread(target=self.run)
        th.start()
        print("started..")


    def loadImageFromFile(self):
        #QPixmap 객체 생성 후 이미지 파일을 이용하여 QPixmap에 사진 데이터 Load하고, Label을 이용하여 화면에 표시
        #self.qPixmapFileVar = QPixmap()
        #self.qPixmapFileVar.load("testImage.jpg")
        #self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(600)
        #self.lbl_picture.setPixmap(self.qPixmapFileVar)
        
        self.start()


    def loadImageFromWeb(self) :

        #Web에서 Image 정보 로드
        urlString = "https://www.navercorp.com/img/ko/naver/img_spot_summary_v2.jpg"
        imageFromWeb = urllib.request.urlopen(urlString).read()

        #웹에서 Load한 Image를 이용하여 QPixmap에 사진데이터를 Load하고, Label을 이용하여 화면에 표시
        self.qPixmapWebVar = QPixmap()
        self.qPixmapWebVar.loadFromData(imageFromWeb)
        self.qPixmapWebVar = self.qPixmapWebVar.scaledToWidth(600)
        self.lbl_picture.setPixmap(self.qPixmapWebVar)

    def saveImageFromWeb(self) :
        #Label에서 표시하고 있는 사진 데이터를 QPixmap객체의 형태로 반환받은 후, save함수를 이용해 사진 저장
        self.qPixmapSaveVar = self.lbl_picture.pixmap()
        self.qPixmapSaveVar.save("SavedImage.jpg")

if __name__ == "__main__" :
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_() 