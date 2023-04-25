from gpu_extras.batch import batch_for_shader
import bpy
import gpu

from ...base_types.base_node import BaseNode
from ...preview_shader import create_preview_shader
from bpy.types import SpaceNodeEditor


preview_handle_dict = dict()

BASIC_NODE_WIDTH = 200


def view_to_region_scaled(context, x, y, clip=True):
    ui_scale = context.preferences.system.ui_scale
    return context.region.view2d.view_to_region(
        x * ui_scale, y * ui_scale, clip=clip)


def gen_draw_func(texture, image_size, para_func):
    '''
    texture will be fisrt scaled by scale_func, then offset by offset_func
    '''
    shader = create_preview_shader()

    x, y = 0, 0
    w, h = image_size

    batch = batch_for_shader(
        shader, 'TRI_FAN',
        {   # 4 corner points: (top left, top right, bottom right, bottom left)
            "pos": ((x, y), (x + w, y), (x + w, y - h), (x, y - h)),
            "uv": ((0, 1), (1, 1), (1, 0), (0, 0)),
        },
    )

    def draw(context):
        scale, offset_x, offset_y = para_func(context)

        shader.bind()
        shader.uniform_sampler("image", texture)
        shader.uniform_float("viewProjectionMatrix",
                             gpu.matrix.get_projection_matrix())
        shader.uniform_float("scale", scale)
        shader.uniform_float("offset_x", offset_x)
        shader.uniform_float("offset_y", offset_y)

        batch.draw(shader)

    return draw


def tag_redraw_all_nodeviews():
    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            if area.type == 'NODE_EDITOR':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        region.tag_redraw()


class ImageInputNode(bpy.types.Node, BaseNode):
    '''An integer input node'''

    bl_idname = 'ImageInput'
    bl_label = 'Image'
    bl_icon = 'IMAGE_DATA'

    def update_prop(self, context):
        for link in self.outputs[0].links:
            link.to_socket.default_value = self.value
            # Draw.update_callback(update_node=link.to_node)

    def get_preview_parameters(self, context):
        '''
        return (scale, top_left_pos_x, top_left_pos_y)
        '''

        ui_scale = context.preferences.system.ui_scale
        image_width, image_height = self.image.size
        aspect_ratio = image_width / image_height
        short_side = BASIC_NODE_WIDTH * self.preview_scale

        if aspect_ratio > 1:
            preview_width = short_side * aspect_ratio
            preview_height = short_side
        else:
            preview_width = short_side
            preview_height = short_side / aspect_ratio

        pos_x, pos_y = self.location
        pos_y += 3  # spacing between node and preview
        return (
            (preview_width / image_width) * ui_scale,
            (pos_x + 0.5 * (self.width - preview_width)) * ui_scale,
            (pos_y + preview_height) * ui_scale,
        )

    def update_preview(self, context):
        if self.enabled_preview:

            draw_func = gen_draw_func(
                texture=gpu.texture.from_image(self.image),
                image_size=self.image.size,
                para_func=lambda
                context: self.get_preview_parameters(context),)

            preview_handle_dict[self.unique_id] = SpaceNodeEditor.draw_handler_add(
                draw_func, (context,), 'WINDOW', 'POST_VIEW')
            tag_redraw_all_nodeviews()
        else:
            SpaceNodeEditor.draw_handler_remove(
                preview_handle_dict[self.unique_id], 'WINDOW')
            tag_redraw_all_nodeviews()

    def recreate_preview(self, context):
        if self.enabled_preview:
            SpaceNodeEditor.draw_handler_remove(
                preview_handle_dict[self.unique_id], 'WINDOW')
            draw_func = gen_draw_func(
                texture=gpu.texture.from_image(self.image),
                image_size=self.image.size,
                para_func=lambda
                context: self.get_preview_parameters(context),)

            preview_handle_dict[self.unique_id] = SpaceNodeEditor.draw_handler_add(
                draw_func, (context,), 'WINDOW', 'POST_VIEW')
            tag_redraw_all_nodeviews()

    image: bpy.props.PointerProperty(
        type=bpy.types.Image, update=recreate_preview)
    texture: bpy.props.PointerProperty(
        type=bpy.types.ImageTexture, update=recreate_preview)

    enabled_preview: bpy.props.BoolProperty(name="Enabled_collision",
                                            default=False,
                                            update=update_preview)
    preview_scale: bpy.props.FloatProperty(
        name="Preview_scale",
        description="scale factor for preview image",
        default=1.2,
        min=0)

    def init(self, context):
        BaseNode.base_init(self, context)
        self.texture = bpy.data.textures.new(
            f"preview_texture_{self.unique_id}", type='IMAGE')
        self.index = -3
        self.outputs.new('DiffusionSocketPositiveInt', "Value")
        self.width = BASIC_NODE_WIDTH

    def draw_buttons(self, context, layout):
        # create a slider for int values
        layout.template_image(
            self, "image", self.texture.image_user, compact=False,
            multiview=True)

        layout.prop(self, "enabled_preview", text="Preview")
        if self.enabled_preview:
            layout.prop(self, "preview_scale", text="Preview Scale")

    def free(self):
        if self.unique_id in preview_handle_dict:
            SpaceNodeEditor.draw_handler_remove(
                preview_handle_dict[self.unique_id], 'WINDOW')
            tag_redraw_all_nodeviews()
            del preview_handle_dict[self.unique_id]
