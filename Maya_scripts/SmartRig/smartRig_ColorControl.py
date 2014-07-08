#-*- coding: utf-8 -*

'''
Created on 11 déc. 2013

@author: nico
'''

import pymel.core as pm
import maya.mel as mm
import maya.cmds as cmds


def colored(col):
    shapList =[]
    for o in pm.ls(sl= True):
        shapList.append(o.getShape())
        
    for i in range(0,len(shapList)):
        print shapList[i].name()
        shapList[i].overrideEnabled.set(True)
        shapList[i].overrideColor.set(col)

def renameShape():
    refName = pm.ls(sl = True)[0]
    #print (refName.name() + "Shape")
    selToName = refName.getShape()
    #print selToName.name("toto")
    pm.rename(selToName, (refName.name() + "Shape"))
    

def UI():
    colorUI = cmds.window(w = 200 , t = "color control")
    cmds.columnLayout( adjustableColumn=True )

    # create a button
    cmds.button(l = "RED", c = lambda *args: colored(13)) 
    cmds.button(l = "BLUE", c = lambda *args: colored(6)) 
    cmds.button (l = "YELLOW", c = lambda *args: colored(17))
    cmds.button(l = "Rename Shape", c = lambda *args: renameShape() )

    # show the window we last created
    cmds.showWindow(colorUI)


        
UI()