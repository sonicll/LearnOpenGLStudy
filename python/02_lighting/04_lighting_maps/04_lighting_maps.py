import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import numpy as np
import argparse
from PIL import Image

import glfw
from OpenGL.GL import *
import glm
from shader import Shader
from camera import Camera
from utils import *

### Primitives
def set_triangle():
    vertices = [  # positions        # texture coords
                 -0.5, -0.5,  0.0,   0.0, 0.0,
                  0.5, -0.5,  0.0,   1.0, 0.0,
                  0.0,  0.5,  0.0,   0.5, 1.0
               ]
    vertices = np.array(vertices, dtype=np.float32)

    return vertices, None

def set_rectangle():
    vertices = [  # positions        # texture coords
                  0.5,  0.5,  0.0,   1.0, 1.0,   # top right
                  0.5, -0.5,  0.0,   1.0, 0.0,   # bottom right
                 -0.5, -0.5,  0.0,   0.0, 0.0,   # bottom left
                 -0.5,  0.5,  0.0,   0.0, 1.0    # top left
               ]
    vertices = np.array(vertices, dtype=np.float32)

    indices = [ 0, 1, 3,
                1, 2, 3 ]
    indices = np.array(indices, dtype=np.uint32)

    return vertices, indices

def set_box():
    vertices = [
                -0.5, -0.5, -0.5,   0.0, 0.0, -1.0,   0.0, 0.0,
                 0.5, -0.5, -0.5,   0.0, 0.0, -1.0,   1.0, 0.0, 
                 0.5,  0.5, -0.5,   0.0, 0.0, -1.0,   1.0, 1.0, 
                 0.5,  0.5, -0.5,   0.0, 0.0, -1.0,   1.0, 1.0, 
                -0.5,  0.5, -0.5,   0.0, 0.0, -1.0,   0.0, 1.0, 
                -0.5, -0.5, -0.5,   0.0, 0.0, -1.0,   0.0, 0.0, 

                -0.5, -0.5,  0.5,   0.0, 0.0, 1.0,    0.0, 0.0,
                 0.5, -0.5,  0.5,   0.0, 0.0, 1.0,    1.0, 0.0,
                 0.5,  0.5,  0.5,   0.0, 0.0, 1.0,    1.0, 1.0,
                 0.5,  0.5,  0.5,   0.0, 0.0, 1.0,    1.0, 1.0,
                -0.5,  0.5,  0.5,   0.0, 0.0, 1.0,    0.0, 1.0,
                -0.5, -0.5,  0.5,   0.0, 0.0, 1.0,    0.0, 0.0,

                -0.5,  0.5,  0.5,  -1.0, 0.0, 0.0,    1.0, 0.0,
                -0.5,  0.5, -0.5,  -1.0, 0.0, 0.0,    1.0, 1.0,
                -0.5, -0.5, -0.5,  -1.0, 0.0, 0.0,    0.0, 1.0,
                -0.5, -0.5, -0.5,  -1.0, 0.0, 0.0,    0.0, 1.0,
                -0.5, -0.5,  0.5,  -1.0, 0.0, 0.0,    0.0, 0.0,
                -0.5,  0.5,  0.5,  -1.0, 0.0, 0.0,    1.0, 0.0,

                 0.5,  0.5,  0.5,   1.0, 0.0, 0.0,    1.0, 0.0,
                 0.5,  0.5, -0.5,   1.0, 0.0, 0.0,    1.0, 1.0,
                 0.5, -0.5, -0.5,   1.0, 0.0, 0.0,    0.0, 1.0,
                 0.5, -0.5, -0.5,   1.0, 0.0, 0.0,    0.0, 1.0,
                 0.5, -0.5,  0.5,   1.0, 0.0, 0.0,    0.0, 0.0,
                 0.5,  0.5,  0.5,   1.0, 0.0, 0.0,    1.0, 0.0,

                -0.5, -0.5, -0.5,   0.0, -1.0, 0.0,   0.0, 1.0,
                 0.5, -0.5, -0.5,   0.0, -1.0, 0.0,   1.0, 1.0,
                 0.5, -0.5,  0.5,   0.0, -1.0, 0.0,   1.0, 0.0,
                 0.5, -0.5,  0.5,   0.0, -1.0, 0.0,   1.0, 0.0,
                -0.5, -0.5,  0.5,   0.0, -1.0, 0.0,   0.0, 0.0,
                -0.5, -0.5, -0.5,   0.0, -1.0, 0.0,   0.0, 1.0,

                -0.5,  0.5, -0.5,   0.0, 1.0, 0.0,    0.0, 1.0,
                 0.5,  0.5, -0.5,   0.0, 1.0, 0.0,    1.0, 1.0,
                 0.5,  0.5,  0.5,   0.0, 1.0, 0.0,    1.0, 0.0,
                 0.5,  0.5,  0.5,   0.0, 1.0, 0.0,    1.0, 0.0,
                -0.5,  0.5,  0.5,   0.0, 1.0, 0.0,    0.0, 0.0,
                -0.5,  0.5, -0.5,   0.0, 1.0, 0.0,    0.0, 1.0,
                ]

    vertices = np.array(vertices, dtype=np.float32)

    return vertices, None


