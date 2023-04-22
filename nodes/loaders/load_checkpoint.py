import bpy

from ...base_types.base_node import BaseNode

from pathlib import Path

BASIC_CHECKPOINT_LOADER_NODE_WIDTH = 300

checkpoint_enum_list = [
    ('0', '0', '0'),
    ('1', '1', '1'),
    ('2', '2', '2'),
    ('3', '3', '3'),
    ('4', '4', '4'),
    ('5', '5', '5'),
    ('6', '6', '6'),
]


class NODE_OT_refresh(bpy.types.Operator):
    bl_idname = "node.refresh"
    bl_label = "Refresh Nodes"
    bl_description = "Refresh the nodes in the editor"

    def execute(self, context):
        # Your code to refresh the nodes goes here
        addon_prefs = context.preferences.addons["blender_diffusion_nodes"].preferences
        asset_base_path = Path(addon_prefs.base_dir)
        checkpoint_path = Path(addon_prefs.checkpoint_dir)

        # check if checkpoint path is relative or absolute
        if not checkpoint_path.is_absolute():
            checkpoint_path = asset_base_path / checkpoint_path

        checkpoint_suffixes = ('.safetensors', '.ckpt')
        files = [f.stem for f in checkpoint_path.glob(
            '**/*') if f.suffix in checkpoint_suffixes]
        print(files)

        return {'FINISHED'}


class LoadCheckpointNode(bpy.types.Node):
    '''A Load checkpoint node'''

    bl_idname = 'LoadCheckpoint'
    bl_label = 'Load Checkpoint'
    bl_icon = 'TEXT'

    # def update_prop(self, context):
    #     for link in self.outputs[0].links:
    #         link.to_socket.default_value = self.value

    checkpoint_enum: bpy.props.EnumProperty(
        items=checkpoint_enum_list,
        name='Checkpoint',
        description='Checkpoint to load',
        default='0',
    )

    def init(self, context):
        BaseNode.base_init(self, context)
        #self.index = -3
        self.outputs.new('DiffusionSocketModel', "Model")
        self.outputs.new('DiffusionSocketCLIP', "CLIP")
        self.outputs.new('DiffusionSocketVAE', "VAE")
        self.width = BASIC_CHECKPOINT_LOADER_NODE_WIDTH

    def draw_buttons(self, context, layout):
        # create a slider for int values
        # add row
        row = layout.row()
        row.prop(self, 'checkpoint_enum', text='Checkpoint')

        # add refresh button to row
        row.operator('node.refresh', text='', icon='FILE_REFRESH')
        # define refresh button operator
