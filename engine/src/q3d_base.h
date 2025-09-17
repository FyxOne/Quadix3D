#pragma once

#ifdef _WIN32
    #define Q3D_EXPORT __declspec(dllexport)
#else
    #define Q3D_EXPORT __attribute__((visibility("default")))
#endif

#define GLEW_STATIC
#include <GL/glew.h>

Q3D_EXPORT void q3d_glclear();