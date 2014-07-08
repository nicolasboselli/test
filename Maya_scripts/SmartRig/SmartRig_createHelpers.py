#-*- coding: utf-8 -*

'''
Created on 13 déc. 2013

@author: nico
'''
import pymel.core as pm
import maya.mel as mm

''' @param [int,int,int] axis'''
def createCircle(axis):    
    sel = pm.ls(sl = True)[0]
    print sel
    oneCircle = pm.circle(n = (sel.name() + "_anim"), ch = True, o = True, nr = axis, r = 2)[0]
    print oneCircle
    
    oneGroup = pm.group(em = True, name = ( oneCircle.name() + "_null" ))
    print oneGroup
    
    oneCircle.setParent(oneGroup)
    pm.parent(oneGroup, sel, r = True)
    pm.parent(oneGroup, w = True)      


def createZeroParent():
    sel = pm.ls(sl = True)[0]
    oneGroup = pm.group(em = True, name = ( sel.name() + "_null" ))
    oneGroup.setParent(sel)
    oneGroup.translate.set([0,0,0])
    oneGroup.rotate.set([0,0,0])
    
    pm.parent(oneGroup, w = True)
    sel.setParent(oneGroup)

def createZero():
    sel = pm.ls(sl = True)[0]
    oneGroup = pm.group(em = True, name = ( sel.name() + "_null" ))
    oneGroup.setParent(sel)
    oneGroup.translate.set([0,0,0])
    oneGroup.rotate.set([0,0,0])
    
    pm.parent(oneGroup, w = True)
    sel.setParent(oneGroup)
    
def createLoc(rad):
    listJoints = []
    oneLoc = []
    
    sel = pm.ls(sl = True)[0]
    print (sel.name() + "loc")
    oneLoc = pm.spaceLocator(a = True, name = (sel.name() + "_loc") )
    print oneLoc
    oneLoc.localScale.set([rad,rad,rad])
    pm.parent(oneLoc, sel, r = True)
    pm.parent(oneLoc, w = True)
  
'''  
global proc createLocOne(float $radius)
{
    global string $listJoints[];
    //global string $oneGroup2 ;  
    string $oneLoc[] ;
         
    $listJoints = `ls -sl`;
   
    $oneLoc = `spaceLocator -a -n "loc#"`;
    
    setAttr ($oneLoc[0] + ".localScaleX") $radius;
    setAttr ($oneLoc[0] + ".localScaleY") $radius;
    setAttr ($oneLoc[0] + ".localScaleZ") $radius;
    
    //parent -r $oneCircle[0] $oneGroup2;
    parent -r $oneLoc[0] $listJoints[0] ;
    
    parent -w $oneLoc[0] ;  
}
'''
    
def creatDist():
    sel = pm.ls(sl = True)
    print sel
    distNodeShape = pm.distanceDimension(sp = [0,0,0], ep = [0,50,0])
    distNode = pm.listRelatives(distNodeShape, fullPath = True, parent = True)
    print distNode
    locs = pm.listConnections(distNodeShape, s = True)
    print locs       
    
    pm.rename(locs[0], (sel[0].name() + "_dist_loc1"))
    pm.rename(locs[1], (sel[1].name() + "_dist_loc2"))
    pm.rename(distNode, (sel[0].name() + "_dist"))
    
    pm.pointConstraint(sel[1], locs[1], w = True)
    pm.pointConstraint(sel[0], locs[0], w = True)
    

    

 