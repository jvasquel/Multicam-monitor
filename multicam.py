
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function
from datetime import date
import datetime
from threading import Thread
from tkinter import N
from typing import Dict, List, Any
from collections import OrderedDict
from functools import partial
from PyQt5.QtGui import QFont, QIcon, QImage, QPixmap
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QLineEdit, QComboBox, QFileDialog, QStyleFactory, QHBoxLayout, QLabel, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget, QStatusBar, QTableWidget, QVBoxLayout, QTableWidgetItem, QHBoxLayout, QSplitter, QGroupBox, QFormLayout, QAction, QGridLayout, QShortcut
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5 import QtCore, Qt, QtGui
from PyQt5.QtCore import QRect, QSize, Qt, QUrl, QDir, QTime, pyqtSlot
from PyQt5.QtGui import QFont, QPixmap, QImage, QColor, QPainter, QPen, QKeySequence, QStandardItemModel

import os
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
import csv
from typing import Dict, List, Any
import sys
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import sys
import cv2
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
from PyQt5.QtWidgets import *

import numpy as np
import cv2
import os
import time
# implemets toaster style notifications
from toaster import QToaster

QT_QPA_PLATFORM_PLUGIN_PATH= "/venv/lib/python3.8/site-packages/cv2/qt/plugins/platforms"


from PyQt5.QtWidgets import *
from PyQt5.QtCore import (QThread, pyqtSignal, pyqtSlot, QSize, Qt, QTimer, QTime, QDate, QObject, QEvent)

os.environ['OPENCV_VIDEOIO_DEBUG']='1'
os.environ['OPENCV_VIDEOIO_PRIORITY_MAMF']='0'
audio_extensions = [".wav", ".mp3"]
video_extensions = [".avi", ".mp4", ".mkv"]
#Qlabel display
width, height = 480*6, 270*6
w = 1920//2 #960
h= 1080//2 #540
capture_delay =80


#-------------------------

class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self,parent:QWidget)-> None: 
        print('new window')
        QDialog.__init__(self,parent)
        self._run_flag = True
        self.flag2=False
        self.parent = parent
        self.link_2=self.parent.link_2
    def run(self):
        # capture from web cam

        cap = cv2.VideoCapture(self.link_2, cv2.CAP_FFMPEG)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
            if self.flag2:
                cap = cv2.VideoCapture(self.link)
                self.flag2= False
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()

# creating a class
# that inherits the QDialog class
class NewSource(QDialog):

	# constructor
    def __init__(self, parent:QWidget)-> None: 
        print('new window')
        QDialog.__init__(self,parent)
        self.parent = parent
		
		# creating a group box
        self.formGroupBox = QGroupBox("Ingrese los datos requeridos")
		# creating a line edit
        self.nameLineEdit = QLineEdit()
        self.nameLineEdit2 = QLineEdit()
		# calling the method that create the form
        self.createForm()
		# creating a dialog button for ok and cancel
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		# adding action when form is accepted
        self.buttonBox.accepted.connect(lambda:self.getInfo( ))
		# addding action when form is rejected
        self.buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
		# adding form group box to the layout
        mainLayout.addWidget(self.formGroupBox)
		# adding button box to the layout
        mainLayout.addWidget(self.buttonBox)
		# setting lay out
        self.setLayout(mainLayout)

	# get info method called when form is accepted
    # get info method called when form is accepted
    def getInfo(self):

		# printing the form information
        print("Person Name : {0}".format(self.nameLineEdit.text()))
        print("Direccion : {0}".format(self.nameLineEdit2.text())) 
        # create the video capture thread
        
        #self.parent.thread.link=self.nameLineEdit2.text()
        if self.parent.slot2 :
            self.parent.slot2.flag=False
        self.parent.link_2=self.nameLineEdit2.text()
        self.parent.slot2=Slot(self, index=17, cam_id=1, link=self.parent.link_2)
        self.parent.slot2.signal.connect(self.parent.update_image)
        self.parent.slot2.start()
        
        # start the thread
        #self.parent.thread.flag2=True
       
        self.nameLineEdit.clear()
        self.nameLineEdit2.clear()
        #Window.select_source(1,self.nameLineEdit2.text(),self.nameLineEdit2.text())
        #"http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4"
        # index id link active
        #self.parent.cameras[self.index] =[ tab2.nameLineEdit.text(), tab2.nameLineEdit2.text(), False]
		# closing the window
        self.close()
    
	# creat form method
    def createForm(self ):

		# creating a form layout
        layout = QFormLayout()

		# adding rows
		# for name and adding input text
        layout.addRow(QLabel("Identificador"), self.nameLineEdit)
        layout.addRow(QLabel("Direccion"), self.nameLineEdit2)
        

		# setting layout
        self.formGroupBox.setLayout(layout)
    def select_source (self,cam_id, link):
        print('select_source')
        slot = Slot(self,self.index, cam_id, link)
        slot.signal.connect(self.parent.ReadImage)
        self.parent.threads[self.index]=slot
        

        print('refresh')
        print("link")
        n=1
        slot.start()
        self.parent.refresh()



        
