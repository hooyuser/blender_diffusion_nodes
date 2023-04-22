import bpy

from pathlib import Path
import json

# the user preferences directory, eg. Blender\3.6\config\scripts\addons\blender_diffusion_nodes
preference_dir = Path(
    bpy.utils.user_resource('CONFIG')).joinpath(
    'scripts', 'addons', __package__)

# define the file path and write the data to the file
preference_json_path = preference_dir.joinpath('preferences.json')


class DiffusionNodesPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    def update_base_path(self, context):
        # create the preferences directory if it doesn't exist
        preference_dir.mkdir(parents=True, exist_ok=True)

        # serialize the string properties, except the ones starting with bl_ or __
        prop_data = {
            attr: getattr(self, attr) for attr in dir(self)
            if
            isinstance(getattr(self, attr),
                       str) and not attr.startswith('__') and
            not attr.startswith('bl_')}

        with open(preference_json_path, 'w') as f:
            json.dump(prop_data, f)

    def load_preferences(self):
        # deserialize the data
        with open(preference_json_path, 'r') as f:
            prop_data = json.load(f)

        # set the properties dynamically
        for key, value in prop_data.items():
            setattr(self, key, value)

    base_dir: bpy.props.StringProperty(
        name="Base Path",
        subtype='FILE_PATH',
        default="",
        description="Base path for all models and configs",
        update=update_base_path
    )

    checkpoint_dir: bpy.props.StringProperty(
        name="Checkpoint Directory",
        subtype='FILE_PATH',
        default="models/Stable-diffusion"
    )

    config_dir: bpy.props.StringProperty(
        name="Config Directory",
        subtype='FILE_PATH',
        default="models/Stable-diffusion"
    )

    vae_dir: bpy.props.StringProperty(
        name="VAE Directory",
        subtype='FILE_PATH',
        default="models/VAE"
    )

    LoRA_dir: bpy.props.StringProperty(
        name="LoRA Directory",
        subtype='FILE_PATH',
        default="models/Lora"
    )

    embedding_dir: bpy.props.StringProperty(
        name="Embedding Directory",
        subtype='FILE_PATH',
        default="embeddings"
    )

    controlnet_dir: bpy.props.StringProperty(
        name="ControlNet Directory",
        subtype='FILE_PATH',
        default="models/ControlNet"
    )

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, "base_dir")
        row = layout.row()
        row.prop(self, "checkpoint_dir")
        row = layout.row()
        row.prop(self, "config_dir")
        row = layout.row()
        row.prop(self, "vae_dir")
        row = layout.row()
        row.prop(self, "LoRA_dir")
        row = layout.row()
        row.prop(self, "embedding_dir")
        row = layout.row()
        row.prop(self, "controlnet_dir")
        row = layout.row()
