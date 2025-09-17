"""
    я нихуя не понимаю
"""

import ctypes
from ctypes import *

dll_path = "../engine/bin/q3d_engine.dll"
lib = cdll.LoadLibrary(dll_path)

### OpenGL ###

def initOpenGL():
    lib.q3d_init_glew()

def glClear():
    lib.q3d_glclear()

### Math ###

class vec2(Structure):
    _fields_ = [("x", c_float), ("y", c_float)]
    
    def __str__(self):
        return f"vec2({self.x}, {self.y})"

class vec3(Structure):
    _fields_ = [("x", c_float), ("y", c_float), ("z", c_float)]
    
    def __str__(self):
        return f"vec3({self.x}, {self.y}, {self.z})"

class vec4(Structure):
    _fields_ = [("x", c_float), ("y", c_float), ("z", c_float), ("w", c_float)]
    
    def __str__(self):
        return f"vec4({self.x}, {self.y}, {self.z}, {self.w})"

class mat4(Structure):
    _fields_ = [("m", (c_float * 4) * 4)]
    
    def __str__(self):
        result = "mat4:\n"
        for i in range(4):
            result += f"[{self.m[i][0]:.2f}, {self.m[i][1]:.2f}, {self.m[i][2]:.2f}, {self.m[i][3]:.2f}]\n"
        return result
    
lib.vec3_normalize.argtypes = [vec3]
lib.vec3_normalize.restype = vec3

lib.vec3_sub.argtypes = [vec3, vec3]
lib.vec3_sub.restype = vec3

lib.vec3_cross.argtypes = [vec3, vec3]
lib.vec3_cross.restype = vec3

lib.vec3_dot.argtypes = [vec3, vec3]
lib.vec3_dot.restype = float

lib.mat4_identity.argtypes = []
lib.mat4_identity.restype = mat4

lib.mat4_translate.argtypes = [mat4, vec3]
lib.mat4_translate.restype = mat4

lib.mat4_rotate.argtypes = [mat4, c_float, vec3]
lib.mat4_rotate.restype = mat4

lib.mat4_perspective.argtypes = [c_float, c_float, c_float, c_float]
lib.mat4_perspective.restype = mat4

lib.mat4_lookAt.argtypes = [vec3, vec3, vec3]
lib.mat4_lookAt.restype = mat4

lib.vec3_normalize.argtypes = [vec3]
lib.vec3_normalize.restype = vec3

lib.vec3_sub.argtypes = [vec3, vec3]
lib.vec3_sub.restype = vec3

lib.vec3_cross.argtypes = [vec3, vec3]
lib.vec3_cross.restype = vec3

lib.vec3_dot.argtypes = [vec3, vec3]
lib.vec3_dot.restype = c_float

lib.mat4_debug.argtypes = [mat4]
lib.mat4_debug.restype = None

class Math:
    def __init__(self):
        pass

    def identity(self):
        return lib.mat4_identity()
    
    def translate(self, matrix, x, y, z):
        return lib.mat4_translate(matrix, vec3(x, y, z))
    
    def rotate(self, matrix, angle, x, y, z):
        return lib.mat4_rotate(matrix, angle, vec3(x, y, z))
    
    def perspective(self, fov, aspect, near, far):
        return lib.mat4_perspective(fov, aspect, near, far)
    
    def lookAt(self, eye_x, eye_y, eye_z, center_x, center_y, center_z, up_x, up_y, up_z):
        return lib.mat4_lookAt(
            vec3(eye_x, eye_y, eye_z),
            vec3(center_x, center_y, center_z),
            vec3(up_x, up_y, up_z)
        )
    
    def debug_matrix(self, matrix):
        return lib.mat4_debug(matrix)

    def normalize(self, vector):
        return lib.vec3_normalize(vector)

    def sub(self, a, b):
        return lib.vec3_sub(a, b)

    def cross(self, a, b):
        return lib.vec3_cross(a, b)

    def dot(self, a, b):
        return lib.vec3_dot(a, b)
    
### Shaders ###

class q3d_shader(Structure):
    _fields_ = [
        ("vertex_shader", c_uint),
        ("fragment_shader", c_uint),
        ("program", c_uint)
    ]

lib.q3d_load_shader.argtypes = [POINTER(q3d_shader), c_char_p, c_char_p]
lib.q3d_load_shader.restype = None

lib.q3d_compile_shaders.argtypes = [POINTER(q3d_shader)]
lib.q3d_compile_shaders.restype = None

lib.q3d_use_shader.argtypes = [POINTER(q3d_shader)]
lib.q3d_use_shader.restype = None

lib.q3d_shader_set_mat.argtypes = [POINTER(q3d_shader), c_char_p, mat4]
lib.q3d_shader_set_mat.restype = None

lib.q3d_shader_set_vec3.argtypes = [POINTER(q3d_shader), c_char_p, vec3]
lib.q3d_shader_set_vec3.restype = None

class Shader:
    def __init__(self):
        self.object = q3d_shader()
    
    def load(self, v, f):
        v = c_char_p(v.encode('utf-8'))
        f = c_char_p(f.encode('utf-8'))
        lib.q3d_load_shader(byref(self.object), v, f)
    
    def compile(self):
        lib.q3d_compile_shaders(byref(self.object))
    
    def use(self):
        lib.q3d_use_shader(byref(self.object))
    
    def set_matrix(self, uniform_name, matrix):
        name = c_char_p(uniform_name.encode('utf-8'))
        lib.q3d_shader_set_mat(byref(self.object), name, matrix)
    
    def set_vec3(self, uniform_name, x, y, z):
        name = c_char_p(uniform_name.encode('utf-8'))
        vector = vec3(x, y, z)
        lib.q3d_shader_set_vec3(byref(self.object), name, vector)
    
    def set_vec3_from_vec(self, uniform_name, vector):
        name = c_char_p(uniform_name.encode('utf-8'))
        lib.q3d_shader_set_vec3(byref(self.object), name, vector)

### Cube 3D ###

class q3d_cube(Structure):
    _fields_ = [
        ("vertices", POINTER(c_float)),
        ("indices", POINTER(c_int)),
        ("VBO", c_uint),
        ("VAO", c_uint),
        ("EBO", c_uint)
    ]

lib.q3d_init_cube.argtypes = [POINTER(q3d_cube)]
lib.q3d_init_cube.restype = None

lib.q3d_draw_cube.argtypes = [POINTER(q3d_cube)]
lib.q3d_draw_cube.restype = None

class Cube3D:
    def __init__(self):
        self.object = q3d_cube()
    
    def init(self):
        lib.q3d_init_cube(byref(self.object))

    def draw(self):
        lib.q3d_draw_cube(byref(self.object))

### Texturing ###

class q3d_texture(Structure):
    _fields_ = [
        ("texture_id", c_uint)
    ]

lib.q3d_load_texture.argtypes = [POINTER(q3d_texture), c_char_p]
lib.q3d_load_texture.restype = None

lib.q3d_bind_texture.argtypes = [POINTER(q3d_texture)]
lib.q3d_bind_texture.restype = None

class Texture:
    def __init__(self):
        self.t = q3d_texture()

    def load(self, path):
        lib.q3d_load_texture(byref(self.t), c_char_p(path.encode('utf-8')))
    
    def bind(self):
        lib.q3d_bind_texture(byref(self.t))