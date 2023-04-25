import bpy

from ...base_types.base_node import BaseNode


class FloatInputNode(bpy.types.Node, BaseNode):
    '''A simple input node'''

    bl_idname = 'FloatInput'
    bl_label = 'Float'
    bl_icon = 'FILE_FONT'

    # def update_prop(self, context):
    #     for link in self.outputs[0].links:
    #         link.to_socket.default_value = self.value
            # Draw.update_callback(update_node=link.to_node)

    value: bpy.props.FloatProperty()

    def init(self, context):
        BaseNode.base_init(self, context)
        self.index = -3
        self.outputs.new('DiffusionSocketFloat', "Value")

    def draw_buttons(self, context, layout):
        # create a slider for int values
        layout.prop(self, 'value', text='Float')