class Slot(QThread):
    print('slot')
    signal= pyqtSignal(np.ndarray, int, int, bool)

    def __init__(self, parent:QWidget, index: int, cam_id: int, link:str) -> None:
        print('init slot')
        QThread.__init__(self, parent)
        self.parent= parent
        self.index= index
        self.cam_id = cam_id
        self.scale = 1
        print('cam_id')
        self.link =link
        self.center_x = None
        self.center_y = None
        print(link)
        self.flag = True
        self.screens=False
        self.recording=False
    def run(self ) ->None:
        print('run')
        
        self.cap = cv2.VideoCapture(self.link)
        while self.cap.isOpened():
            has, im =self.cap.read()
            if not has: break
            if self.screens:
                self.take_screenshot(im) 

            if self.recording:
                self.output_video.write(im)

            if self.flag== False :
                print("close thread")
                break 
            
            if not self.scale == 1:
                im = self.__zoom(im)
            else:
                
                im= cv2.resize(im, (w,h))
            self.signal.emit(im, self.index, self.cam_id, True)
            cv2.waitKey(capture_delay) & 0xFF

        im= np.zeros((h,w,3), dtype= np.uint8)
        self.signal.emit(im, self.index, self.cam_id, False)
        cv2.waitKey(capture_delay) & 0xFF
    def take_screenshot(self,im):
        print ("Take screenshot")
        now = datetime.datetime.now()
        date = now.strftime('%Y%m%d')
        hour = now.strftime('%H%M%S')
        user_id = '00001'
        filename = './images/cvui_{}_{}_{}.png'.format(date, hour, user_id)
        
        cv2.imwrite(filename, im)
        self.screens=False
    def __zoom(self, img, center=None):
        # zoom하는 실제 함수
        height, width = img.shape[:2]
        if center is None:
            #   중심값이 초기값일 때의 계산
            center_x = int(width / 2)
            center_y = int(height / 2)
            radius_x, radius_y = int(width / 2), int(height / 2)
        else:
            #   특정 위치 지정시 계산
            rate = height / width
            center_x, center_y = center

            #   비율 범위에 맞게 중심값 계산
            if center_x < width * (1-rate):
                center_x = width * (1-rate)
            elif center_x > width * rate:
                center_x = width * rate
            if center_y < height * (1-rate):
                center_y = height * (1-rate)
            elif center_y > height * rate:
                center_y = height * rate

            center_x, center_y = int(center_x), int(center_y)
            left_x, right_x = center_x, int(width - center_x)
            up_y, down_y = int(height - center_y), center_y
            radius_x = min(left_x, right_x)
            radius_y = min(up_y, down_y)

        # 실제 zoom 코드
        radius_x, radius_y = int(self.scale * radius_x), int(self.scale * radius_y)

        # size 계산
        min_x, max_x = center_x - radius_x, center_x + radius_x
        min_y, max_y = center_y - radius_y, center_y + radius_y

        # size에 맞춰 이미지를 자른다
        cropped = img[min_y:max_y, min_x:max_x]
        # 원래 사이즈로 늘려서 리턴
        new_cropped = cv2.resize(cropped, (width, height))

        return new_cropped

##_-----------------------------------------------------

def clickable(widget):
    class Filter(QObject):
        clicked = pyqtSignal()
        def eventFilter(self,obj, event):
            if obj == widget:
                if event.type()== QEvent.MouseButtonRelease:
                    self.clicked.emit()
                    return True
            return False
    
    filter =Filter(widget)
    widget.installEventFilter(filter)
    return filter.clicked

