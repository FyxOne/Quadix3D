#include "q3d_math.h"

mat4 mat4_identity()
{
    mat4 result;

    memset(result.m, 0, sizeof(result.m));

    for(int i = 0; i < 4; i++)
    {
        result.m[i][i] = 1.0f;
    }

    return result;
}

mat4 mat4_translate(mat4 matrix, vec3 coodrinates)
{
    mat4 result = matrix;

    result.m[0][3] += coodrinates.x;
    result.m[1][3] += coodrinates.y;
    result.m[2][3] += coodrinates.z;

    return result;
}

mat4 mat4_rotate(mat4 matrix, float angle, vec3 axis)
{
    axis = vec3_normalize(axis);
    
    float cos_angle = cosf(angle);
    float sin_angle = sinf(angle);
    float t = 1.0f - cosf(angle);

    mat4 rotation = {{
        {t * axis.x * axis.x + cos_angle, t * axis.x * axis.y - sin_angle * axis.z, t * axis.x * axis.z + sin_angle * axis.y, 0.0f},
        {t * axis.x * axis.y + sin_angle * axis.z, t * axis.y * axis.y + cos_angle, t * axis.y * axis.z - sin_angle * axis.x, 0.0f},
        {t * axis.x * axis.z - sin_angle * axis.y, t * axis.y * axis.z + sin_angle * axis.x, t * axis.z * axis.z + cos_angle, 0.0f},
        {0.0f, 0.0f, 0.0f, 1.0f}
    }};

    mat4 result;
    memset(result.m, 0, sizeof(result.m));

    for (int row = 0; row < 4; row++)
    {
        for (int col = 0; col < 4; col++)
        {
            for (int i = 0; i < 4; i++)
                result.m[row][col] += matrix.m[row][i] * rotation.m[i][col];
        }
    }

    return result;
}

mat4 mat4_perspective(float radians, float aspect, float near, float far)
{
    mat4 result = {0};

    result.m[0][0] = 1.0f / (aspect * tanf(radians / 2.0f));
    result.m[1][1] = 1.0f / tanf(radians / 2.0f);
    result.m[2][2] = (far + near) / (near - far);
    result.m[2][3] = -1.f;
    result.m[3][2] = -1.0f;

    return result;
}

mat4 mat4_lookAt(vec3 eye, vec3 center, vec3 up)
{
    vec3 f = vec3_normalize(vec3_sub(center, eye));
    vec3 s = vec3_normalize(vec3_cross(f, up));
    vec3 u = vec3_cross(s, f);

    mat4 result = mat4_identity();

    result.m[0][0] = s.x;
    result.m[0][1] = s.y;
    result.m[0][2] = s.z;
    result.m[0][3] = -vec3_dot(s, eye);

    result.m[1][0] = u.x;
    result.m[1][1] = u.y;
    result.m[1][2] = u.z;
    result.m[1][3] = -vec3_dot(u, eye);

    result.m[2][0] = -f.x;
    result.m[2][1] = -f.y;
    result.m[2][2] = -f.z;
    result.m[2][3] = vec3_dot(f, eye);

    return result;
}

vec3 vec3_normalize(vec3 vector)
{
    float length = sqrtf(vector.x * vector.x + vector.y * vector.y + vector.z * vector.z);

    if (length == 0.0f)
        return (vec3) {0, 0, 0};
    else
        return (vec3) {vector.x / length, vector.y / length, vector.z / length};
}

vec3 vec3_sub(vec3 a, vec3 b)
{
    return (vec3) {a.x - b.x, a.y - b.y, a.z - b.z};
}

vec3 vec3_cross(vec3 a, vec3 b)
{
    return (vec3) {
        a.y * b.z - a.z * b.y,
        a.z * b.x - a.x * b.z,
        a.x * b.y - a.y * b.x
    };
}

float vec3_dot(vec3 a, vec3 b)
{
    return a.x * b.x + a.y * b.y + a.z * b.z;
}

void mat4_debug(mat4 matrix)
{
    for(int i = 0; i < 4; i++)
    {
        for(int j = 0; j < 4; j++)
        {
            printf("%8.3f", matrix.m[i][j]);
        }

        printf("\n");
    }
}
