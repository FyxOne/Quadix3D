/*
    И в один из дней, когда мир падет... обретем свободу мы,
    потеряв наше тело. И свет далекий, укажет нам, 
    кто расскажет, кто покажет,
    и где таится тот далекий мир, 
    что давно мы потеряли.
*/

#pragma once

#include "q3d_base.h"
#include "q3d_math.h"

#define GLEW_STATIC
#include <GL/glew.h>

typedef struct q3d_shader
{
    unsigned int vertex_shader;
    unsigned int fragment_shader;
    unsigned int program;
} q3d_shader;

Q3D_EXPORT void q3d_load_shader(q3d_shader* shader, const char* v, const char* f);
Q3D_EXPORT void q3d_compile_shaders(q3d_shader* shader);
Q3D_EXPORT void q3d_use_shader(q3d_shader* shader);

Q3D_EXPORT void q3d_shader_set_mat(q3d_shader* shader, const char* uniform_id, mat4 matrix);
Q3D_EXPORT void q3d_shader_set_vec3(q3d_shader* shader, const char* uniform_id, vec3 vector);