from engine import Math, vec3, vec4, mat4, Cube3D

class Voxel:
    def __init__(self):
        self.voxel = Cube3D()
        self.voxel.init()

        self.math = Math()
        self.model = self.math.identity()

    def draw(self):
        self.voxel.draw()

    def setPosition(self, x, y, z):
        self.model = self.math.translate(self.model, x, y, z)

    def getMathModel(self):
        return self.model