#-*- coding: utf-8 -*

'''
Created on 12 dec. 2013

@author: nico
'''
import pymel.core as pm
import maya.mel as mm
import maya.cmds as cmds

import SmartRig.smartRig_AddAttr as smartRig_AddAttr
reload(smartRig_AddAttr)

import SmartRig.SmartRig_createHelpers as SmartRig_createHelpers
reload(SmartRig_createHelpers)

import SmartRig.smartRig_makeRibbon as smartRig_makeRibbon
reload(smartRig_makeRibbon)

# import smartAnim
# reload (smartAnim)

import SmartRig.smartRig_ikCurve as smartRig_ikCurve
reload(smartRig_ikCurve)

def UI():
    defUI = pm.window(t = "rig companion", w = 200)
    pm.columnLayout(adjustableColumn=True)
    
    pm.button(l = "create X circle (anim)!", c = lambda *args: SmartRig_createHelpers.createCircle([1,0,0]))
    pm.button(l = "create Y circle (anim)!", c = lambda *args: SmartRig_createHelpers.createCircle([0,1,0]))
    pm.button(l = "create Z circle (anim)!", c = lambda *args: SmartRig_createHelpers.createCircle([0,0,1]))
    pm.text(l = "-------------")
    pm.button(l = "create locator 1!", c = lambda *args: SmartRig_createHelpers.createLoc(1) )
    pm.button(l = "create locator 0.5 !", c = lambda *args: SmartRig_createHelpers.createLoc(0.5) )
    pm.button(l = "create locator 0.2 !", c = lambda *args: SmartRig_createHelpers.createLoc(0.2) )
    pm.text(l = "-------------")
    pm.button(l = "create zero !", c = lambda *args: SmartRig_createHelpers.createZero())
    pm.text(l = "-------------")
    pm.button(l = "create dimension !", c = lambda *args: SmartRig_createHelpers.creatDist() )
    pm.text(l = "-------------")
    pm.button(l = "add IK attributes", c = lambda *args: smartRig_AddAttr.addAttrIK())
    pm.button(l = "add switch attributes", c = lambda *args: smartRig_AddAttr.addAttrSwitch() )
    pm.text(l = "-------------")
    pm.button(l = "create plane", c = lambda *args: smartRig_makeRibbon.createPlane())
    pm.button(l = "make ribbon", c = lambda *args: smartRig_makeRibbon.makeRibbon())
    pm.text(l = "-------------")
    # pm.button(l = "reset position", c = lambda *args: smartAnim.resetPosRot() )
    pm.text(l = "-------------")
    pm.button(l = "add curve info", c = lambda *args: smartRig_ikCurve.curveInfo() )
        
    pm.showWindow(defUI)
    
UI()