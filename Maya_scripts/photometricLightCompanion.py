#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import pymel.core as pm
import maya.mel as mm

import pymel.core.nodetypes as nt

#recupère la liste de photonmap sur les light
def listPhotoMap():
    shapeList = []
    litSel = pm.ls(sl = True)
    for o in litSel:
        shapeList.append(o.getShape())
    
    print shapeList
    
    photoLitTemp = []
    for s in shapeList:
        for c in pm.listConnections(s):
            if isinstance(c, nt.Mia_photometric_light):
                photoLitTemp.append(c)

    return photoLitTemp

#add mia photon map
def addPhotonMap():
    lightSel = pm.ls(sl = True)[0]
    lightMapVar = pm.createNode("mia_photometric_light", n = "mia_photometric_light")
    
    lightMapVar.manual_peak_intensity_cd.set(500)
    lightMapVar.units_to_meter_scale.set(100)
    lightMapVar.distribution_mode.set(1)
    
    pm.connectAttr( lightMapVar.message, lightSel.getShape().miLightShader, f = True)
    pm.connectAttr( lightMapVar.message, lightSel.getShape().miPhotonEmitter, f = True)

#activation de l area light
def areaLight():
    lightSel = pm.ls(sl = True)[0]
    lightSelShape = lightSel.getShape()
    lightSelShape.areaLight.set(1)
    lightSel.scale.set([5,5,1])
    

#change l'état de la map   
def onOffPhotoLit(mapList, state):
    for l in mapList: 
        l.on.set(state)

#UI      
def UI():
    photoUI = pm.window(t = "Photometric Light Companion", w = 200)
    pm.columnLayout( adj = True )
    pm.button(l = "add mia photon map", c = lambda *args: addPhotonMap() )
    pm.button(l = "on mia photon map", c = lambda *args: onOffPhotoLit(mapList = listPhotoMap(), state = True) )
    pm.button(l = "off mia photon map", c = lambda *args: onOffPhotoLit(mapList = listPhotoMap(), state = False))
    pm.button(l = "active area light", c = lambda *args: areaLight())
   
    pm.showWindow(photoUI)
    
#UI()