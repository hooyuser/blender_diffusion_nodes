import bpy

from ...base_types.base_node import BaseNode


class PrintNode(bpy.types.Node, BaseNode):
    '''A Print node'''

    bl_idname = 'Print'
    bl_label = 'Print'
    bl_icon = 'ALIGN_TOP'

    def init(self, context):
        BaseNode.base_init(self, context)
        self.inputs.new('DiffusionSocketGeneral', "Input")

    def compute(self, x):
        linked_node = self.inputs[0].links[0].from_node
        linked_socket = self.inputs[0].links[0].from_socket
        print(f'Print result for Node "{linked_node.name}" - Socket "{linked_socket.name}"\n{x}\n')
