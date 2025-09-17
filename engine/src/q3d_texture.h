#pragma once
#include "q3d_base.h"

#include <GL/glew.h>

#define STB_IMAGE_IMPLEMENTATION
#define STB_IMAGE_STATIC
#include <stb_image.h>

typedef struct q3d_texture
{
    unsigned int texture_id;
} q3d_texture;

Q3D_EXPORT void q3d_load_texture(q3d_texture* texture, const char* path);
Q3D_EXPORT void q3d_bind_texture(q3d_texture* texture);