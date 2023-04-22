import bpy
import nodeitems_utils

from . import auto_load
from pathlib import Path


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
