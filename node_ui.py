import bpy


class DiffusionNodeTree(bpy.types.NodeTree):
    # the docstring here is used to generate documentation but
    #   also used to display a description to the user
    '''A custom node tree type'''
    # then we can give it a custom id to access it, if not given
    #   it will use the classname by default
    bl_idname = 'DiffusionNodeTree'
    # the label is the name that will be displayed to the user
    bl_label = 'Diffusion Nodes'
    # the icon that will be displayed in the UI
    # NOTE: check the blender dev plugins to see icons in text editor
    bl_icon = 'SCRIPTPLUGINS'


class ExecuteNodetreeOp(bpy.types.Operator):
    bl_idname = "diffusion_node.execute_nodetree_op"
    bl_label = "My Operator"

    def execute(self, context):
        # Code to run when the button is clicked
        print("start executing")
        return {'FINISHED'}


class DiffusionNodePanel(bpy.types.Panel):
    bl_label = "Diffusion Nodes"
    bl_idname = "DIFFUSION_PT_NODE_PANEL"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = 'UI'
    bl_category = "Node Tree"
    bl_context = 'objectmode'
    bl_order = 2

    @classmethod
    def poll(cls, context):
        try:
            return context.space_data.node_tree.bl_idname == 'DiffusionNodeTree'
        except:
            return False

    def draw(self, context):
        layout = self.layout
