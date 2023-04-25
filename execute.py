import bpy


def get_custom_nodes(context):
    # for node in context.space_data.edit_tree.nodes:
    #     print(node.bl_idname)
    return [node for node in context.space_data.edit_tree.nodes]


def topological_sort(node_vectors):
    sorted_nodes = []
    visited = set()

    def dfs_iterative(node):
        stack = [node]

        while stack:
            current_node = stack[-1]

            if current_node not in visited:
                visited.add(current_node)
                unvisited_outputs = [
                    link.to_node
                    for output in current_node.outputs for link in output.links
                    if link.to_node not in visited]

                if unvisited_outputs:
                    stack.extend(unvisited_outputs)
                else:
                    sorted_nodes.append(current_node)
                    stack.pop()
            else:
                stack.pop()

    for node in node_vectors:
        if node not in visited:
            dfs_iterative(node)

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
            # node.execute(context)
        return {'FINISHED'}
