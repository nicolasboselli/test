#-*- coding: utf-8 -*

import pymel.core as pm
import maya.mel as mm


import pymel.core.nodetypes as nt

'''
Created on 13 dec. 2013

@author: nico
'''

def curveInfo():
    sel = pm.ls(sl = True)[0]
    curve = pm.arclen(sel, ch = True)
    print pm.rename(curve, (sel.name() + "_info"))
    print curve

    pm.addAttr( sel, longName = "part", attributeType = 'double' )
    
    pm.setAttr( (sel + ".part") , keyable = True ) 
    str =(sel + ".part = " + curve + ".arcLength/8 ;")
    print str
    pm.expression(s = str, o = sel, ae = True, uc = "all" , n = (sel + "_part"))
