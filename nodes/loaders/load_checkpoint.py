import bpy

from ...base_types.base_node import BaseNode
from comfy.sd import load_checkpoint_guess_config

from pathlib import Path

BASIC_CHECKPOINT_LOADER_NODE_WIDTH = 300


def get_checkpoint_file_paths():
    # Your code to refresh the nodes goes here
    addon_prefs = bpy.context.preferences.addons["blender_diffusion_nodes"].preferences
    asset_base_path = Path(addon_prefs.base_dir)
    checkpoint_path = Path(addon_prefs.checkpoint_dir)

    # check if checkpoint path is relative or absolute
    if not checkpoint_path.is_absolute():
        checkpoint_path = asset_base_path / checkpoint_path

    files = [f for f in checkpoint_path.glob(
        '**/*') if f.suffix in ('.safetensors', '.ckpt')]

    # sort the files
    files.sort(key=lambda x: x.stem, reverse=True)

    return files


def checkpoint_items_callback(scene, context):
    files = get_checkpoint_file_paths()
    return [(str(i), filename.stem, filename.name) for i, filename in enumerate(files)]


class LoadCheckpointNode(bpy.types.Node, BaseNode):
    '''A Load checkpoint node'''

    bl_idname = 'LoadCheckpoint'
    bl_label = 'Load Checkpoint'
    bl_icon = 'ASSET_MANAGER'

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

    def compute(self, *args):
        checkpoint_path = get_checkpoint_file_paths()[
            int(self.checkpoint_enum)]
        result = load_checkpoint_guess_config(str(checkpoint_path))
        # model, clip, vae, ignore clipvision
        return (result[0], result[1], result[2])
