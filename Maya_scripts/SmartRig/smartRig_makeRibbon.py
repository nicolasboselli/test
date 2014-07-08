
import pymel.core as pm
import maya.mel as mm

import pymel.core.nodetypes as nt


def createPlane():
    sel = pm.ls(sl = True)[0]
    
    selChild = sel.listRelatives(c = True, typ = 'joint')[0]
    planSize = selChild.translateX.get()
    
    onePlan = pm.nurbsPlane(ch = True, o = True, po = False, ax = [0,1,0], w = planSize, lr = 0.25, u = 3)
    onePlan[0].setParent(sel)
    onePlan[0].translate.set([planSize/2,0,0])
    onePlan[0].rotate.set([0,0,0])
    pm.parent(onePlan, w = True)
    
def makeRibbon():
        
    # CREATION DU RIBBON
    # recup de la selection
    planeSelStr = pm.ls(sl= True)[0]
    
    # recup de la shape
    planeShapeStr = planeSelStr.getShape()
    
    #recup du nurbplane
    NurbPlane = planeShapeStr.listConnections( d = False )[0]
    
    folNum =  NurbPlane.patchesU.get()
    # creation des follicles
    mm.eval('createHair ' + str(folNum) + ' 1 10 0 0 0 0 5 0 1 1 1;')
    
    #recuperer les follicles
    folArray =  planeShapeStr.listConnections()
    
    for obj in folArray:
        print type(obj)
        
    # suppression des doublons    
    folArray2 = list(set(folArray))
    
    for obj in folArray2:
        print obj
        
    curveList = []
    
    # recuperation des curves
    for obj in folArray2:
        if isinstance(obj, nt.Transform ):
            curveList.append( pm.listRelatives(obj, c = True, typ = 'transform'))
            
    
     #creer les joints associer aux follicles et les parenter
    for curve in curveList:
        jointTemp = pm.joint(n = "test", rad = 3 )
        jointTemp.setParent(curve)
        jointTemp.translate.set([0,0,0])
        jointTemp.jointOrient.set([0,0,0])
    
   #supprimer les node inutiles de hair
    
    # CREATION DU RIG    
    # recuperation de la taille du ribbon
    for obj in folArray:
        if isinstance( obj , nt.MakeNurbPlane ):
            ribbonSize = obj.width.get()
    
    # positionnement du loc central
    locOne = pm.spaceLocator(n = (planeSelStr.name() + "_twist"))
    locOne.setParent(planeSelStr)
    locOne.translate.set([0,0,0])
    locOne.rotate.set([0,0,0])
    
    # positionnement du loc up
    locTwo = pm.duplicate(locOne, n = (planeSelStr.name() + "_twist") )[0]
    locTwo.translateX.set(ribbonSize/2)
    
    # positionnement du loc down
    locThree = pm.duplicate(locOne, n = (planeSelStr.name() + "_twist") )[0]
    locThree.translateX.set(ribbonSize/2*-1)
    
    locList = [ locTwo, locOne,  locThree ]
    print locList[2]
    
    allLocList = []
    
    # creation des arbres
    for obj in locList:
        Aim = pm.duplicate(obj, n = (obj.name() + "_aim") )[0]
        Up = pm.duplicate(obj, n = (obj.name() + "_up") )[0]
        
        Aim.setParent(obj)
        Up.setParent(obj)
        
        Up.translateY.set(10)
        
        pm.parent(obj, w = True )
        
        allLocList.append( obj )
        allLocList.append( Aim )
        allLocList.append( Up )
        
    # creation des joints pour le skin du ribbon
        
    jointSkinList = []
    
    for i in range(1,10,3):
        print allLocList[i]
        jointOne = pm.joint(n = (allLocList[i].name() + "_joint"), rad = 2)
        jointOne.setParent(allLocList[i])
        jointOne.translate.set([0,0,0])
        jointOne.jointOrient.set([0,0,0])
        jointSkinList.append(jointOne)
    
    jointEndList = []
    
    for i in range(0,3,2):
        print jointSkinList[i]
        jointTwo = pm.duplicate(n = jointSkinList[i].name())[0]
        jointTwo.setParent(jointSkinList[i])
        jointTwo.translate.set([0,0,0])
        jointTwo.translateX.set(1)
        jointEndList.append(jointTwo)
    
    # creation des contraintes
    pm.aimConstraint(jointSkinList[1] , allLocList[1], wut = "object", wu = [0,1,0], wuo = allLocList[2]  )
    pm.aimConstraint(jointSkinList[1] , allLocList[7], wut = "object", wu = [0,1,0], wuo = allLocList[8]  )
    pm.pointConstraint(allLocList[6],allLocList[0], allLocList[3])
    pm.pointConstraint(allLocList[8],allLocList[2], allLocList[5])
    
    pm.aimConstraint(allLocList[6] ,allLocList[4], wut = "object", wu = [0,1,0], wuo = allLocList[5]  )
    
    # ccreation du skin
    pm.skinCluster( jointSkinList[0], jointSkinList[1], jointSkinList[2], jointEndList[0], jointEndList[1], planeSelStr)


