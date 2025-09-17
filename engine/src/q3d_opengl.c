#include "q3d_opengl.h"

void q3d_init_glew()
{
    if(glewInit() != GLEW_OK)
    {
        printf("Uhm...\n");
    }

    glEnable(GL_DEPTH_TEST);  
    //glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
}