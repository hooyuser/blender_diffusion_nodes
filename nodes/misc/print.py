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
