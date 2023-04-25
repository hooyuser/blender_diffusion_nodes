import bpy


def socket_types_compatible(from_type, to_type):
    # Replace this with your conversion rules
    compatible_types = {
        'DiffusionSocketCLIP': ['DiffusionSocketCLIP'],
        'DiffusionSocketModel': ['DiffusionSocketModel'],
        'DiffusionSocketVAE': ['DiffusionSocketVAE'],
        'DiffusionSocketText': ['DiffusionSocketText'],
        'DiffusionSocketFloat': ['DiffusionSocketFloat'],
        'DiffusionSocketPositiveInt': ['DiffusionSocketPositiveInt', 'DiffusionSocketFloat'],
    }
    return to_type in compatible_types[from_type]


class UniqueIdManager:
    # Static private member variable
    _max_id = -1

    # Static public member method to get the next ID
    @staticmethod
    def get_id():
        # Access the static private member variable
        UniqueIdManager._max_id += 1
        return UniqueIdManager._max_id


class BaseNode(object):
    # this line makes the node visible only to the 'SDFNodeTree'
    #   node tree, essentially checking context
    bpy.types.Node.index = bpy.props.IntProperty()
    bpy.types.Node.coll_index = bpy.props.IntProperty()
    # index = -1: to be searched. index = -2: will not be searched

    # bpy.types.Node.ref_num = bpy.props.IntProperty()
    # bpy.types.Node.coll_ref_num = bpy.props.IntProperty()
    # ref_num actually equals the referencing number - 1

    # bpy.types.Node.coll_para_idx = bpy.props.IntProperty()
    # the index of the first parameter of a node
    bpy.types.Node.unique_id = bpy.props.IntProperty()

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'DiffusionNodeTree'

    def base_init(self, context):
        self.unique_id = UniqueIdManager.get_id()

    def update(self):
        if self.outputs:
            tree = bpy.context.space_data.edit_tree
            for output_socket in self.outputs:
                for link in output_socket.links:
                    input_socket = link.to_socket
                    if not socket_types_compatible(output_socket.bl_idname, input_socket.bl_idname):
                        tree.links.remove(link)
                        # tree.links.new(self.outputs[0],
                        #             to_node.inputs[-1]).is_valid = True

        # self.last_update = self
