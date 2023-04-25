import bpy
import dask


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


def change_args_to_tuples(func, index_list):
    def new_func(*tuples):
        args = [tuples[i][index_list[i]] for i in range(len(tuples))]
        return func(*args)
    return new_func


def has_connected_output(node):
    for output in node.outputs:
        if output.is_linked:
            return True
    return False


class ExecuteNodetreeOp(bpy.types.Operator):
    bl_idname = "diffusion_node.execute_nodetree_op"
    bl_label = "My Operator"

    def execute(self, context):
        # Code to run when the button is clicked
        print("\nStart executing")

        node_tree = context.space_data.edit_tree
        node_vectors = topological_sort(node_tree.nodes)
        dask_tasks = {}
        leaf_tasks = []

        for i, node in enumerate(node_vectors):
            print(f'{i}: executing node {node.name}')

            # for input_socket in node.inputs:
            #     print(
            #         f'input socket {input_socket.name}: {input_socket.connected_output_index}')

            input_tasks = [
                dask_tasks[input_socket.links[0].from_node]
                if input_socket.is_linked else (input_socket.default_value,)
                for input_socket in node.inputs]

            tuple_index_list = [
                max(input_socket.connected_output_index, 0)
                for input_socket in node.inputs]

            delayed_func = dask.delayed(
                change_args_to_tuples(node.compute, tuple_index_list))
            dask_tasks[node] = delayed_func(*input_tasks)

            if not has_connected_output(node):
                leaf_tasks.append(dask_tasks[node])

        # for k, task in dask_tasks.items():
        #     print(f'key: {k.name}, task: {task}')
        #     print(task.dask)
        # dask.compute(*dask_tasks.values())
        # task.compute()
        # print(f'leaf tasks: {leaf_tasks}')
        dask.compute(leaf_tasks)

        return {'FINISHED'}
