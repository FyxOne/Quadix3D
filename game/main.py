"""
    я не знаю никаких пайтонов можно домой пожалуйста отпустите 
"""

import glfw
from engine import Math, vec2, vec3, vec4, mat4, initOpenGL, Texture, Cube3D, glClear, Shader
from world import World
from player import Player, create_cursor_callback

vertex = "#version 420 core\n"\
"layout (location = 0) in vec3 position;\n"\
"layout(location=2) in vec2 aTexCoord;\n"\
"out vec4 vertex_color;\n"\
"out vec2 TexCoord;\n"\
"uniform mat4 model;\n"\
"uniform mat4 view;\n"\
"uniform mat4 projection;\n"\
"void main()\n"\
"{"\
"    gl_Position = projection * view * model * vec4(position, 1.0f);\n"\
"    vec3 colors = vec3(1.0f, 1.0f, 1.0f);\n"\
"    TexCoord = aTexCoord;\n"\
"}"

fragment = "#version 420 core\n"\
"in vec2 TexCoord;\n;"\
"out vec4 FragColor;\n"\
"uniform sampler2D texture1;\n"\
"void main()\n"\
"{\n"\
"    FragColor = texture(texture1, TexCoord);\n"\
"}"

if __name__ == "__main__":
    if not glfw.init():
        raise Exception("GLFW initialization failed")

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)

    window = glfw.create_window(1920, 1080, "Quadix3D", glfw.get_primary_monitor(), None)
    if not window:
        glfw.terminate()
        raise Exception("GLFW window creation failed")

    glfw.make_context_current(window)

    initOpenGL()

    shader = Shader()
    shader.load(vertex, fragment)
    shader.compile()

    math = Math()

    i = 0

    world = World()
    player = Player()
    cursor_callback = create_cursor_callback(player)
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)
    glfw.set_cursor_pos_callback(window, cursor_callback)

    grass = Texture()
    grass.load("resources/grass.png")

    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear()
        shader.use()

        i += 0.01

        l = math.lookAt(0, 0, -4, 0, 0, 0, 0, 1, 0)
        p = math.perspective(90, 800/600, 0.1, 100)

        player.shader_sync(shader)
        #shader.set_matrix("view", l)
        shader.set_matrix("projection", p)

        player.update()

        grass.bind()
        world.draw(shader)

        glfw.swap_buffers(window)

    glfw.terminate()