#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

'''
Created on 22 May 2014

@author: nboselli
'''

# Import PySide classes

import sip
import maya.OpenMayaUI as omui
import pymel.core as pm
import maya.mel as mm

import SmartRig_createHelpers
reload(SmartRig_createHelpers)

from PyQt4 import QtCore
from PyQt4 import QtGui

#from shiboken import wrapInstance

def maya_main_window():
    ptr = omui.MQtUtil.mainWindow()
    if ptr is not None:
        return sip.wrapinstance(long(ptr), QtCore.QObject)
        

class PrimitiveUi(QtGui.QDialog):
    
    def __init__(self, parent = maya_main_window()):
        super(PrimitiveUi, self).__init__(parent)
        
        self.setWindowTitle("Rig Companion")
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        self.create_layout()
        self.create_connections()

    def create_layout(self):
        self.btnXcirc = QtGui.QPushButton("create X circle (anim)!")
        self.btnYcirc = QtGui.QPushButton("create Y circle (anim)!")
        self.btnZcirc = QtGui.QPushButton("create Z circle (anim)!")
        
        self.btnLoc10 = QtGui.QPushButton("create locator 1!")
        self.btnLoc05 = QtGui.QPushButton("create locator 0.5!")
        self.btnLoc02 = QtGui.QPushButton("create locator 0.2!")
        
        self.btnZero = QtGui.QPushButton("create zero!")
        
        self.tiret1 = QtGui.QLabel("-------")
        self.tiret2 = QtGui.QLabel("-------")
                
        main_layout = QtGui.QVBoxLayout()
        
        main_layout.setContentsMargins(2,2,2,2)
        main_layout.setSpacing(2)    
        
        main_layout.addWidget(self.btnXcirc)
        main_layout.addWidget(self.btnYcirc)
        main_layout.addWidget(self.btnZcirc)
        
        main_layout.addWidget(self.tiret1)
           
        main_layout.addWidget(self.btnLoc10)
        main_layout.addWidget(self.btnLoc05)
        main_layout.addWidget(self.btnLoc02)
        
        main_layout.addWidget(self.tiret2)
        
        main_layout.addWidget(self.btnZero)
        
        main_layout.addStretch()
        self.setLayout(main_layout)
        
    def create_connections(self):
        self.btnXcirc.clicked.connect(lambda:SmartRig_createHelpers.createCircle([1,0,0]))
        self.btnYcirc.clicked.connect(lambda:SmartRig_createHelpers.createCircle([0,1,0]))
    

        

'''
try:
    ui.close()
except:
    pass   
'''
        
ui = PrimitiveUi()

ui.show()
#ui.close()
