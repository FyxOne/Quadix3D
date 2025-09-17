from engine import Math, vec2, vec3, vec4, mat4, Shader
import keyboard
import math

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        
        self.camera_front = vec3(0, 0, -1)
        self.camera_up = vec3(0, 1, 0)
        self.camera_right = vec3(1, 0, 0)
        
        self.pitch = 0
        self.yaw = -90
        self.lastX = 1920 / 2.0
        self.lastY = 1080 / 2.0
        self.firstMouse = True
        
        self.math = Math()

    def process_mouse_movement(self, xpos, ypos):
        if self.firstMouse:
            self.lastX = xpos
            self.lastY = ypos
            self.firstMouse = False

        xoffset = xpos - self.lastX
        yoffset = self.lastY - ypos  # Обратно, так как координаты Y идут снизу вверх
        self.lastX = xpos
        self.lastY = ypos

        sensitivity = 0.1
        xoffset *= sensitivity
        yoffset *= sensitivity

        self.yaw += xoffset
        self.pitch += yoffset

        # Ограничение угла наклона
        if self.pitch > 89.0:
            self.pitch = 89.0
        if self.pitch < -89.0:
            self.pitch = -89.0

        # Обновление векторов направления камеры
        front = vec3()
        front.x = math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        front.y = math.sin(math.radians(self.pitch))
        front.z = math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch))
        
        self.camera_front = self.math.normalize(front)
        
        # Также пересчитываем правый вектор и вектор вверх
        world_up = vec3(0, 1, 0)
        self.camera_right = self.math.normalize(self.math.cross(self.camera_front, world_up))
        self.camera_up = self.math.normalize(self.math.cross(self.camera_right, self.camera_front))

    def set_position(self, x, y, z):
        self.x = x
        self.y = y 
        self.z = z

    def shader_sync(self, shader):
        self.view_matrix = self.math.lookAt(
            self.x, self.y, self.z,
            self.x + self.camera_front.x, 
            self.y + self.camera_front.y, 
            self.z + self.camera_front.z,
            self.camera_up.x, self.camera_up.y, self.camera_up.z
        )

        shader.set_matrix("view", self.view_matrix)

    def get_position(self):
        return [self.x, self.y, self.z]
    
    def get_view_matrix(self):
        return self.view_matrix

class Player(Camera):
    def __init__(self):
        super().__init__()
        self.move_speed = 0.05

    def _control(self):
        if keyboard.is_pressed("w"):
            self.set_position(
                self.x + self.move_speed * self.camera_front.x,
                self.y + self.move_speed * self.camera_front.y, 
                self.z + self.move_speed * self.camera_front.z
            )

        if keyboard.is_pressed("s"):
            self.set_position(
                self.x - self.move_speed * self.camera_front.x,
                self.y - self.move_speed * self.camera_front.y, 
                self.z - self.move_speed * self.camera_front.z
            )

        if keyboard.is_pressed("d"):
            self.set_position(
                self.x + self.move_speed * self.camera_right.x,
                self.y + self.move_speed * self.camera_right.y,
                self.z + self.move_speed * self.camera_right.z
            )

        if keyboard.is_pressed("a"):
            self.set_position(
                self.x - self.move_speed * self.camera_right.x,
                self.y - self.move_speed * self.camera_right.y,
                self.z - self.move_speed * self.camera_right.z
            )

    def update(self):
        self._control()

# Функция обратного вызова для мыши
def create_cursor_callback(player):
    def cursor_position_callback(window, xpos, ypos):
        player.process_mouse_movement(xpos, ypos)
    return cursor_position_callback