### Textures
def load_texture(file_path):
    texture = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, texture)   # all upcoming GL_TEXTURE_2D operations now have effect on this texture object
    
    # set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)    # set texture wrapping to GL_REPEAT (default wrapping method)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    # set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    img = Image.open(file_path)
    img_w, img_h, img_data = img.size[0], img.size[1], img.tobytes("raw", "RGBA", 0, -1)
    if(img_data):
        # Note that 7th parameter(color type) is same as the img's color type
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img_w, img_h, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)
    else:
        print("Failed to load texture")
    
    return texture



### lighting
light_position = glm.vec3(1.2, 1.0, 2.0)


### main
def main(args):
    # glfw: initialize and configure
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    if (sys.platform == "darwin"):  # for Mac OS. forward compatibility
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

    ### camera
    camera = Camera(args.window_width, args.window_height, glm.vec3(0.0, 0.0, 3.0))
 
    # glfw window creation
    window = glfw.create_window(args.window_width, args.window_height, "LearnOpenGL", None, None)
    if window is None:
        print("Failed to create GLFW window")
        glfw.terminate()
        return   

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
    glfw.set_cursor_pos_callback(window, camera.mouse_callback)
    glfw.set_scroll_callback(window, camera.zoom)

    # tell glfw to capture mouse
    glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_NORMAL)

    # configure global opengl state
    glEnable(GL_DEPTH_TEST)

    # set shader program
    obj_shader   = Shader('04_lighting_maps/04_object.vs',   '04_lighting_maps/04_object.fs')
    light_shader = Shader('04_lighting_maps/04_lighting.vs', '04_lighting_maps/04_lighting.fs')


    # select primitive type
    if args.primitive == "tri":
        vertices, indices = set_triangle()
    elif args.primitive == "rect":
        vertices, indices = set_rectangle()
    elif args.primitive == "box":
        vertices, indices = set_box()
    else :
        print("Please write target primitive ('triangle', 'rect')")
        exit()
    

    # configure the VBO(EBO)
    VBO = glGenBuffers(1)
    EBO = glGenBuffers(1) if indices is not None else None

    # copy vertices array in a buffer for OpenGL to use
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices, GL_STATIC_DRAW)
    if EBO is not None:
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices, GL_STATIC_DRAW)

    # configure the object's VAO
    obj_VAO = glGenVertexArrays(1)
    glBindVertexArray(obj_VAO)
    # position attribute
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)
    # normal attribute
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), ctypes.c_void_p(3 * sizeof(GLfloat)))
    glEnableVertexAttribArray(1)
    # texture coord attribute
    glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), ctypes.c_void_p(6 * sizeof(GLfloat)))
    glEnableVertexAttribArray(2)

    # configure the light's VAO (VBO is the same)
    light_VAO = glGenVertexArrays(1)
    glBindVertexArray(light_VAO)

    glBindBuffer(GL_ARRAY_BUFFER, VBO)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8 * sizeof(GLfloat), ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    # load and create a texture
    diffuse_map  = load_texture("/media/cl/D:/Dooo/FUN/LearnOpenGLStudy/python/02_lighting/test_img/container2.png")
    specular_map = load_texture("/media/cl/D:/Dooo/FUN/LearnOpenGLStudy/python/02_lighting/test_img/container2_specular.png")
 
    obj_shader.use()
    obj_shader.set_int("material.diffuse",  0)
    obj_shader.set_int("material.specular", 1)

    # render loop
    while not glfw.window_should_close(window):
        current_frame = glfw.get_time()
        camera.delta_time = current_frame - camera.last_frame
        camera.last_frame = current_frame

        # input
        process_input(window)
        camera.translate(window)

        # render
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # bind textures on corresponding texture units
        # Task 1: diffuse map texture
        if args.task == 0:
            # bind diffuse map
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, diffuse_map)
            glActiveTexture(GL_TEXTURE1)
            glBindTexture(GL_TEXTURE_2D, diffuse_map)      
        # Task 2: diffuse map & specular map
        elif args.task == 1:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, diffuse_map)
            glActiveTexture(GL_TEXTURE1)
            glBindTexture(GL_TEXTURE_2D, specular_map)
        else:
            raise TypeError("Wrong task number")

        # render container
        glBindVertexArray(obj_VAO)

        # object shader
        obj_shader.use()
        obj_shader.set_vec3("viewPos", camera.position)       # cam properties
        obj_shader.set_vec3("light.position", light_position) # light properties
        obj_shader.set_vec3("light.ambient",  glm.vec3(0.2))
        obj_shader.set_vec3("light.diffuse",  glm.vec3(0.5))
        obj_shader.set_vec3("light.specular", glm.vec3(1.0))
        obj_shader.set_float("material.shininess", 32)        # material properties 

        # view properties for object shader           
        proj_mat = glm.perspective(glm.radians(camera.fov), args.window_width / args.window_height, 0.1, 100.0)
        view_mat = camera.get_view_matrix()
        obj_shader.set_mat4("projection", proj_mat)
        obj_shader.set_mat4("view", view_mat)


        # create transformations
        model_mat_list = [glm.mat4(1.0)]

        # draw
        for i in range(len(model_mat_list)):
            obj_shader.set_mat4("model", model_mat_list[i])
            
            if EBO is None:
                glDrawArrays(GL_TRIANGLES, 0, 36)
            if EBO is not None:
                glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, ctypes.c_void_p(0)) # last argument is indices that specifies an offset in a buffer
                                                                                        # or a pointer to the location where the indices are stored
      
        # draw light cube
        light_shader.use()
        light_shader.set_mat4("projection", proj_mat)
        light_shader.set_mat4("view", view_mat)

        model_mat = glm.mat4(1.0)
        model_mat = glm.translate(model_mat, light_position)
        model_mat = glm.scale(model_mat, glm.vec3(0.2))
        light_shader.set_mat4("model", model_mat)

        light_shader.set_vec3("color", glm.vec3(1.0))

        glBindVertexArray(light_VAO)
        glDrawArrays(GL_TRIANGLES, 0, 36)
        

        # check and call events and swap the buffers
        glfw.swap_buffers(window)
        glfw.poll_events()

    glDeleteVertexArrays(1, obj_VAO)
    glDeleteVertexArrays(1, light_VAO)
    glDeleteBuffers(1, VBO)
    if EBO is not None:
        glDeleteBuffers(1, EBO)

    # clear all previously allocated GLFW resources
    glfw.terminate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--task", dest="task", default=1, type=float)
    parser.add_argument("-p", "--primitive", dest="primitive",     default="box")
    parser.add_argument("-m", "--mode",      dest="polygon_mode",  default="fill")

    parser.add_argument("-ww", "--window_width",  dest="window_width",  default=800)
    parser.add_argument("-wh", "--window_height", dest="window_height", default=600)

    args = parser.parse_args()

    main(args)