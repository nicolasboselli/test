
import pymel.core as pm
import maya.mel as mm

# recup selection (modele defaut et modele a symetriser) 
sel = pm.ls(sl= True)

''' double duplication du modele defaut '''
source =  pm.duplicate(sel[0])
target = pm.duplicate(sel[0])

'''' symetrisation de la premiere copie'''
pm.setAttr(source[0] + ".scaleX", -1 )
pm.setAttr(source[0] + ".translate", [100,0,0])

''' application du blendsahape a la premiere copie symetrisee '''
tempBS = pm.blendShape( sel[1], source[0])


pm.setAttr(target[0] + ".translate", [100,0,0])

pm.select( target[0], source[0] )
''' application du wrap a la deuxieme copie '''
test = mm.eval('doWrapArgList "2" { "1","0","1" };')


# blendshape  a fond
pm.setAttr(tempBS[0] +"." + sel[1], 1)

BSFinal = pm.duplicate( target[0], rr = True)

pm.delete(source[0], target[0])
pm.select(BSFinal[0])


# duplication du deuxieme modele qui est la forme symetrisee  '''





