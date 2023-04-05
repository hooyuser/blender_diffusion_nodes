import bpy

from ...base_types.base_node import BaseNode

BASIC_TEXT_INPUT_NODE_WIDTH = 200

class TextInputNode(bpy.types.Node):
    '''An text input node'''

    bl_idname = 'TextInput'
    bl_label = 'Text'
    bl_icon = 'TEXT'

    # def update_prop(self, context):
    #     for link in self.outputs[0].links:
    #         link.to_socket.default_value = self.value


    text: bpy.props.StringProperty()

    def init(self, context):
        BaseNode.base_init(self, context)
        self.index = -3
        self.outputs.new('SdfNodeSocketPositiveInt', "Value")
        self.width = BASIC_TEXT_INPUT_NODE_WIDTH

    def draw_buttons(self, context, layout):
        # create a slider for int values
        layout.prop(self, 'text', text='Text')

    # def update(self):
    #     if self.outputs[0].links:
    #         tree = bpy.context.space_data.edit_tree
    #         for link in self.outputs[0].links:
    #             if link.to_socket.bl_idname in int_category:
    #                 link.to_socket.default_value = self.value
    #             else:
    #                 tree.links.remove(link)
