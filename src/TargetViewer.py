#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
@file TargetViewer.py
@detail TargetViewer is to display image sequences from a library. Upgrade from the image_viewer to include the following set
        1. 2D datasets
        2. zoom view
        3. rotation
@author hui han chin
@date 02/2015
"""

#imports

# imageview
# ====================================================================

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future_builtins import *

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QDate', 2)
sip.setapi('QTime', 2)
sip.setapi('QDateTime', 2)
sip.setapi('QUrl', 2)
sip.setapi('QTextStream', 2)
sip.setapi('QVariant', 2)
sip.setapi('QString', 2)

import imageviewer as IV
# ====================================================================

import sys
from PyQt4 import QtGui as QG
from PyQt4 import QtCore as QC
import cv2
import numpy as np

__version__= "0.2"
__company__= "DSO National Laboratories"

class TargetViewer(QG.QWidget):

    #global variables
    aspectAngle = 1
    azimuthAngle = 50
    grazingAngle = 50
    imageHeight = 400
    imageWidth = 400
    loadedData = 0

    def __init__(self):
        super(TargetViewer, self).__init__()
        self.initUI()
        self.setFixedSize(self.geometry().width(), self.geometry().height())

    def initUI(self):

        # simulation parameters
        self.TargetLabel = QG.QLabel('-',self)
        self.aspectAngleLabel = QG.QLabel('-',self)
        self.ResolutionLabel = QG.QLabel('-',self)
        
        self.grazingAngleLabel = QG.QLabel('-',self)
        self.RadarazimuthLabel = QG.QLabel('-',self)

        # 3 views image
        xmap = QG.QPixmap("../img/pov_1.png")

        viewport_name = ['Sensor View','Radar Reflectivity', 'SAR simulation']
        self.viewports = {}
        for i in xrange(3):
            view = IV.ImageViewer(xmap)
            view.enableScrollBars(False)
            view.enableHandDrag(True)
            self.viewports[viewport_name[i]] = view

        ## tool bar 
        # load file
        fileButton = QG.QPushButton('Load \n Dataset', self) 
        fileButton.clicked.connect(self.selectFile)

        # aspect slider
        AspectSlider = QG.QSlider(QC.Qt.Horizontal, self)
        AspectSlider.setMaximum(360)
        AspectSlider.setMinimum(1)
        AspectSlider.setTickPosition(QG.QSlider.TicksBelow)
        AspectSlider.valueChanged[int].connect(self.sliderChangeAspect)
        self.aspectAngleLabel =  QG.QLabel(str(self.aspectAngle),self)
        self.aspectAngleLabel.setAlignment(QC.Qt.AlignHCenter)
        self.aspectAngleLabel.setText(str(self.aspectAngle))
        
        #azimuth slide
        azimuthSlider = QG.QSlider(QC.Qt.Horizontal, self)
        azimuthSlider.setMaximum(360)
        azimuthSlider.setMinimum(1)
        azimuthSlider.setTickPosition(QG.QSlider.TicksBelow)
        azimuthSlider.valueChanged[int].connect(self.sliderChangeAspect)
        self.azimuthAngleLabel =  QG.QLabel(str(self.azimuthAngle),self)
        self.azimuthAngleLabel.setAlignment(QC.Qt.AlignHCenter)
        self.azimuthAngleLabel.setText(str(self.azimuthAngle))


        # simulation parameters
        simParamBox = QG.QGroupBox('Simulation Parameters',self) 
        paramLayout = QG.QGridLayout();
        paramLayout.addWidget(QG.QLabel('Target: ',self),0,0)
        paramLayout.addWidget(QG.QLabel('Grazing: ',self),1,0)
        paramLayout.addWidget(QG.QLabel('Resolution: ',self),2,0)
        paramLayout.addWidget( self.TargetLabel ,0,1)
        paramLayout.addWidget(self.grazingAngleLabel,1,1)
        paramLayout.addWidget( self.ResolutionLabel,2,1)
        
        simParamBox.setLayout(paramLayout)

        # drawing of the UI
        viewPortLayout = QG.QHBoxLayout()
        for i in xrange(3):
            viewPortLayout.addWidget(self.viewports[viewport_name[i]], QC.Qt.AlignHCenter)
            
        
        toolPortLayout = QG.QGridLayout()
        toolPortLayout.setColumnStretch(0,1)
        toolPortLayout.setColumnStretch(1,1)
        toolPortLayout.setColumnStretch(2,1)
        toolPortLayout.addWidget(fileButton, 1,0, QC.Qt.AlignTop)
        toolPortLayout.addWidget(simParamBox,1,2, 2,1,QC.Qt.AlignTop)
        
        aspectBox = QG.QGroupBox('Aspect Angle /Degrees',self)
        aspectBoxLayout = QG.QVBoxLayout()
        aspectBoxLayout.addWidget(AspectSlider)
        aspectBoxLayout.addWidget(self.aspectAngleLabel)
        aspectBox.setLayout(aspectBoxLayout)
        
        azimuthBox = QG.QGroupBox('Radar azimuth Angle /Degrees',self)
        azimuthBoxLayout = QG.QVBoxLayout()
        azimuthBoxLayout.addWidget(azimuthSlider)
        azimuthBoxLayout.addWidget(self.azimuthAngleLabel)
        azimuthBox.setLayout(azimuthBoxLayout)
    
        toolPortLayout.addWidget(aspectBox,1,1, QC.Qt.AlignTop)
        toolPortLayout.addWidget(azimuthBox,2,1, QC.Qt.AlignTop)
        ## overall UI
        viewerLayout = QG.QVBoxLayout()
        viewerLayout.addLayout(viewPortLayout)
        viewerLayout.addLayout(toolPortLayout)
        self.setLayout(viewerLayout)
        QG.QApplication.setStyle(QG.QStyleFactory.create('Windows'))

        self.center()
        self.setWindowTitle('Target Simulation Viewer')
        self.show()


    def selectFile(self):
        filename = QG.QFileDialog.getOpenFileName(self,'Open File','/home/hchin/Code/image_viewer/test') 


    def sliderChangeAspect(self, value):
        self.aspectAngle = value 
        self.aspectAngleLabel.setText(str(self.aspectAngle))

    def center(self):
        self.move(QG.QDesktopWidget().availableGeometry().center() - self.frameGeometry().center())

# end of TargetViewer class
def main():
    ex = TargetViewer()
    return app.exec_()
#launch main 
if __name__=='__main__':
    app = QG.QApplication(sys.argv)
    sys.exit(main())



