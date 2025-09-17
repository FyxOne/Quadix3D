#pragma once

#include "q3d_base.h"

#include <stdio.h>
#include <string.h>
#include <math.h>

typedef struct 
{
    float x, y;
} vec2;

typedef struct
{
    float x, y, z;
} vec3;

typedef struct 
{
    float x, y, z, w;
} vec4;

typedef struct
{
    float m[4][4];
} mat4;

Q3D_EXPORT mat4 mat4_identity();
Q3D_EXPORT mat4 mat4_translate(mat4 matrix, vec3 coodrinates);
Q3D_EXPORT mat4 mat4_rotate(mat4 matrix, float angle, vec3 axis);
Q3D_EXPORT mat4 mat4_perspective(float radians, float aspect, float near, float far);
Q3D_EXPORT mat4 mat4_lookAt(vec3 eye, vec3 center, vec3 up);

Q3D_EXPORT vec3 vec3_normalize(vec3 vector);
Q3D_EXPORT vec3 vec3_sub(vec3 a, vec3 b);
Q3D_EXPORT vec3 vec3_cross(vec3 a, vec3 b);
Q3D_EXPORT float vec3_dot(vec3 a, vec3 b);

Q3D_EXPORT void mat4_debug(mat4 matrix);