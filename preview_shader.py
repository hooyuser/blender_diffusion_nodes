import gpu
from gpu_extras.batch import batch_for_shader


def create_preview_shader():
    vert_out = gpu.types.GPUStageInterfaceInfo("my_interface")
    vert_out.smooth('VEC2', "uv_interp")

    shader_info = gpu.types.GPUShaderCreateInfo()
    shader_info.push_constant('MAT4', "viewProjectionMatrix")
    shader_info.push_constant('FLOAT', "scale")
    shader_info.push_constant('FLOAT', "offset_x")
    shader_info.push_constant('FLOAT', "offset_y")
    shader_info.sampler(0, 'FLOAT_2D', "image")
    shader_info.vertex_in(0, 'VEC2', "pos")
    shader_info.vertex_in(1, 'VEC2', "uv")
    shader_info.vertex_out(vert_out)
    shader_info.fragment_out(0, 'VEC4', "FragColor")
    vertex_shader = '''
        void main() 
        {
            gl_Position = viewProjectionMatrix * vec4(pos.x * scale + offset_x, pos.y * scale + offset_y, 0.0f, 1.0f);
            //gl_Position.z = 1.0f;
            uv_interp = uv;
        }
    '''
    shader_info.vertex_source(vertex_shader)
    fragment_shader = """
        void main()
        {
            vec4 texture_color = texture(image, uv_interp);
            texture_color.rgb = pow(texture_color.rgb, vec3(1.0 / 2.2f));
            FragColor = texture_color;
        }
    """
    shader_info.fragment_source(fragment_shader)

    shader = gpu.shader.create_from_info(shader_info)
    del vert_out
    del shader_info
    return shader
