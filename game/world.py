from engine import Shader
from voxel import Voxel

class World:
    def __init__(self):
        self.blocks = []
        
        x = -15
        z = -15
        for i in range(30):
            row = []
            for j in range(30):
                voxel = Voxel()
                voxel.setPosition(x, -2, z)

                row.append(voxel)

                x += 1
            
            self.blocks.append(row)
            x = -15
            z += 1

    def draw(self, shader):
        for i in range(0, 30):
            for j in range(0, 30):
                shader.set_matrix("model", self.blocks[i][j].getMathModel())
                self.blocks[i][j].draw()