###---------------------------------------------------------
#select thread IndexError
#inicialise slot
#replace slot
#change slot window
class NewWindow(QDialog):
    def __init__(self, parent:QWidget)-> None: 
        print('new window')
        QDialog.__init__(self,parent)
        self.parent = parent
        self.index: int =0

        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.label.setScaledContents(True)
        self.label.setFont(QFont("Times",30))
        self.label.setStyleSheet(
            "color: rgb(255,0,255);"
            "background-color: rgb(0,0,0);"
            "qproperty-alignment: AlignCenter;")

        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0) 
        #layout.SetSpacing(2)
        layout.addWidget(self.label)
        self.setLayout(layout)
        self.setWindowTitle('Camera{}'.format(self.index))
    
    def sizeHint(self) -> QSize:
        print('sizehint')
        return QSize (width//3, height//3)

    def resizeEvent(self, event) ->None:
        print('resizehint')
        self.update()
    
class Newform(QDialog):
    def __init__(self, parent:QWidget)-> None: 
        print('new window')
        QDialog.__init__(self,parent)
        self.parent = parent
        self.index: int =0
        self.recording = False
        # setting window title
        tab1 = QTabWidget()
        tab2 = QTabWidget()
        tab3 = QTabWidget()
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.West)
        self.tabs.setMovable(False)
        self.tabs.usesScrollButtons()
        
        self.tabs.addTab(tab1,"Video")
        self.tabs.addTab(tab2,"Cambiar fuente")
        #self.tabs.addTab(tab3,"Tab 3")
        self.tabs.setCurrentIndex(0)
        self.tab1UI(tab1)
        self.tab2UI(tab2)
        self.tab3UI(tab3)
		# creating a vertical layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0) 
		# adding form group box to the layout
        layout.addWidget(self.tabs)
        
		
        

        
        #layout.SetSpacing(2)
        
        self.setLayout(layout)
        self.setWindowTitle('Camera{}'.format(self.index))
    

    def tab1UI(self, tab1):
         
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.label.setScaledContents(True)
        self.label.setFont(QFont("Times",30))
        self.label.setStyleSheet(
            "color: rgb(255,0,255);"
            "background-color: rgb(0,0,0);"
            "qproperty-alignment: AlignCenter;")

        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        #layout.SetSpacing(2)
        layout.addWidget(self.label)
        self.width = layout.geometry().width()
        self.height = layout.geometry().height()

        self.parent.threads[self.index].center_x = self.width / 2
        self.parent.threads[self.index].center_y = self.height / 2
        
        tab1.setLayout(layout)
		
    def tab2UI(self, tab2):

		# creating a group box
        tab2.formGroupBox = QGroupBox("Ingrese los datos requeridos")
		# creating a line edit
        tab2.nameLineEdit = QLineEdit()
        tab2.nameLineEdit2 = QLineEdit()
		# calling the method that create the form
        self.createForm(tab2)
		# creating a dialog button for ok and cancel
        tab2.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
		# adding action when form is accepted
        tab2.buttonBox.accepted.connect(lambda:self.getInfo(tab2))
		# addding action when form is rejected
        tab2.buttonBox.rejected.connect(self.reject)

        mainLayout = QVBoxLayout()
		# adding form group box to the layout
        mainLayout.addWidget(tab2.formGroupBox)
		# adding button box to the layout
        mainLayout.addWidget(tab2.buttonBox)
		# setting lay out
        tab2.setLayout(mainLayout)
		
    def tab3UI(self, tab3):
      layout = QHBoxLayout()
      layout.addWidget(QLabel("subjects")) 
      layout.addWidget(QCheckBox("Physics"))
      layout.addWidget(QCheckBox("Maths"))
      tab3.setTabText(2,"Education Details")
      tab3.setLayout(layout)

    def sizeHint(self) -> QSize:
        print('sizehint')
        return QSize (width//3, height//3)

    def resizeEvent(self, event) ->None:
        print('resizehint')
        self.update()

    	# get info method called when form is accepted
    def getInfo(self,tab2):

		# printing the form information
        print("Person Name : {0}".format(tab2.nameLineEdit.text()))
        print("Direccion : {0}".format(tab2.nameLineEdit2.text())) 
        self.select_source(tab2.nameLineEdit.text(),tab2.nameLineEdit2.text())
        print(self.index)
        tab2.nameLineEdit.clear()
        tab2.nameLineEdit2.clear()
        #Window.select_source(1,self.nameLineEdit2.text(),self.nameLineEdit2.text())
        #"http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4"
        # index id link active
        self.parent.cameras[self.index] =[ tab2.nameLineEdit.text(), tab2.nameLineEdit2.text(), False]
		# closing the window
        self.close()
    
	# creat form method
    def createForm(self, tab2):

		# creating a form layout
        layout = QFormLayout()

		# adding rows
		# for name and adding input text
        layout.addRow(QLabel("Identificador"), tab2.nameLineEdit)
        layout.addRow(QLabel("Direccion"), tab2.nameLineEdit2)
        

		# setting layout
        tab2.formGroupBox.setLayout(layout)
    def select_source (self,cam_id, link):
        print('select_source')
        slot = Slot(self,self.index, cam_id, link)
        slot.signal.connect(self.parent.ReadImage)
        self.parent.threads[self.index]=slot
        

        print('refresh')
        print("link")
        n=1
        slot.start()
        self.parent.refresh()
    def keyPressEvent(self, event):

          
        if event.key() == Qt.Key_C:
            # Take a screenshot
            self.parent.threads[self.index].screens=True
            QToaster.showMessage(
                self, "Screenshot", corner=3, desktop=False)
        if event.key() == Qt.Key_Escape:
            # Close window
            self.close()
        elif event.key() == Qt.Key_R:
            # r : 동영상 촬영 시작 및 종료
            # Start recording
            QToaster.showMessage(
                self, "Start recording", corner=3, desktop=False)
            self.start_recording()
            
        elif event.key() == Qt.Key_T:
            # Stop recording
            QToaster.showMessage(
                self, "Stop recording", corner=3, desktop=False)
            self.stop_recording()
        elif event.key() == Qt.Key_W:
            print("Mover arriba")
            QToaster.showMessage(
                self, "Mover arriba", corner=2, desktop=False)
        elif event.key() == Qt.Key_S:
            print("Mover abajo")
            QToaster.showMessage(
                self, "Mover abajo", corner=2, desktop=False)
        elif event.key() == Qt.Key_D:
            print("Mover izquierda")
            QToaster.showMessage(
                self, "Mover izquierda", corner=2, desktop=False)
        elif event.key() == Qt.Key_A:  
            print("Mover derecha")
            QToaster.showMessage(
                self, "Mover derecha", corner=2, desktop=False)
        elif event.key() == Qt.Key_Q:
            print("Mover izquierda")
            QToaster.showMessage(
                self, "Zoom adelante", corner=2, desktop=False)
        elif event.key() == Qt.Key_E:  
            print("Mover derecha")
            QToaster.showMessage(
                self, "Zoom atras", corner=2, desktop=False)
        elif event.key() == Qt.Key_B:
            print("b")
        elif event.key()== Qt.Key_K:
            self.parent.threads[self.index].flag= False
        elif event.key()== Qt.Key_L:
            self.close_threads()
        # Zoom on video
        elif event.key()== Qt.Key_Z:
            print("Zoom")
            QToaster.showMessage(
                self, "Zoom in", corner=3, desktop=False)
            self.zoom_in()
        elif event.key()== Qt.Key_X:
            # x : zoom - out
            QToaster.showMessage(
            self, "Zoom Out", corner=3, desktop=False)
            self.zoom_out()
    

    def zoom_out(self):
        # scale 값을 조정하여 zoom-out
        if self.parent.threads[self.index].scale < 1:
            self.parent.threads[self.index].scale += 0.1
        if self.parent.threads[self.index].scale == 1:
            self.parent.threads[self.index].center_x = self.width
            self.parent.threads[self.index].center_y = self.height
            self.parent.threads[self.index].touched_zoom = False

    def zoom_in(self):
        # scale 값을 조정하여 zoom-in
        if self.parent.threads[self.index].scale > 0.2:
            self.parent.threads[self.index].scale -= 0.1



    def close_threads (self):
        for slot in self.parent.threads:
            print("closing")
            slot.flag= False
     
        
    def start_recording(self, filename=None):
        """TODO: add docstring"""

        if self.parent.threads[self.index].recording:
            print('[MyVideoCapture] already recording:', self.recording_filename)
        else:
            self.recording_filename = time.strftime("videos/%Y.%m.%d %H.%M.%S", time.localtime()) + ".avi"
           
            self.video_file = self.recording_filename
            self.video_file_name = self.recording_filename + '.avi'

            # Default resolutions of the frame are obtained (system dependent)
            self.frame_width = int( self.parent.threads[self.index].cap.get(3))
            self.frame_height = int(self.parent.threads[self.index].cap.get(4))

            # Set up codec and output video settings
            self.codec = cv2.VideoWriter_fourcc('M','J','P','G')
            self.parent.threads[self.index].output_video = cv2.VideoWriter(self.video_file_name, self.codec, 30, (self.frame_width, self.frame_height))
            self.parent.threads[self.index].recording= True
      
    def stop_recording(self):
        """TODO: add docstring"""
        print("stop recording")
        if not self.parent.threads[self.index].recording:
            print('[MyVideoCapture] not recording')
        else:
            
            self.parent.threads[self.index].output_video.release()
            self.parent.threads[self.index].recording = False
           
            print('[MyVideoCapture] stop recording:', self.recording_filename)


    def update_frame(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
                self.output_video.write(self.frame)  


    def save_frame(self):
        # Save obtained frame into video output file
        self.output_video.write(self.frame)

   
   
    
    def screenshot(self):
        print('Space key pressed')
        print(self.index)
        try:
            ret, img = self.parent.threads[self.index].cap.read()
        except:
            print("error")
        else:
        
            if ret:
                print("ret")
                now = datetime.datetime.now()
                date = now.strftime('%Y%m%d')
                hour = now.strftime('%H%M%S')
                user_id = '00001'
                filename = './images/cvui_{}_{}_{}.png'.format(date, hour, user_id)
                
                cv2.imwrite(filename, img)
            

####-----------------------------------------------
class Windo(QDialog):

	# constructor
   
    def __init__(self, parent:QWidget)-> None: 
        print('new window')
        QDialog.__init__(self,parent)
        self.parent = parent
        self.index: int =0

		# setting window title
        self.setWindowTitle("Conectar camara")

		# creating a group box
        self.formGroupBox = QGroupBox("Ingrese los datos requeridos")

		# creating a line edit
        self.nameLineEdit = QLineEdit()
        self.nameLineEdit2 = QLineEdit()
        
		# calling the method that create the form
        self.createForm()

		# creating a dialog button for ok and cancel
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

		# adding action when form is accepted
        self.buttonBox.accepted.connect(self.getInfo)

		# addding action when form is rejected
        self.buttonBox.rejected.connect(self.reject)

		# creating a vertical layout
        mainLayout = QVBoxLayout()

		# adding form group box to the layout
        mainLayout.addWidget(self.formGroupBox)

		# adding button box to the layout
        mainLayout.addWidget(self.buttonBox)

		# setting lay out
        self.setLayout(mainLayout)
    
	# get info method called when form is accepted
    def getInfo(self):

		# printing the form information
        print("Person Name : {0}".format(self.nameLineEdit.text()))
        print("Direccion : {0}".format(self.nameLineEdit2.text())) 
        Window.select_source(1,self.nameLineEdit2.text(),self.nameLineEdit2.text())
        #"http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4"
		# closing the window
        self.close()

	# creat form method
    def createForm(self):

		# creating a form layout
        layout = QFormLayout()

		# adding rows
		# for name and adding input text
        layout.addRow(QLabel("Identificador"), self.nameLineEdit)
        layout.addRow(QLabel("Direccion"), self.nameLineEdit2)
        

		# setting layout
        self.formGroupBox.setLayout(layout)


class Window(QWidget):
    def __init__(self, cams: Dict[int,str]) ->None:
        super(Window, self). __init__()
        print('Window')
        width = 1000
        
        height = 700
  
        # setting the minimum size
        self.setMinimumSize(width, height)
        # inicialize the cameras winth emptt values
        self.cameras: Dict[int, List[Any]]= OrderedDict()
        index:int
        for index in range (len(cams.keys())):
            #           index id link active
            print('index id link active')
            self.cameras[index] =[ None, None, False]
        
        index =0 
        for cam_id, link in cams.items():
            # index id link active
            self.cameras[index] =[cam_id, link, False]
            index+=1
        # setting tabs for main window
        tab_1 = QTabWidget()
        tab_2 = QTabWidget()
        tab_3 = QTabWidget()
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setMovable(False)
        self.tabs.usesScrollButtons()


        
        #main layout ----------
        layout = QGridLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(2)

        tab_1.setLayout(layout)
        self.tabs.addTab(tab_1,"Monitoreo de camaras")
        self.tabs.addTab(tab_2,"Monitoreo Robot")
        #self.tabs.addTab(tab_3,"Tab 3")
        self.tab2_UI(tab_2)
        # Make something when a tab is clicked
        self.tabs.tabBarClicked.connect(self.handle_tabbar_clicked)
        self.labels: List[QLabel] =[]
        self.threads: List[Slot] =[]
        for index, value in self.cameras.items():
            print('for window ' )
            cam_id, link, active = value
            print(cam_id)
            print(link)
            print(index)
            # thread ----------------
            
               

            slot = Slot(self, index, cam_id, link)
            slot.signal.connect(self.ReadImage)
            self.threads.append(slot)
            print('screen')
            # screen ---------------
            label= QLabel()
            label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
            label.setScaledContents(True)
            label.setFont(QFont("Times", 30))
            label.setStyleSheet(
                "color: rgb(255,0,255); background-color: rgb(0,0,0); "
                "qproperty-alignment:  AlignCenter;")
            
            clickable(label).connect(partial(self.showCam , index))
            self.labels.append(label)
            print('if add')
            if index == 0:
                layout.addWidget(label,0,0)# row1,col1
            elif index == 1:
                layout.addWidget(label, 0,1)# row1,col2
            elif index == 2:
                layout.addWidget(label,0,2)# row1,col1
            elif index == 3:
                layout.addWidget(label, 0,3)# row1,col2
            elif index == 4:
                layout.addWidget(label,1,0)# row1,col1
            elif index == 5:
                layout.addWidget(label, 1,1)# row1,col2
            elif index == 6:
                layout.addWidget(label,1,2)# row1,col1
            elif index == 7:
                layout.addWidget(label, 1,3)# row1,col2
            elif index == 8:
                layout.addWidget(label,2,0)# row1,col1
            elif index == 9:
                layout.addWidget(label, 2,1)# row1,col2
            elif index == 10:
                layout.addWidget(label,2,2)# row1,col1
            elif index == 11:
                layout.addWidget(label, 2,3)# row1,col2
            elif index == 12:
                layout.addWidget(label,3,0)# row1,col1
            elif index == 13:
                layout.addWidget(label, 3,1)# row1,col2
            elif index == 14:
                layout.addWidget(label,3,2)# row1,col1
            elif index == 15:
                layout.addWidget(label, 3,3)# row1,col2
            else:
                raise ValueError("n Camera != rows/cols")
        print('time screen')
      
        # Time screen --------------------------
        timer =  QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000) # ls
        self.showTime()
        print('timer auto threads')
        # TImer auto restart threads (restart every 3 hours)
        timer_th = QTimer(self)
        timer_th.timeout.connect(lambda:self.refresh)
        # lambda:self.select_source(1,"camarera","http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4")
        timer_th.start(60*60*3 ) # 60s*60*3 = 3hour
        # creating a vertical layout
        
        layout2 = QVBoxLayout()
        layout2.setContentsMargins(0,0,0,0) 
		# adding form group box to the layout
        layout2.addWidget(self.tabs)
		
        

        
        #layout.SetSpacing(2)
        # Change between layout and layout2 and see the magic
        self.setLayout(layout2)
        self.setWindowTitle('Monitoreo camaras')
        self.setWindowIcon(QIcon('icon.png')) 

        self.newWindow = Newform(self)
        self.newWindow3 = NewWindow(self)
        print(len(self.threads))
        self.refresh()

    
    def tab2_UI(self, tab_2):
        
        rowNo = 1
        colNo = 0
        fName = ""
        fName2 = ""
        fileNameExist = ""
        dropDownName = ""
        mainLayout = QVBoxLayout()
        model = QStandardItemModel()
        # Label camara
        self.labelcam = QLabel()
        self.labelcam.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.labelcam.setScaledContents(True)
        self.labelcam.setFont(QFont("Times",30))
        self.labelcam.setStyleSheet(
            "color: rgb(255,0,255);"
            "background-color: rgb(0,0,0);"
            "qproperty-alignment: AlignCenter;")
        # Layout Camara
        
  
        openButton = QPushButton("Cambiar fuente")
        openButton.clicked.connect(self.showForm)

        playButton = QPushButton()
        playButton.setEnabled(False)
        playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
         
        
        lbl = QLabel('00:00:00')
        lbl.setFixedWidth(60)
        lbl.setUpdatesEnabled(True)
        # self.lbl.setStyleSheet(stylesheet(self))

        elbl = QLabel('00:00:00')
        elbl.setFixedWidth(60)
        elbl.setUpdatesEnabled(True)
        # self.elbl.setStyleSheet(stylesheet(self))


        nextButton = QPushButton("Screenshot")
        #self.nextButton.clicked.connect(self.next)
        sButton = QPushButton("Screenshot")
        sButton.clicked.connect(self.screenshot)
        #self.nextButton.clicked.connect(self.next)
        delButton = QPushButton("Record")
       
        delButton.clicked.connect(self.start_recording)
        #self.delButton.clicked.connect(self.delete)

        exportButton = QPushButton("Stop record")
        exportButton.clicked.connect(self.stop_recording)
        #self.exportButton.clicked.connect(self.export)

        importButton = QPushButton("Import")
        #self.importButton.clicked.connect(self.importCSV)
        zoomButton = QPushButton("Zoom in")
        zoomButton.clicked.connect(self.zoom_in)
        #self.nextButton.clicked.connect(self.next)

        zoomOutButton = QPushButton("Zoom out")
        zoomOutButton.clicked.connect(self.zoom_out)
        #self.delButton.clicked.connect(self.delete)


        # self.ctr = QLineEdit()
        # self.ctr.setPlaceholderText("Extra")

        startTime = QLineEdit()
        startTime.setPlaceholderText("Select Start Time")

        endTime = QLineEdit()
        endTime.setPlaceholderText("Select End Time")

        iLabel = QComboBox()
        iLabel.addItem("1. Eye Contact")
        iLabel.addItem("2. Pointing")
        iLabel.addItem("3. Response to Names")
        iLabel.addItem("4. Following Pointing")
        iLabel.addItem("5. Babbling")
        iLabel.addItem("6. Question-Answering")
        iLabel.addItem("7. Showing")
        iLabel.addItem("8. Following Instructions")
        iLabel.activated[str].connect(self.style_choice)

        # self.iLabel = QLineEdit()
        # self.iLabel.setPlaceholderText("Label")

        positionSlider = QSlider(Qt.Horizontal)
        positionSlider.setRange(0, 100)
        positionSlider.sliderMoved.connect(self.setPosition)
        positionSlider.sliderMoved.connect(self.handleLabel)
        positionSlider.setSingleStep(2)
        positionSlider.setPageStep(20)
        positionSlider.setAttribute(Qt.WA_TranslucentBackground, True)

        errorLabel = QLabel()
        errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        # Main plotBox
        plotBox = QHBoxLayout()
        # Layout controles
        controlLayout = QHBoxLayout()
        # controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(openButton)
        controlLayout.addWidget(playButton)
        controlLayout.addWidget(lbl)
        controlLayout.addWidget(positionSlider)
        controlLayout.addWidget(elbl)

         
        # Left Layout{
        # layout.addWidget(self.videoWidget)

        layoutc= QVBoxLayout()
        layoutc.addWidget(self.labelcam, 3)
        # layout.addLayout(self.grid_root)
        layoutc.addLayout(controlLayout)
        layoutc.addWidget(errorLabel)

        plotBox.addLayout(layoutc, 5)
        # }
        mainLayout.addLayout(plotBox)
        # Right Layout {
        inputFields = QHBoxLayout()
        inputFields.addWidget(startTime)
        inputFields.addWidget(endTime)
        inputFields.addWidget(iLabel)
        # inputFields.addWidget(self.ctr)

        
      
        label2 = QLabel()
        label2.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        label2.setScaledContents(True)
        label2.setFont(QFont("Times",30))
        label2.setStyleSheet(
            "color: rgb(255,0,255);"
            "background-color: rgb(0,0,0);"
            "qproperty-alignment: AlignCenter;")

        feats = QGridLayout()
        feats.addWidget(nextButton,  1, 1)
        feats.addWidget(sButton,  1, 1)
        feats.addWidget(delButton, 1, 2)
        feats.addWidget(exportButton,  1, 3)
        feats.addWidget(importButton,  2,1)
        feats.addWidget(zoomButton,  2, 2)
        feats.addWidget(zoomOutButton,  2, 3)

        grid_layout = QGridLayout()
       
        button = QPushButton('Close')
        button.clicked.connect(lambda: self.showMessage(message="Close Hand"))
        grid_layout.addWidget(button, 0, 0)
        
        button = QPushButton('Open')
        button.clicked.connect(lambda: self.showMessage(message="Open Hand"))
        grid_layout.addWidget(button, 0, 2)
        button = QPushButton('Left')
        button.clicked.connect(lambda: self.showMessage(message="Move Left"))
        grid_layout.addWidget(button, 1, 0)
        ######## (x,y, alto, ancho )
        button = QPushButton('Right')
        button.clicked.connect(lambda: self.showMessage(message="Move Right"))
        grid_layout.addWidget(button, 1, 2)
        button = QPushButton('Up')
        button.clicked.connect(lambda: self.showMessage(message="Move Up"))
        grid_layout.addWidget(button, 0, 1)
        button = QPushButton('Down')
        button.clicked.connect(lambda: self.showMessage(message="Move Down"))
        grid_layout.addWidget(button, 2, 1)
        button = QPushButton('Reset')
        button.clicked.connect(lambda: self.showMessage(message="Reset"))
        grid_layout.addWidget(button, 1, 1)

        controlrob= QGroupBox("Controles robot")
        controlrob.setLayout(grid_layout)

        arm_layout = QGridLayout()
        button = QPushButton('Move Up')
        button.clicked.connect(lambda: self.showMessage(message="Move Up"))
        arm_layout.addWidget(button, 1, 0)
        
        button = QPushButton('Reset')
        button.clicked.connect(lambda: self.showMessage(message="Reset"))
        arm_layout.addWidget(button, 2, 0)
        button = QPushButton('Move Down')
        button.clicked.connect(lambda: self.showMessage(message="Move Down"))
        arm_layout.addWidget(button, 3, 0)
        ######## (x,y, alto, ancho )
        button = QPushButton('Move Up')
        button.clicked.connect(lambda: self.showMessage(message="Move Up"))
        arm_layout.addWidget(button, 1, 1)
        button = QPushButton('Reset')
        button.clicked.connect(lambda: self.showMessage(message="Reset"))
        arm_layout.addWidget(button, 2, 1)
        button = QPushButton('Move Down')
        button.clicked.connect(lambda: self.showMessage(message="Move Down"))
        arm_layout.addWidget(button, 3, 1)
        button = QPushButton('Move Up')
        button.clicked.connect(lambda: self.showMessage(message="Move Up"))
        arm_layout.addWidget(button, 1, 2)
        button = QPushButton('Reset')
        button.clicked.connect(lambda: self.showMessage(message="Reset"))
        arm_layout.addWidget(button, 2, 2)
        button = QPushButton('Move Down')
        button.clicked.connect(lambda: self.showMessage(message="Move Down"))
        arm_layout.addWidget(button, 3, 2)
        
        label_ = QLabel("     Hombro")

        arm_layout.addWidget(label_, 0,0)
        label_ = QLabel("     Codo")

        arm_layout.addWidget(label_, 0,1)
        label_ = QLabel("     Muñeca")

        arm_layout.addWidget(label_, 0,2)

        controlarm= QGroupBox("Controles brazo")
        controlarm.setLayout(arm_layout)

        controlvid= QGroupBox("Acciones sobre video")
        controlvid.setLayout(feats)
        # Layout de arriba
        layout2 = QVBoxLayout()
        layout2.addWidget(controlarm) 
        layout2.addWidget(controlrob) 
        layout2.addLayout(inputFields, 1)
        layout2.addWidget(controlvid) 
        layout2.addWidget(nextButton)
        

        plotBox.addLayout(layout2, 2)

        # self.setLayout(layout)
        mainLayout.addLayout(plotBox)

        
 
        # create the video capture thread
        self.link_2="http://192.168.104:2204/video_feed2"
        
        self.slot2 = Slot(self, index=17, cam_id=1, link=self.link_2)
        self.slot2.signal.connect(self.update_image)
        self.slot2.start()
        '''
        #self.threads.append(slot)
        self.thread_2 = VideoThread(self)
        # connect its signal to the update_image slot
        self.thread_2.change_pixmap_signal.connect(self.update_image)
        # start the thread  
        self.thread_2.start()
        '''
        
        self.newWindow4 = NewSource(self)
        

        
 
		# setting lay out
        tab_2.setLayout(mainLayout)
		# creat form method

     # creat form method
    def showMessage(self,message) :
        QToaster.showMessage(
                self, message, corner=1, desktop=False)
    
    def start_recording(self, filename=None):
        """TODO: add docstring"""

        if self.slot2.recording:
            print('Already recording:', self.recording_filename)
            QToaster.showMessage(
                self, "Already recording", corner=1, desktop=False)
        else:
            self.recording_filename = time.strftime("videos/%Y.%m.%d %H.%M.%S", time.localtime()) + ".avi"
           
            self.video_file = self.recording_filename
            self.video_file_name = self.recording_filename + '.avi'

            # Default resolutions of the frame are obtained (system dependent)
            self.frame_width = int( self.slot2.cap.get(3))
            self.frame_height = int(self.slot2.cap.get(4))

            # Set up codec and output video settings
            self.codec = cv2.VideoWriter_fourcc('M','J','P','G')
            self.slot2.output_video = cv2.VideoWriter(self.video_file_name, self.codec, 30, (self.frame_width, self.frame_height))
            self.slot2.recording= True
            QToaster.showMessage(
                self, "Recording", corner=1, desktop=False)
      
    def stop_recording(self):
        """TODO: add docstring"""
        print("stop recording")
        if not self.slot2.recording:
            print('[MyVideoCapture] not recording')
            QToaster.showMessage(
                self, "Not recording", corner=1, desktop=False)
        else:
            
            self.slot2.output_video.release()
            self.slot2.recording = False
           
            print('[MyVideoCapture] stop recording:', self.recording_filename)
            QToaster.showMessage(
                self, "Stop recording:", corner=1, desktop=False)



    def screenshot(self):
        self.slot2.screens=True
        QToaster.showMessage(
            self, "Screenshot", corner=3, desktop=False)
    
    def zoom_out(self):
        # scale 값을 조정하여 zoom-out
        if self.slot2.scale < 1:
            self.slot2.scale += 0.1
        if self.slot2.scale == 1:
            self.slot2.center_x = self.width
            self.slot2.center_y = self.height
            self.slot2.touched_zoom = False

    def zoom_in(self):
        # scale 값을 조정하여 zoom-in
        if self.slot2.scale > 0.2:
            self.slot2.scale -= 0.1

    def createForm(self):

		# creating a form layout
        layout = QFormLayout()

		# adding rows
		# for name and adding input text
        layout.addRow(QLabel("Identificador"), self.nameLineEdit_)
        layout.addRow(QLabel("Direccion"), self.nameLineEdit_2)
        

		# setting layout
        self.formGroupBox2.setLayout(layout)
   

    def showForm(self) :
        print('showcam')
         
        
        self.newWindow4.setWindowTitle('Camviar fuente del video')
        self.newWindow4.show()
    
    # def mouseMoveEvent(self, event):
        # if event.buttons() == Qt.LeftButton:
        #     self.move(event.globalPos() \- QPoint(self.frameGeometry().width() / 2, \
        #                 self.frameGeometry().height() / 2))
        #     event.accept()
 
    ##################### update Label ##################################
    def handleLabel(self):
        self.lbl.clear()
        mtime = QTime(0,0,0,0)
        self.time = mtime.addMSecs(self.mediaPlayer.position())
        self.lbl.setText(self.time.toString())
 
    def clickFile(self):
        print("File Clicked")

    def clickExit(self):
        sys.exit()

   
    def select_source (self,cam_id, link):
        print('select_source')
        slot = Slot(self,self.index, cam_id, link)
        slot.signal.connect(self.parent.ReadImage)
        self.parent.threads[self.index]=slot
        

        print('refresh')
        print("link")
        n=1
        slot.start()
        self.parent.refresh()	

    def close_threads (self, index):
        for slot in self.threads:
            print("closing")
            if slot.index != index:
                slot.flag= False

    def start_threads (self,cam_id, link):
        for index, value in self.cameras.items():
            print('for window ' )
            cam_id, link, active = value
            print(cam_id)
            print(link)
            print(index)
            # thread ----------------
            
            print('select_source')
            slot = Slot(self,self.index, cam_id, link)
            slot.signal.connect(self.parent.ReadImage)
            self.parent.threads[self.index]=slot
            slot.start()
        self.refresh()



        


    def handle_tabbar_clicked(self, index):
        print(index)

        print("x2:", index * 2)

    def select_source ( index, cam_id, link):
        print('select_source')
        slot = Slot(self, index, cam_id, link)
        slot.signal.connect(self.ReadImage)
        self.threads[index]=slot
        print('refresh')
        n=1
        slot.start()
        

    def sizeHind(self) -> QSize:
        return QSize(width, height)

    def resizeEvent(self, event) -> None:
        self.update()

    def KeyPressEvent(self,event) -> None:
        if event.Key() == Qt.Key_Escape:
            print("Escape")
            self.close()
        if event.Key() == Qt.Key_S:
            print("Snapshot")
        

    def closeEvent(self,event): pass

    def showCam(self, index: Any) -> None:
        print('showcam')
        self.newWindow.index = index
        if not self.cameras[index][2]:
            text_ = "Camara{}\nNot active".format(self.cameras[index][0])
            self.newWindow.label.setText(text_)
        self.newWindow.setWindowTitle('Camara {}'.format(self.cameras[index][0]))
        self.newWindow.show()

    def showCam2(self, index) -> None:
        print('showcam2')
        print('showcam')
        self.newWindow2.show()
    
    # get info method called when form is accepted
    def getInfo(self):

		# printing the form information
        print("Person Name : {0}".format(self.nameLineEdit.text()))
        print("Degree : {0}".format(self.degreeComboBox.currentText()))
        print("Age : {0}".format(self.ageSpinBar.text()))

		# closing the window
        self.close()


    def showTime(self) -> None:
        # Time
        print('showtime')
        time = QTime.currentTime()
        textTime= time.toString('hh:mm:ss')
        # Date
        date= QDate.currentDate()
        texDate= date.toString('ddd, MMM d')

        text ="{}\n{}".format(textTime, texDate)

        for index, value in self.cameras.items():
            cam_id, link,  active= value
            if not active:
                text_ = "Camara {}\n".format(cam_id)+ text
                self.labels[index].setText(text_)

    
    @pyqtSlot(np.ndarray, int , int , bool)
    def ReadImage(self, im: np.ndarray, index: int, cam_id: int, active: bool) -> None:

        self.cameras[index][2] = active
        cam_id, link, active= self.cameras[index]

        im = QImage (im.data, im.shape[1], im.shape[0], QImage.Format_RGB888).rgbSwapped()
        self.labels[index].setPixmap(QPixmap.fromImage(im))

        if index == self.newWindow.index:
            self.newWindow.label.setPixmap(QPixmap.fromImage(im))

    def refresh(self) -> None:
        print('refresh')
        for slot in self.threads:
            slot.start()
   
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.labelcam.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        
        return QPixmap.fromImage(convert_to_Qt_format)
    
    def style_choice(self, text):
        self.dropDownName = text
        QApplication.setStyle(QStyleFactory.create(text))
 
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)
    

# creating a class
# that inherits the QDialog class
if __name__ == '__main__':

    import sys

    cams: Dict[int, Any] = OrderedDict()
    
    print('main')
    cams[1] = None
    cams[2] = 0
    cams[3] = "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4"
    cams[4] = None
    cams[5] = None
    cams[6] = None
    cams[7] = None
    cams[8] = None
    cams[9] = None
    cams[10] = None
    cams[11] = None
    cams[12] = None
    cams[13] = None
    cams[14] = None
    cams[15] = None
    cams[16] = None
    print('cams')
    app = QApplication(sys.argv)
    print('Qapplication')
    win = Window(cams= cams)
    print('Window')
    win.show()
    sys.exit(app.exec_())
