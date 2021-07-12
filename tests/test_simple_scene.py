import sys
sys.path.append('.')

from core.base import Base
from core.renderer import Renderer
from core.object3d import Scene, Mesh
from core.camera import Camera
from core.geometry import Box
from core.attribute import Attribute
from material.basicMaterial import SurfaceMaterial

class Test(Base):
    def initialize(self):
        self.renderer = Renderer()
        self.scene = Scene()

        self.camera = Camera()
        self.camera.setPerspective()
        self.camera.setPosition([0,0,4])

        geometry = Box(other_attribs={
            "vertexColor":(Attribute.Vec3Type, [[1,1,1],[1,0,0],[0,1,0],[0,0,1]]*2)
        })
        material = SurfaceMaterial({"useVertexColor":True})
        self.mesh = Mesh(geometry, material)
        self.scene.add(self.mesh)

    def update(self,dt):
        self.mesh.rotateY(0.514*dt)
        self.mesh.rotateX(0.337*dt)

        self.renderer.render(self.scene, self.camera)

if __name__ == "__main__":
    Test().run()