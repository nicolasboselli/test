#-*- coding: utf-8 -*

'''
Created on 8 déc. 2013

@author: nico
'''
import pymel.core as pm
import maya.mel as mm

def addAttrSwitch():
    # attibute du switch ik
    sel = pm.ls(sl= True)
    newAttrs = ("ik" , "fk", "autoVis", 'ikVis', 'fkVis')
    
    for i in range(0,2):
        pm.addAttr( sel[0], longName = newAttrs[i], attributeType = 'double', min = 0 , max = 1, dv = 0 )
        pm.setAttr( (sel[0] + "." + newAttrs[i]) , keyable = True )
        
    for i in range(2,5):
        pm.addAttr( sel[0], longName = newAttrs[i], attributeType = 'bool' )
        pm.setAttr( (sel[0] + "." + newAttrs[i]) , keyable = True )   

def addAttrIK():
    # ik attributes
    sel = pm.ls(sl= True)
    newAttrs = ("autoStretch" , "lockElbow", "squashNStretch",)
    
    for i in range(0,3):
        pm.addAttr( sel[0], longName = newAttrs[i], attributeType = 'double', min = 0 , max = 1, dv = 0 )
        pm.setAttr( (sel[0] + "." + newAttrs[i]) , keyable = True )