import bpy


def get_custom_nodes(context):
    # for node in context.space_data.edit_tree.nodes:
    #     print(node.bl_idname)
    return [node for node in context.space_data.edit_tree.nodes]


def topological_sort(node_vectors):
    sorted_nodes = []
    stack = []
    visited = set()

    for node in node_vectors:
        if node not in visited:
            stack.append(node)
            while stack:
                current_node = stack[-1]
                visited.add(current_node)
                unvisited_neighbor = None
                for output_idx, output in enumerate(current_node.outputs):
                    for link in output.links:
                        link.to_socket.connected_output_index = output_idx
                        if link.to_node not in visited:
                            unvisited_neighbor = link.to_node
                            break
                if unvisited_neighbor is None:
                    sorted_nodes.append(stack.pop())
                else:
                    stack.append(unvisited_neighbor)

    return sorted_nodes[::-1]


class ExecuteNodetreeOp(bpy.types.Operator):
    bl_idname = "diffusion_node.execute_nodetree_op"
    bl_label = "My Operator"

    def execute(self, context):
        # Code to run when the button is clicked
        print("\nstart executing")
        # my_custom_nodes = get_custom_nodes(context)
        # for node in my_custom_nodes:
        #     print(f'executing node {node.name}')
        node_tree = context.space_data.edit_tree
        node_vectors = topological_sort(node_tree.nodes)
        for i, node in enumerate(node_vectors):
            print(f'{i}: executing node {node.name}')
            for input_socket in node.inputs:
                print(f'input socket {input_socket.name}: {input_socket.connected_output_index}')
            # node.execute(context)
        return {'FINISHED'}
