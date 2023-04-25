import bpy

from ...base_types.base_node import BaseNode

from pathlib import Path

BASIC_CHECKPOINT_LOADER_NODE_WIDTH = 300


def checkpoint_items_callback(scene, context):
    # Your code to refresh the nodes goes here
    addon_prefs = context.preferences.addons["blender_diffusion_nodes"].preferences
    asset_base_path = Path(addon_prefs.base_dir)
    checkpoint_path = Path(addon_prefs.checkpoint_dir)

    # check if checkpoint path is relative or absolute
    if not checkpoint_path.is_absolute():
        checkpoint_path = asset_base_path / checkpoint_path

    files = [f for f in checkpoint_path.glob(
        '**/*') if f.suffix in ('.safetensors', '.ckpt')]

    # sort the files
    files.sort(key=lambda x: x.stem, reverse=True)

    return [(str(i), filename.stem, filename.name) for i, filename in enumerate(files)]


class LoadCheckpointNode(bpy.types.Node, BaseNode):
    '''A Load checkpoint node'''

    bl_idname = 'LoadCheckpoint'
    bl_label = 'Load Checkpoint'
    bl_icon = 'TEXT'

    checkpoint_enum: bpy.props.EnumProperty(
        items=checkpoint_items_callback,
        name='Checkpoint',
        description='Checkpoint to load'
    )

    def init(self, context):
        BaseNode.base_init(self, context)
        self.outputs.new('DiffusionSocketModel', "Model")
        self.outputs.new('DiffusionSocketCLIP', "CLIP")
        self.outputs.new('DiffusionSocketVAE', "VAE")
        self.width = BASIC_CHECKPOINT_LOADER_NODE_WIDTH

    def draw_buttons(self, context, layout):
        # add row
        row = layout.row()
        row.prop(self, 'checkpoint_enum', text='Checkpoint')
