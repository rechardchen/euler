from .matrix import *

class Object3D(object):
    def __init__(self):
        self.transform  = makeIdentity()
        self.parent     = None
        self.children   = []
    
    def add(self,child):
        self.children.append(child)
        child.parent = self
    
    def remove(self, child):
        self.children.remove(child)
        child.parent = None
    
    def getWorldMatrix(self):
        if self.parent is not None:
            return self.parent.getWorldMatrix() @ self.transform
        else:
            return self.transform
    
    def descendantIter(self):
        nodesToProcess=[self]
        while len(nodesToProcess) > 0:
            node = nodesToProcess.pop(0)
            yield node
            nodesToProcess = node.children + nodesToProcess
    
    def applyMatrix(self, matrix, localCoord = True):
        self.transform = self.transform @ matrix if localCoord else matrix @ self.transform
    
    def translate(self, x,y,z,localCoord=True):
        m = makeTranslation(x,y,z)
        self.applyMatrix(m,localCoord)
    
    def rotateX(self,angle,localCoord=True):
        m = makeRotationX(angle)
        self.applyMatrix(m,localCoord)
    
    def rotateY(self,angle,localCoord=True):
        m = makeRotationY(angle)
        self.applyMatrix(m,localCoord)
    
    def rotateZ(self,angle,localCoord=True):
        m = makeRotationZ(angle)
        self.applyMatrix(m,localCoord)
    
    def scale(self, s, localCoord=True):
        m = makeScale(s)
        self.applyMatrix(m,localCoord)
    
    def getPosition(self):
        return [self.transform.item((0,3)), 
                self.transform.item((1,3)), 
                self.transform.item((2,3))]
    
    def getWorldPosition(self):
        worldTransform = self.getWorldTransform()
        return [worldTransform.item((0,3)), 
                worldTransform.item((1,3)),
                worldTransform.item((2,3))]
    
    def setPosition(self, position):
        self.transform.itemset((0,3), position[0])
        self.transform.itemset((1,3), position[1])
        self.transform.itemset((2,3), position[2])

# Scene and Group class do not provide special implementations 
# Just make understanding code more easily
class Scene(Object3D):
    def __init__(self):
        super().__init__()

class Group(Object3D):
    def __init__(self):
        super().__init__()

class Mesh(Object3D):
    def __init__(self, geometry, material):
        super().__init__()

        self.geometry = geometry
        self.material = material

        self.visible = True
        geometry.associateVariables(material.programRef)


