import bpy

from ...base_types.base_node import BaseNode

BASIC_TEXT_INPUT_NODE_WIDTH = 200


class TextInputNode(bpy.types.Node, BaseNode):
    '''An text input node'''

    bl_idname = 'TextInput'
    bl_label = 'Text'
    bl_icon = 'TEXT'

    # def update_prop(self, context):
    #     for link in self.outputs[0].links:
    #         link.to_socket.default_value = self.value

    text: bpy.props.PointerProperty(type=bpy.types.Text)

    def init(self, context):
        BaseNode.base_init(self, context)
        self.index = -3
        self.outputs.new('DiffusionSocketText', "Text")
        self.width = BASIC_TEXT_INPUT_NODE_WIDTH

    def draw_buttons(self, context, layout):
        # create a slider for int values
        # layout.prop(self, 'text', text='Text')
        layout.template_ID(self, "text", new="text.new",
                        unlink="text.unlink", open="text.open")
