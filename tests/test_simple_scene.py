import sys
sys.path.append('.')

from core.base import Base
from core.renderer import Renderer
from core.object3d import Scene, Mesh
from core.camera import Camera
from core.geometry import Box
from core.attribute import Attribute
from material.basicMaterial import SurfaceMaterial
from extras.helpers import AxisHelper,GridHelper
from extras.movementRig import MovementRig

class Test(Base):
    def initialize(self):
        self.renderer = Renderer()
        self.scene = Scene()

        self.moveRig = MovementRig(1, 0.1)
        self.moveRig.setPosition([0,0,4])

        self.camera = Camera()
        self.camera.setPerspective()
        self.moveRig.add(self.camera)

        geometry = Box(other_attribs={
            "vertexColor":(Attribute.Vec3Type, [[1,1,1],[1,0,0],[0,1,0],[0,0,1]]*2)
        })
        material = SurfaceMaterial({
            "useVertexColor":True,
            # "wireframe":True,
            # "lineWidth":4
        })
        self.mesh = Mesh(geometry, material)

        self.scene.add(self.mesh)
        self.scene.add(AxisHelper(lineWidth=3))
        self.scene.add(GridHelper(lineWidth=2, gridColor=[0.5,0.5,0.5]))
        self.scene.add(self.moveRig)

        self.input.regMouseEventListener(self.moveRig)

    def update(self,dt):
        self.mesh.rotateY(0.514*dt)
        self.mesh.rotateX(0.337*dt)
        self.moveRig.update(dt, self.input)
        # self.camera.rotateX(0.3*dt, False)
        
        self.renderer.render(self.scene, self.camera)

if __name__ == "__main__":
    Test().run()