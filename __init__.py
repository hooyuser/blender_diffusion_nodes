import bpy
import nodeitems_utils

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
    #         nodeitems_utils.NodeItem("BoxSDF", label="Box"),
    #         nodeitems_utils.NodeItem("PlaneSDF", label="Plane"),
    #         nodeitems_utils.NodeItem("TorusSDF", label="Torus"),
    #         nodeitems_utils.NodeItem("CylinderSDF", label="Cylinder"),
    #         nodeitems_utils.NodeItem("ConeSDF", label="Cone")
    #     ]),
    # CustomNodeCategory("OPERATION_NODES",
    #                    "Operation",
    #                    items=[
    #                        nodeitems_utils.NodeItem("Transform",
    #                                                 label="Transform"),
    #                        nodeitems_utils.NodeItem("Round", label="Round"),
    #                        nodeitems_utils.NodeItem("Solidify",
    #                                                 label="Solidify"),
    #                        nodeitems_utils.NodeItem("Array", label="Array"),
    #                        nodeitems_utils.NodeItem("Mirror", label="Mirror"),
    #                        nodeitems_utils.NodeItem("ClippedMirror",
    #                                                 label="Clipped Mirror"),
    #                        nodeitems_utils.NodeItem("Elongate",
    #                                                 label="Elongate"),
    #                        nodeitems_utils.NodeItem("Bend", label="Bend"),
    #                        nodeitems_utils.NodeItem("Twist", label="Twist"),
    #                    ]),
    # CustomNodeCategory("CONSTRUCTION_NODES",
    #                    "Construction",
    #                    items=[
    #                        nodeitems_utils.NodeItem("Bool", label="Bool"),
    #                        nodeitems_utils.NodeItem("SmoothBool",
    #                                                 label="Smooth Bool"),
    #                        nodeitems_utils.NodeItem("Blend", label="Blend"),
    #                    ]),
    # CustomNodeCategory("MATERIAL_NODES",
    #                    "Material",
    #                    items=[
    #                        nodeitems_utils.NodeItem("PBRMaterial", label="PBR Material"),
    #                    ]),
    # CustomNodeCategory("DISPLACEMENT_NODES",
    #                    "Displacement",
    #                    items=[
    #                        nodeitems_utils.NodeItem("SimplexNoise",
    #                                                 label="Simplex Noise"),
    #                        nodeitems_utils.NodeItem("FbmNoise",
    #                                                 label="FBM Noise"),
    #                        nodeitems_utils.NodeItem("WhiteNoise",
    #                                                 label="White Noise"),
    #                    ]),
    CustomNodeCategory("INPUT_NODES",
                       "Input",
                       items=[
                           nodeitems_utils.NodeItem("FloatInput",
                                                    label="Float"),
                           nodeitems_utils.NodeItem("IntegerInput",
                                                    label="Integer"),
                           nodeitems_utils.NodeItem("ImageInput",
                                                    label="Image"),
                       ]),
    # CustomNodeCategory("OUTPUT_NODES",
    #                    "Output",
    #                    items=[
    #                        nodeitems_utils.NodeItem("Viewer", label="Viewer"),
    #                    ]),
    # CustomNodeCategory("MATH_NODES",
    #                    "Math",
    #                    items=[
    #                        nodeitems_utils.NodeItem("FloatMath",
    #                                                 label="Float Math"),
    #                    ]),
    # CustomNodeCategory(
    #     "MISC_NODES",
    #     "Misc",
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
    #         nodeitems_utils.NodeItem("Add",
    #                                  label="Add",
    #                                  settings={"intProp": repr(1.0)}),
    #         # minimalistic node addition is like this
    #         # nodeitems_utils.NodeItem("CustomSimpleInputNode"),
    #     ]),
]


auto_load.init()


def register():
    auto_load.register()
    nodeitems_utils.register_node_categories("CUSTOM_NODES", node_categories)
    print("Registered Diffusion Nodes")


def unregister():
    auto_load.unregister()
    nodeitems_utils.unregister_node_categories("CUSTOM_NODES")
    print("Unregistered Diffusion Nodes")
