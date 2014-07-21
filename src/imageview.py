#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@file
@detail
@author hui han chin
@date 04/2014
"""

import sys
from PyQt4 import QtGui, QtCore
import cv2
import numpy as np

class Viewer(QtGui.QWidget):
    
    aspectAng = 0
    imageH = 400
    imageW = 400
    datasetFilename = ''

    

    def __init__(self):
        super(Viewer, self).__init__()
        self.initUI()

    def initUI(self):

        ## the 3 views image display
        xmap = QtGui.QPixmap("../img/pov_1.png")
        self.pov = QtGui.QLabel(self)
        self.pov.setFixedSize(self.imageW, self.imageH)
        self.pov.setPixmap(xmap)
        self.proj = QtGui.QLabel(self)
        self.proj.setFixedSize(self.imageW, self.imageH)
        self.proj.setPixmap(xmap)
        self.sim = QtGui.QLabel(self)
        self.sim.setFixedSize(self.imageW, self.imageH)
        self.sim.setPixmap(xmap)

        ## tool bar 
        # load file
        fileButton = QtGui.QPushButton('Load \n Dataset', self) 
        fileButton.clicked.connect(self.selectFile)

        # aspect slider
        angSlider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        angSlider.setMaximum(360)
        angSlider.setTickPosition(QtGui.QSlider.TicksBelow)
        angSlider.valueChanged[int].connect(self.sliderChangeAng)
        self.angLabel =  QtGui.QLabel(self)
        self.angLabel.setAlignment(QtCore.Qt.AlignHCenter)
        self.angLabel.setText(str(self.aspectAng))

        # simulation parameters
        simParamBox = QtGui.QGroupBox('Simulation Parameters',self) 
        paramLayout = QtGui.QGridLayout();
        paramLayout.addWidget(QtGui.QLabel('Target',self),0,0)
        paramLayout.addWidget(QtGui.QLabel('Grazing',self),1,0)
        paramLayout.addWidget(QtGui.QLabel('Resolution',self),2,0)
        simParamBox.setLayout(paramLayout)

        # drawing of the UI

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)
        grid.addWidget(self.pov,1,0, QtCore.Qt.AlignHCenter)
        grid.addWidget(self.proj,1,1, QtCore.Qt.AlignHCenter)
        grid.addWidget(self.sim,1,2, QtCore.Qt.AlignHCenter)
        
        grid.addWidget(fileButton,2,0, QtCore.Qt.AlignTop)
        angBox = QtGui.QGroupBox('Aspect Angle /Degrees',self)
        angBoxLayout = QtGui.QVBoxLayout()
        angBoxLayout.addWidget(angSlider)
        angBoxLayout.addWidget(self.angLabel)
        angBox.setLayout(angBoxLayout)
        grid.addWidget(angBox,2,1)
        grid.addWidget(simParamBox,2,2)
        
        self.setLayout(grid)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Windows'))

        self.center()
        self.setWindowTitle('Target Simulation Viewer')
        self.show()


    def selectFile(self):
        filename = QtGui.QFileDialog.getOpenFileName(self,'Open File','/home/hchin/Code/image_viewer/test') 
        self.povPixarray = self.readMovie(str(filename), 300)
        self.updateView()

    def updateView(self):
        self.pov.setPixmap(self.povPixarray[self.aspectAng])
        self.pov.show()
        
#eoCap = cv2.VideoCapture()
#eoCap.open(str(filename))
#print eoCap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT)
#eoCap.release()

    def readMovie(self, filename, count):
        vidCap = cv2.VideoCapture(filename)
        print vidCap.get(8)
        if vidCap.get(7)<count: #cv2.CV_CAP_PROP_FRAME_COUNT
            vidCap.release()
            return
        vidWidth = vidCap.get(3) #cv2.CV_CAP_PROP_FRAME_WIDTH
        vidHeight = vidCap.get(4) #cv2.CV_CAP_PROP_FRAME_HEIGHT
        pixArray = []
        for x in xrange(count):
            (ret, frame) = vidCap.read()
            image = QtGui.QImage(frame, vidWidth, vidHeight, QtGui.QImage.Format_RGB888)
            image = image.scaled(self.imageW, self.imageH)
            pixFrame = QtGui.QPixmap(self.imageW,self.imageH)
            pixFrame.convertFromImage(image)
            pixArray.append(pixFrame)

#        vidCap.release()

        print len(pixArray)
        cv2.destroyAllWindows()
        return pixArray
        


    def center(self):           
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def sliderChangeAng(self, value):
        self.aspectAng = value 
        self.angLabel.setText(str(self.aspectAng))
        self.updateView()


def main():    
    app = QtGui.QApplication(sys.argv)
    ex = Viewer()
    sys.exit(app.exec_())

#launch main
if __name__ == '__main__':
    main()
