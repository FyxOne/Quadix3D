#pragma once

#include "q3d_base.h"

#define GLEW_STATIC
#include <GL/glew.h>

#include <string.h>
#include <stdlib.h>
#include <stdio.h>

typedef struct q3d_cube
{
    float* vertices;
    int* indices;

    unsigned int VBO, VAO, EBO;
} q3d_cube;

Q3D_EXPORT void q3d_init_cube(q3d_cube* cube);
Q3D_EXPORT void q3d_draw_cube(q3d_cube* cube);