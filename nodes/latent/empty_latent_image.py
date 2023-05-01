import bpy

from ...base_types.base_node import BaseNode

import torch


class EmptyLatentImageNode(bpy.types.Node, BaseNode):
    '''Empty Latent Image node'''

    bl_idname = 'EmptyLatentImage'
    bl_label = 'Empty Latent Image'
    bl_icon = 'FILE_FONT'

    def init(self, context):
        BaseNode.base_init(self, context)
        self.inputs.new('DiffusionSocketPositiveInt', "Width")
        self.inputs["Width"].default_value = 512
        self.inputs.new('DiffusionSocketPositiveInt', "Height")
        self.inputs["Height"].default_value = 512
        self.inputs.new('DiffusionSocketPositiveInt', "Batch Size")
        self.inputs["Batch Size"].default_value = 1
        self.outputs.new('DiffusionSocketLatent', "Latent")

    def compute(self, width, height, batch_size):
        latent = torch.zeros([batch_size, 4, height // 8, width // 8])
        return ({"samples": latent}, )
