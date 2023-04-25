import bpy

from ...base_types.base_node import BaseNode

BASIC_STRING_INPUT_NODE_WIDTH = 200


class StringInputNode(bpy.types.Node, BaseNode):
    '''An string input node'''

    bl_idname = 'StringInput'
    bl_label = 'String'
    bl_icon = 'TEXT'

    # def update_prop(self, context):
    #     for link in self.outputs[0].links:
    #         link.to_socket.default_value = self.value

    string_text: bpy.props.StringProperty()

    def init(self, context):
        BaseNode.base_init(self, context)
        self.outputs.new('DiffusionSocketText', "Text")
        self.width = BASIC_STRING_INPUT_NODE_WIDTH

    def draw_buttons(self, context, layout):
        # create a slider for int values
        layout.prop(self, 'string_text', text='Text')

    # def update(self):
    #     if self.outputs[0].links:
    #         tree = bpy.context.space_data.edit_tree
    #         for link in self.outputs[0].links:
    #             if link.to_socket.bl_idname in int_category:
    #                 link.to_socket.default_value = self.value
    #             else:
    #                 tree.links.remove(link)
