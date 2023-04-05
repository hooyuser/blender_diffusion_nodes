import bpy

from ...base_types.base_node import BaseNode

BASIC_CLIP_TEXT_ENCODE_NODE_WIDTH = 170


class CLIPTextEncodeNode(bpy.types.Node):
    '''CLIP Text Encode Node'''

    bl_idname = 'CLIPTextEncode'
    bl_label = 'CLIP Text Encode'
    bl_icon = 'ALIGN_LEFT'

    # def update_prop(self, context):
    #     for link in self.outputs[0].links:
    #         link.to_socket.default_value = self.value

    def init(self, context):
        BaseNode.base_init(self, context)
        self.index = -3
        self.inputs.new('DiffusionSocketCLIP', "CLIP")
        self.inputs.new('DiffusionSocketText', "Text")
        self.outputs.new('SdfNodeSocketPositiveInt', "Conditioning")
        self.width = BASIC_CLIP_TEXT_ENCODE_NODE_WIDTH

    #def draw_buttons(self, context, layout):
        # create a slider for int values
        #layout.prop(self, 'text', text='Text')

        # def update(self):
        #     if self.outputs[0].links:
        #         tree = bpy.context.space_data.edit_tree
        #         for link in self.outputs[0].links:
        #             if link.to_socket.bl_idname in int_category:
        #                 link.to_socket.default_value = self.value
        #             else:
        #                 tree.links.remove(link)
