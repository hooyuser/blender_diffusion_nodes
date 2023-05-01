import bpy
import nodeitems_utils
import os
import sys

from . import auto_load


bl_info = {
    "name": "Diffusion Nodes",
    "description": "Stable Diffusion Nodes for Blender",
    "author": "hooyuser",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "Node Editor",
    "warning": "",  # used for warning icon and text in add-ons panel
    "wiki_url": "http://my.wiki.url",
    "tracker_url": "http://my.bugtracker.url",
    "support": "COMMUNITY",
    "category": "Node"
}

install_dependencies = False
if install_dependencies:
    import subprocess

    bundle_dir = "bundle_packages"
    requirements_file = "requirements.txt"
    python_path = sys.executable

    print(f"Installing packages from {requirements_file} into {bundle_dir} ...")

    # Set the package names and URL
    packages = ['torch', 'torchvision', 'torchaudio']
    index_url = 'https://download.pytorch.org/whl/cu118'

    # Construct the pip3 command
    pip_cmd = ['pip3', 'install', '--upgrade', '-t', bundle_dir] + packages + ['--index-url', index_url]

    # Run the pip3 command using subprocess
    subprocess.call(pip_cmd)

    # subprocess.call([
    #     python_path,
    #     "-m",
    #     "pip",
    #     "install",
    #     "-r",
    #     requirements_file,
    #     "-t",
    #     bundle_dir
    # ])

# print("Done.")
# input("Press Enter to continue...") # equivalent of 'pause' command

bundle_path = os.path.join(os.path.dirname(__file__), 'bundle_packages')
comfy_path = os.path.join(os.path.dirname(__file__), 'ComfyUI')
comfy_path2 = os.path.join(os.path.dirname(__file__), "ComfyUI", "comfy")
base_path = os.path.dirname(__file__)
if bundle_path not in sys.path:
    # insert at the end to give it lowest priority
    sys.path.insert(0, bundle_path)
    sys.path.insert(0, comfy_path)
    sys.path.insert(0, comfy_path2)
    sys.path.insert(0, base_path)

# for p in sys.path:
#     print(p)


class CustomNodeCategory(nodeitems_utils.NodeCategory):
    # define the classmethod that tells blender which node tree
    #   the categories made with this class belong to (is visible to)
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'DiffusionNodeTree'


node_categories = [
    # NOTE: did not find documentation other then template script for it
    # esentially:
    #   we instantiate a new 'nodeitems_utils.NodeCategory' class, that
    #   has been extended with a poll method that makes sure that the
    #   category and node only shows up in the desired node tree
    # The first argument is a string with its id we will use to access it by
    # the second argument is the name displayed to the user
    # the third argument is a list of (items) nodes that are under
    #   that category, the list contains instances 'nodeitems_utils.NodeItem'

    # CustomNodeCategory(
    #     "PRIMITIVES_NODES",
    #     "Primitives",
    #     items=[
    #         # the nodes (items) in this category are instantiated in this list
    #         #   with the 'nodeitems_utils.NodeItem' class, which can have
    #         #   additional settings
    #         # the first argument is the node class idname we want to add
    #         # then there can be keyword arguments like label
    #         # another argument can be a 'settings' keyword argument
    #         #   that takes a dictionary that can override default values of all
    #         #   properties
    #         #   NOTE: use 'repr()' to convert the value to string IMPORTANT
    #         nodeitems_utils.NodeItem("SphereSDF", label="Sphere"),
    #     ]),
    CustomNodeCategory(
        "INPUT_NODES",
        "Input",
        items=[
            nodeitems_utils.NodeItem("FloatInput", label="Float"),
            nodeitems_utils.NodeItem("IntegerInput", label="Integer"),
            nodeitems_utils.NodeItem("ImageInput", label="Image"),
            nodeitems_utils.NodeItem("TextInput", label="Text"),
            nodeitems_utils.NodeItem("StringInput", label="String"),
        ]),
    CustomNodeCategory(
        "LOADERS_NODES",
        "Loaders",
        items=[
            nodeitems_utils.NodeItem(
                "LoadCheckpoint", label="Load Checkpoint"),
        ]),
    CustomNodeCategory(
        "CONDITIONING_NODES",
        "Conditioning",
        items=[
            nodeitems_utils.NodeItem(
                "CLIPTextEncode", label="CLIP Text Encode"),
        ]),
    CustomNodeCategory(
        "SAMPLER_NODES",
        "Sampler",
        items=[
            nodeitems_utils.NodeItem(
                "KSampler", label="K Sampler"),
        ]),
    CustomNodeCategory(
        "LATENT_NODES",
        "Latent",
        items=[
            nodeitems_utils.NodeItem(
                "EmptyLatentImage", label="Empty Latent Image"),
        ]),
    CustomNodeCategory(
        "MISC_NODES",
        "Misc",
        items=[
            nodeitems_utils.NodeItem(
                "FloatMath", label="Float Math"),
            nodeitems_utils.NodeItem(
                "Print", label="Print"),
        ]),
]


auto_load.init()


def check_preference_base_path():
    bpy.context.preferences.addons[__name__].preferences.load_preferences()


def execute_nodetree_button(self, context):
    if context.space_data.tree_type == 'DiffusionNodeTree':
        layout = self.layout
        # show text in header
        row = layout.row(align=True)
        row.scale_x = 1.0
        row.label(text="      ")
        row.operator("diffusion_node.execute_nodetree_op", text="Execute")
        row.label(text="      ")


def register():
    auto_load.register()
    nodeitems_utils.register_node_categories("CUSTOM_NODES", node_categories)
    bpy.types.NODE_HT_header.append(execute_nodetree_button)
    check_preference_base_path()
    print("Registered Diffusion Nodes")


def unregister():
    auto_load.unregister()
    nodeitems_utils.unregister_node_categories("CUSTOM_NODES")
    bpy.types.NODE_HT_header.remove(execute_nodetree_button)
    print("Unregistered Diffusion Nodes")
