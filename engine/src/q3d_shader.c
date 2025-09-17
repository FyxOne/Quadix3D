#include "q3d_shader.h"

void q3d_load_shader(q3d_shader *shader, const char *v, const char *f)
{
    shader->vertex_shader = glCreateShader(GL_VERTEX_SHADER);
    shader->fragment_shader = glCreateShader(GL_FRAGMENT_SHADER);

    glShaderSource(shader->vertex_shader, 1, &v, (void*)0);
    glShaderSource(shader->fragment_shader, 1, &f, (void*)0);
}

void q3d_compile_shaders(q3d_shader* shader)
{
    GLint success;
    GLchar infoLog[512];

    glCompileShader(shader->vertex_shader);
    glGetShaderiv(shader->vertex_shader, GL_COMPILE_STATUS, &success);
    if (!success)
    {
        glGetShaderInfoLog(shader->vertex_shader, 512, (void*)0, infoLog);
        printf("Shader_v: %s\n", infoLog);

        return;
    }

    glCompileShader(shader->fragment_shader);
    glGetShaderiv(shader->fragment_shader, GL_COMPILE_STATUS, &success);
    if (!success)
    {
        glGetShaderInfoLog(shader->fragment_shader, 512, (void*)0, infoLog);
        printf("Shader_f: %s\n", infoLog);

        return;
    }

    shader->program = glCreateProgram();
    glAttachShader(shader->program, shader->vertex_shader);
    glAttachShader(shader->program, shader->fragment_shader);
    glLinkProgram(shader->program);

    glGetProgramiv(shader->program, GL_LINK_STATUS, &success);
    if (!success) {
        glGetProgramInfoLog(shader->program, 512, (void*)0, infoLog);
        printf("Shader_p: %s\n", infoLog);
        
        return;
    }

    glDeleteShader(shader->vertex_shader);
    glDeleteShader(shader->fragment_shader);
}

void q3d_use_shader(q3d_shader* shader)
{
    glUseProgram(shader->program);
}

void q3d_shader_set_mat(q3d_shader* shader, const char *uniform_id, mat4 matrix)
{
    GLuint mat_loc = glGetUniformLocation(shader->program, uniform_id);
    if (mat_loc == -1) 
    {
        return;
    }
    
    glUniformMatrix4fv(mat_loc, 1, GL_TRUE, (const GLfloat*)&matrix);
}

void q3d_shader_set_vec3(q3d_shader* shader, const char *uniform_id, vec3 vector)
{
    GLuint vec_loc = glGetUniformLocation(shader->program, uniform_id);
    if (vec_loc == -1) 
    {
        return;
    }

    glUniform3f(vec_loc, vector.x, vector.y, vector.z);   
}
