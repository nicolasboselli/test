import os
import sys

import pymel.core as pm
import maya.mel as mel
import maya.OpenMaya as om

from PySide import QtGui,QtCore
from PySide.QtGui import *
from PySide.QtCore import *

sys.path.append(os.path.dirname(__file__))
from Ui_forestGenerator import Ui_forestGenerator


class forestGenerator(QWidget):
    """
    TODO : Rendre la possibilite de pourvoir modifier les parameter par defaut de l'emitter,particleShape,collider
    
    """
    
    def __init__(self, parent=None):
        
        self.version = "0.15"
        
        # BUILD UI
        
        super(forestGenerator, self).__init__(parent)
        self.ui = Ui_forestGenerator()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        # PRINTS
        
        self.printInf = om.MGlobal_displayInfo
        self.printWan = om.MGlobal_displayWarning
        self.printErr = om.MGlobal_displayError
        
        # SET VAR
        
        self.surface= []
        self.listInstanceOrig = []
        self.listInstance=[]
        self.listInstanceInfo={}
        self.IsFirstStart = True
        self.worldParent = "forestGenerator_grp"
        self.worldParentBake = "forestGeneratorBake_grp"
        self.DynState = 1
        
        # SET CONNECTIONS
        
        self.setupConnection()
        
        
        # SET UI VISIBILITY / DISABLE
        
        if self.IsFirstStart:
            self.showGlobalParameter()
            self.ui.bake_qw.setHidden(True)
        self.ui.simulationContinue_bt.setEnabled(False)
        self.ui.updateRadius_gb.setHidden(True)
        #self.ui.simulationStart_bt.setEnabled(False)
        
        
        # PARAMETERS OF DYNAMIC
    
        self.particleParameter={
                                'lifespanMode':3
                        }
        
        self.emitterParameter={
                               'needParentUV':1,
                               'scaleRateByObjectSize':0
                               }
        
        self.nucleusParameter={
                               'startFrame':100,
                               'gravityDirectionY':-10
                               }
        self.rigidParameter={
                               'thickness':0,
                               'stickiness':200,
                               'friction':0.1
                               }

        # INIT INSTANCE TABLE
        self.columnsName = {'instance':{
                                       'name':'Instance',
                                       'id':0
                                       },
                             'type':{
                                         'name':'Type',
                                         'id':1,
                                          'menu':['Large','Medium','Small']
                                         },
                             'percent':{
                                     'name':'%',
                                     'id':2,
                                     'default':100
                                     },
                             'radius':{
                                           'name':'Radius',
                                           'id':3,
                                           'default':1,
                                           },
                             'rx':{
                                     'name':'Rx',
                                     'id':4,
                                     'default':4
                                     },
                             'ry':{
                                           'name':'Ry',
                                           'id':5,
                                           'default':360
                                           },
                             'rz':{
                                          'name':'Rz',
                                          'id':6,
                                          'default':4
                                          },
                             'scMin':{
                                          'name':'Sc Min',
                                          'id':7,
                                          'default':0.5
                                          },
                             'scMax':{
                                             'name':'Sc Max',
                                             'id':8,
                                             'default':1.5
                                             }
                            }
        
        self.ui.instance_tw.setColumnCount(len(self.columnsName))
        for i,row in enumerate(self.columnsName):
            item = QTableWidgetItem()
            self.ui.instance_tw.setHorizontalHeaderItem(int(self.columnsName[row]['id']), item)
            item.setText(self.columnsName[row]['name'])
            item.setSizeHint(QtCore.QSize(20, 20))
        
        
        # SHOW UI
        self.GUI={}
        self.GUI['wins'] = self
        self.GUI['wins'].show()
        
        self.printInf("--- Forest Generator v{0} ---".format(self.version))
        
    def setupConnection(self):
        # Link action clicked button 
        self.ui.surfaceSelect_bt.clicked.connect(self.selectSurface)
        self.ui.instanceAdd_bt.clicked.connect(self.addSelectInstance)
        self.ui.instanceRemoveSel_bt.clicked.connect(self.removeSelectInstance)
        self.ui.instanceClear_bt.clicked.connect(self.clearInstance)
        self.ui.global_gb.clicked.connect(self.showGlobalParameter)
        self.ui.simulationStart_bt.clicked.connect(self.startSimulation)
        self.ui.stop_bt.clicked.connect(self.stopSimulation)
        self.ui.simulationContinue_bt.clicked.connect(self.continueSimlation)
        self.ui.instance_tw.cellChanged.connect(self.tablechanged)
        self.ui.bake_bn.clicked.connect(self.bake)
        self.ui.simulationDisplayInstance_cb.toggled.connect(self.updateDisplay)
        self.ui.simulationDisplayRadius_cb.toggled.connect(self.updateDisplay)
        self.ui.updateRadius_bt.clicked.connect(self.updateRadius)
        
    def selectSurface(self):
        listFace = pm.filterExpand(pm.ls(sl=1),sm=34)
        if listFace == None:listFace=[]
        listMesh = pm.ls(sl=1,type="transform")
        
        if len(listFace) > 0 and len(listMesh) > 0 :
            self.printErr("Select face or mesh")
            return
        
        
        #MESH IS SELECT 
        if len(listMesh) >= 1:
            if len(listMesh) > 1:
                self.printErr("Select only one mesh")
                return
            if len(listMesh[0].listRelatives(c=1,ni=1,s=1)) == 0:
                self.printErr("Select invalid mesh / only one shape")
                return
            
            self.surface = pm.filterExpand(str(listMesh[0])+".f[*]",sm=34)
            self.ui.surfaceInfo_le.setText("Mesh select -> {0}".format(listMesh[0]))
            self.IsFirstStart = True
            return
        
        #FACE IS SELECT 
        if len(listFace) > 1:
            listFaceMesh=[]
            for x in listFace:
                if not str(x).split(".")[0] in listFaceMesh:
                    listFaceMesh.append(str(x).split(".")[0])
                    
            if len(listFaceMesh) > 1:
                self.printErr("Select only one mesh")
                return
            
            self.surface = listFace
            self.ui.surfaceInfo_le.setText("Face Select {0} in mesh {1}".format(len(listFace),listFaceMesh[0]))
            self.IsFirstStart = True
            return
    
    def addSelectInstance(self):
        if not pm.ls(sl=1):
            return
        listMesh = pm.ls(sl=1,type="transform")
        if len(listMesh[0].listRelatives(c=1,ni=1,s=1)) > 1:
            self.printErr("Select mesh with only one shape")
            return
        if len(listMesh[0].listRelatives(c=1,ni=1,s=1)) == 0:
            self.printErr("Select mesh")
            return
        for mesh in listMesh:
            
            self.addInstance(mesh)
    
    def removeSelectInstance(self):
        if not self.ui.instance_tw.selectedItems():
            self.printWan("No instance select")
            return
        for instance in self.ui.instance_tw.selectedItems():
            item = self.ui.instance_tw.item(0,instance.row())
            self.listInstanceOrig = [ x for x in self.listInstanceOrig if not item.text() in x.name()]
            self.ui.instance_tw.removeRow(instance.row())
        
    def clearInstance(self):
        row = self.ui.instance_tw.rowCount()
        i=0
        while i <= row:
            self.ui.instance_tw.removeRow(0)
            i+=1
        self.listInstance = []
        
    def addInstance(self,mesh):
        """
            Add mesh in instance table.
        """
        row = self.ui.instance_tw.rowCount()
        
        # Test if instance is already added
        if row >> 0:
            i=0
            while i < row:
                if str(mesh) == self.ui.instance_tw.item(i,0).text():
                    self.printWan("Instance already added -> {0}".format(mesh))
                    return
                i+=1
        
        self.ui.instance_tw.setRowCount(self.ui.instance_tw.rowCount() + 1)
        
        
        for column in self.columnsName:
            key=self.columnsName[column]['id']
            item = QTableWidgetItem()
            self.ui.instance_tw.setItem(row, key, item)
            
            if key == 0:
                item.setText(str(mesh))
            else:
                if self.getColumnById(key)['default']:
                    item.setText(str(self.getColumnById(key)['default']))
                
            if self.getColumnById(key)['menu']:
                item.setText(self.getColumnById(key)['menu'][0])
                item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsEnabled)
        self.listInstanceOrig.append(mesh)
    def contextMenuEvent(self, event):
        """
            Displays the menu if needed on selected cell
        """
        if self.ui.instance_tw.selectedItems():
            cells = self.ui.instance_tw.selectedItems()
            for i in range(len(cells)):
                if i == len(cells)-1:break
                if not cells[i].column() == cells[i+1].column():
                    return
            list = self.getColumnById(cells[0].column())['menu']
            if list:
                self.contextMenu = QMenu(self)
                for i in range(len(list)):
                    Action =self.contextMenu.addAction(list[i])
                self.contextMenu.triggered.connect(self.setNewTextCell)
                self.contextMenu.popup(QCursor.pos())

    def setNewTextCell(self,action):
        cells = self.ui.instance_tw.selectedItems()
        for cell in cells:
            cell.setText(action.text())

    def getColumnById(self,id):
        column = {}
        for key in self.columnsName:
            if id == self.columnsName[key]['id']:
                column['key']=key
                column['name']=self.columnsName[key]['name']
                column['id']=self.columnsName[key]['id']
                
                if 'default' in self.columnsName[key]:
                    column['default']=self.columnsName[key]['default']
                else:
                    column['default']=False
                    
                if 'menu' in self.columnsName[key]:
                    column['menu']=self.columnsName[key]['menu']
                else:
                    column['menu']=False
                    
                
        return column

    def getRowByName(self,name):
        listRow = {}
        for i in range(0,self.ui.instance_tw.rowCount(),1):
            if self.ui.instance_tw.item(i,0).text() == name:
                for key in self.columnsName:
                    listRow[key] = self.ui.instance_tw.item(i,self.columnsName[key]['id']).text()
                return listRow

    def tablechanged(self,row,column):
        self.setNewTextCell(self.ui.instance_tw.item(row,column))
        if not self.IsFirstStart :
            
            isPlay = pm.play( q=True, state=True )
            if isPlay : pm.play(state=False)
            self.updateDynState(1)
            if isPlay : pm.runtime.InteractivePlayback()


    def showGlobalParameter(self):
        if self.ui.global_gb.isChecked():self.ui.global_qw.setHidden(False)
        else:self.ui.global_qw.setHidden(True)
    
    def startSimulation(self):

        if len(self.surface) == 0:
            self.printErr('No surface select!')
            return 

        if len(self.listInstanceOrig) == 0:
            self.printErr("No instance select!")
            return
        

        pm.currentTime(100)
        if self.IsFirstStart :
            self.IsFirstStart = False
            #Delete the root group if exists
            
            if pm.objExists(self.worldParent):
                pm.delete(self.worldParent)
            if pm.objExists("forestGenerator_exp"):
                pm.delete("forestGenerator_exp")
            
            #Create root group
            self.worldParent = pm.group(em=1,w=1,name=self.worldParent)
            
            
            #Duplicate instance
            pm.select(cl=1)
            self.listInstance = []
            for inst in self.listInstanceOrig:
                tmp = pm.duplicate(inst,name=inst.name()+"_inst")[0]
                self.connectOriginaleMesh(inst, tmp)
                pm.select(tmp,add=True)
                
                #Instance radius computation
                
                bbx = pm.polyEvaluate(tmp,b=True)
                ltmp = [abs(bbx[0][1]-bbx[0][0]),abs(bbx[2][1]-bbx[2][0])]
                self.listInstanceInfo[str(tmp)]={
                                            "meshOriginal":inst,
                                            "radius":min(ltmp)/2
                                            }
            self.listInstance = pm.ls(sl=1)
            
            grpInstance = pm.group(n="instance_grp")
            pm.parent(grpInstance,self.worldParent)
            pm.select(cl=1)
    
            self.meshCollider = self.createCollider(self.surface)
            if self.ui.surfaceSmooth_cb.isChecked():
                pm.polySmooth(self.meshCollider,dv=self.meshCollider.getAttr("displaySmoothMesh"),method=0 )
            
            pm.parent(self.meshCollider,self.worldParent)
            self.meshCollider.setAttr("v",0)
            
            self.meshEmitter = self.createEmitter(self.meshCollider)
            pm.parent(self.meshEmitter,self.worldParent)
            self.meshEmitter.setAttr("v",0)
            
            self.createParticleEmitter(self.meshEmitter,collider=self.meshCollider)
        
        # Init expresionn at Creation
        self.updateDynExpressionCreation(self.partShape)
        
        
        #Play Interractive playback
        pm.playbackOptions(aet=20000,max=20000)
        self.simulate()
        
    
    def stopSimulation(self):
        mel.eval("playButtonForward;")
        self.updateDynState(2)
        for x in range(0,3,1):
            pm.currentTime(pm.currentTime()+1)
        self.ui.simulationContinue_bt.setEnabled(True)
        self.ui.updateRadius_gb.setHidden(False)
        self.ui.bake_qw.setHidden(False)

    def continueSimlation(self):
        self.simulate()

    def simulate(self):
        self.ui.updateRadius_gb.setHidden(True)
        if not self.ui.simulationlarge_cb.isChecked() and not self.ui.simulationMedium_cb.isChecked() and not self.ui.simulationSmall_cb.isChecked():
            self.printErr("Please at least select a checkBox!")
            return
        self.updateDisplay()
        self.ui.bake_qw.setHidden(True)
        self.updateDynState(1)
        pm.runtime.InteractivePlayback()
        
    def connectOriginaleMesh(self,original,mesh):
        
        pm.addAttr(mesh,longName='originalMesh', attributeType='message')
        pm.connectAttr(str(original)+".message",str(mesh)+".originalMesh",f=1)
        mesh.setAttr('originalMesh',l=1)

    def updateDynState(self,state):
        self.DynState = state
        if state != 1:
            pm.setAttr(self.nameEmitter+".rate",0)
        else : 
            pm.setAttr(self.nameEmitter+".rate",float(self.ui.simulationEmit_le.text()))
        self.updateDynExpressionCreation(self.partShape)

    def updateDisplay(self):
        if pm.objExists(self.particle) :
            pm.setAttr(self.particle+".v",self.ui.simulationDisplayRadius_cb.isChecked())
        if pm.objExists(self.instancer) :
            pm.setAttr(self.instancer+".v",self.ui.simulationDisplayInstance_cb.isChecked())
    
    def updateRadius(self):
        
        if self.ui.updateRadiusBy_le.text() == "":return
        
        reduce = float(self.ui.updateRadiusBy_le.text())
        
        for x in self.partShape.getAttr("id"):
            t = pm.nParticle(self.partShape,q=1,at="typePP",id=x)[0]
            r = pm.nParticle(self.partShape,q=1,at="radiusPP",id=x)[0]
            pos = pm.nParticle(self.partShape,q=1,at="position",id=x)
            pm.nParticle(self.partShape,e=1,at="fixPosPP",vv=(pos[0],pos[1],pos[2]),id=x)
            p = pm.nParticle(self.partShape,q=1,at="fixPosPP",id=x)
            
            if t == self.ui.updateRadiusType_cb.currentIndex():
                if self.ui.updateRadiusOp_cb.currentText() == "Divide":
                    nR = r/reduce
                elif self.ui.updateRadiusOp_cb.currentText() == "Multiply":
                    nR = r*reduce
                pm.nParticle(self.partShape,e=1,at="fixPosPP",vv=(p[0],p[1]-(r-nR),p[2]),id=x)
                pm.nParticle(self.partShape,e=1,at="radiusPP",fv=nR,id=x)
                
                
                print p,pm.nParticle(self.partShape,q=1,at="fixPosPP",id=x)

    def createCollider(self,faces,name="collider_msh"):
        # Create Collider 
        
        #Duplicate mesh
        meshCollider = pm.duplicate(faces[0].split('.')[0],name="collider_msh")[0]
        
        #Get same face in the duplicate mesh
        faces = pm.filterExpand([str(meshCollider)+"."+y.split(".")[1] for y in faces],sm=34)
        
        #Get all face in mesh
        faceMesh = pm.filterExpand(str(meshCollider)+".f[*]",sm=34)
        
        #Reverse the face select
        faceReverse = list(set(faceMesh)-set(faces))
        
        #Delete for the reverse face for keep face select
        pm.delete(faceReverse)
        
        return meshCollider
        
    def createEmitter(self,mesh,name="particleEmitter_msh"):
        #Create boundingBox of the mesh
        bbx = pm.polyEvaluate(mesh,b=True)
        cube = pm.polyCube(w=abs(bbx[0][1]-bbx[0][0]),h=abs(bbx[1][1]-bbx[1][0]),d=abs(bbx[2][1]-bbx[2][0]),sx=1,sy=1,sz=1,ax=(0,1,0),cuv=4,ch=0,name=name)
        cube = cube[0]
        cube.setAttr("t",( (bbx[0][1]+bbx[0][0])/2,(bbx[1][1]+bbx[1][0])/2,(bbx[2][1]+bbx[2][0])/2))
        
        #Keep only face 1 for emit
        pm.delete([cube+".f[2:6]",cube+".f[0]"])
        
        #Connection of mesh and the emitter 
        self.connectOriginaleMesh(mesh, cube)
        
        #Move emitter in y  in a percentage of area of face.
        face = pm.PyNode(cube+".f[1]")
        area = face.getArea(space="world")
        pm.select(cube)
        y = pow(area,0.1)*100
        pm.move(0,y,0,r=1,os=1,wd=1)
        return cube
    
    def createParticleEmitter(self,meshEmitter,collider):
        
        # Force nParticle balls at creation
        pm.optionVar(sv=("NParticleStyle","Balls"))
        
        self.particle,self.partShape = pm.nParticle(n=str(meshEmitter)+"_particle")
        #Add attribute in particleShape
        pm.addAttr(self.partShape,ln="indexPP",dt="doubleArray")
        pm.addAttr(self.partShape,ln="rotatePP",dt="vectorArray")
        pm.addAttr(self.partShape,ln="scalePP",dt="vectorArray")
        pm.addAttr(self.partShape,ln="rgbPP",dt="vectorArray")
        pm.addAttr(self.partShape,ln="fixPosPP",dt="vectorArray")
        pm.addAttr(self.partShape,ln="opacityPP",dt="doubleArray")
        
        pm.addAttr(self.partShape,ln="typePP",dt="doubleArray")
        
        self.nameEmitter = str(meshEmitter)+"_emitter"
        pm.emitter(meshEmitter,type="surface",name=self.nameEmitter,r=float(self.ui.simulationEmit_le.text()))
        pm.connectDynamic(self.partShape,em=self.nameEmitter)
        
        #Used maya command because pymel crash when find nucleus node
        self.nucleusName = mel.eval("listConnections -type \"nucleus\" "+self.partShape+";")[0]
        
        pm.parent(self.partShape,self.worldParent)
        pm.parent(self.nameEmitter,self.worldParent)
        pm.parent(self.nucleusName,self.worldParent)
        
        self.setParamaters(self.partShape,self.particleParameter)
        self.setParamaters(self.nameEmitter,self.emitterParameter)
        self.setParamaters(self.nucleusName,self.nucleusParameter)
        pm.addAttr(self.partShape,ln="radiusPP",dt="doubleArray")

        
        #Create Rigid
        pm.select(collider,r=1)
        pm.runtime.nClothMakeCollide(collider)
        self.nrigid = pm.listConnections(collider.listRelatives(s=1,c=1)[0],type='nRigid')[0]
        self.setParamaters(self.nrigid.listRelatives(s=1,c=1)[0],self.rigidParameter)
        pm.parent(self.nrigid,self.worldParent)
        self.nrigid.setAttr("v",0)
        
        #Create instancer
        self.instancer = pm.particleInstancer(self.partShape,a=True,object=self.listInstance,n=str(meshEmitter)+"_instancer",cycle="sequential",age="indexPP",rotation="rotatePP",scale="scalePP",visibility="opacityPP")
        pm.parent(self.instancer,self.worldParent)
        
        #Create proc Colision 
        expression = """
global proc forestGeneratorEvent(string $particleObject,int $particleId, string  $geometryObject) 
{

    vector $rgb = `nParticle -attribute rgbPP -id $particleId -q $particleObject`;

    if ($rgb != << 1,1,1 >>)
    {
        nParticle -e -attribute rgbPP -id $particleId -vv 0 1 0 $particleObject;
    }
    
    vector $pos = `nParticle -attribute position -id $particleId -q $particleObject`;
    
    vector $lastPos = `nParticle -attribute lastPosition -id $particleId -q $particleObject`;
    
    
    
    nParticle -e -attribute opacityPP -id $particleId -fv 1 $particleObject;

    if (mag($pos - $lastPos) >= 10 && $rgb != << 1,1,1 >>){
    
        nParticle -e -attribute lifespanPP -id $particleId -fv 0 $particleObject;
    }
}"""
        pm.expression(s=expression,n="forestGenerator_exp")
        #Create  Colision event
        
        pm.event(self.partShape,die=0,count=0,proc="forestGeneratorEvent")

    def setParamaters(self,nodeName,parameters):
        print "set parameter",nodeName
        if len(parameters) == 0:return 
        for att in parameters:
            pm.setAttr(nodeName+"."+att,parameters[att])
            
            
    def updateDynExpressionCreation(self,particleShape):
        pm.setAttr(self.partShape+".radiusPP",l=0)
        
        if self.DynState == 1:
            expression ="""

if (rgbPP == << 1,1,1 >>)
{
    position = fixPosPP;
}

"""
            expression += "if(age>={0} && rgbPP != <<0,1,0>> && rgbPP != <<1,1,1>>)\n".format(self.ui.simulationAge_le.text())
            expression += """
{
    lifespanPP=0;
}
if (rgbPP != <<1,1,1>> && rgbPP == <<0,1,0>> && mag(position - lastPosition) >= 2)
{
    lifespanPP=0;
}
"""
        elif self.DynState == 2:
            expression = """
if ((opacityPP == 0 || mag(position - lastPosition) >= 2) && rgbPP != <<1,1,1>>)
{
    lifespanPP=0;
    
}
else
{
    rgbPP = <<1,1,1>>;
    fixPosPP = position;

}
"""
        else:
            expression = """
vector $pos = position;
position = << $pos.x, $pos.y - (radiusPP/2) ,$pos.z >>;
"""
        pm.dynExpression(self.partShape,s=expression,runtimeAfterDynamics=True)
        l = []
        for i,x in enumerate(self.listInstance):
            inst = self.getRowByName(x.getAttr("originalMesh").name())
            typ = inst['type']
            
            if "Large" == typ and self.ui.simulationlarge_cb.isChecked():
                l.append(i)
                continue
            if "Medium" == typ and self.ui.simulationMedium_cb.isChecked():
                l.append(i)
                continue
            if "Small" == typ and self.ui.simulationSmall_cb.isChecked():
                l.append(i)
                continue


        expression = "// AUTO BUILD\n"
        expression += "int $percent = rand(0,100);\n"
        expression += "int $listIndex[];\n"
        
        for i,itm in enumerate(l):
            perc = self.ui.instance_tw.item(itm,self.columnsName['percent']['id']).text()
            expression += "if($percent <= {0})//{1}\n".format(perc,str(self.listInstance[itm]))
            expression += "{\n"
            expression += "\t\t$listIndex[{0}] = {1};\n".format(i,itm)
            expression += "}\n"
        
        expression += "int $j = rand(0,size($listIndex));\n"
        expression += "int $i = $listIndex[$j];\n"
        
        
        
        expression += "if(size($listIndex) == 0)\n"
        expression += "{\n"
        expression += "\t\tlifespanPP=0;\n".format(i,itm)
        expression += "}\n"
        
        expression += "float $gScale ={0};\n".format(float(self.ui.globalScale_le.text()))
        
        expression += "indexPP = $i;\n\n"
        expression += "//Compute Radius , Scale & Rotation\n\n"
        for i,itm in enumerate(self.listInstance):
            expression += "if($i == {0})//{1}\n".format(i,str(itm))
            expression += "{\n"
            expression += "\t//Scale\n"
            expression += "\tscalePP = rand({0},{1})*$gScale;\n".format(float(self.ui.instance_tw.item(i,self.columnsName['scMin']['id']).text()),float(self.ui.instance_tw.item(i,self.columnsName['scMax']['id']).text()))
            expression += "\t//Radius\n"
            expression += "\tradiusPP = {0}*{1}*scalePP;\n".format( float(self.listInstanceInfo[str(itm)]['radius']),float(self.ui.instance_tw.item(i,self.columnsName['radius']['id']).text()))
            expression += "\t//rotate\n"
            rx = float(self.ui.instance_tw.item(i,self.columnsName['rx']['id']).text())/2
            ry = float(self.ui.instance_tw.item(i,self.columnsName['ry']['id']).text())/2
            rz = float(self.ui.instance_tw.item(i,self.columnsName['rz']['id']).text())/2
            expression += "\trotatePP = << rand(-{0},{0}) , rand(-{1},{1}), rand(-{2},{2})>>;\n".format(rx,ry,rz)
            
            expression += "\t//type\n"
            typ = self.ui.instance_tw.item(i,self.columnsName['type']['id']).text()
            
            if "Large" == typ   :   t = 2
            if "Medium" == typ  :   t = 1
            if "Small" == typ   :   t = 0
            expression += "\ttypePP = {0};\n".format(t)
        
            expression += "}\n"
        expression += "opacityPP = 0;\n"
        expression += "rgbPP = <<0,0,0>>;\n"

        pm.dynExpression(self.partShape,s=expression,creation=True)
        pm.setAttr(self.partShape+".radiusPP",l=1)
    
    def bake(self):
        self.updateDynState(3)
        self.instancer = pm.PyNode(self.instancer)
        
        if not pm.objExists(self.worldParentBake):
            self.worldParentBake = pm.group(n=self.worldParentBake,em=1,w=1)
            
        
        if pm.ls("FGpass_*"):
            pad = str(int(sorted(pm.ls("FGpass_*"),reverse=True)[0].split('_')[1])+1).zfill(4)
            
        else:
            pad = "1".zfill(4)
        
        prefix = "FGp_"+pad
        
        self.worldPassBake = pm.parent(pm.group(em=1,w=1,name="FGpass_"+pad),self.worldParentBake)
        
        arbo = {}
        for i,x in enumerate(self.instancer.allInstances()[1]):
            id = self.instancer.allInstances()[2][i]
            inst = self.instancer.allInstances()[0][self.instancer.allInstances()[3][i]]
            instT = inst.listRelatives(p=1)[0]
            mesh = instT.getAttr("originalMesh")
            
            instParamater = self.getRowByName(mesh)
            typeInst = instParamater["type"].lower()
            if not typeInst in arbo:
                arbo[typeInst] = {}
            
            if not mesh.name() in arbo[typeInst] :
                arbo[typeInst][mesh.name()] = []
                
            meshTmp = pm.instance(mesh,n=prefix+"_"+str(mesh)+"_"+str(id)+"_inst")[0]
            meshTmp.setTransformation(x)
            arbo[typeInst][mesh.name()].append(meshTmp)
            self.connectOriginaleMesh(mesh, meshTmp)
            #loc = pm.spaceLocator(n=str(mesh)+"_"+str(id)+"_loc")
            #arbo[typeInst][mesh.name()].append(loc)
            #loc.setTransformation(x)
            #self.connectOriginaleMesh(mesh, loc.listRelatives(s=1,c=1)[0])
        
        for x in arbo:
            typeGrp = pm.group(n=prefix+"_"+x,em=1,w=1)
            typeGrp = pm.parent(typeGrp,self.worldPassBake)
            for y in arbo[x]:
                pm.select(cl=1)
                pm.select(arbo[x][y])
                grptmp = pm.group(w=1,n=prefix+"_"+y+"_locGrp")
                pm.parent(grptmp,typeGrp)
