import bpy


class BaseNodeSocket(object):
    connected_output_index: bpy.props.IntProperty(default=-1)
    # bpy.types.NodeSocket.connected_output_index = -1: not connected

    def __init__(self):
        self.connected_output_index = -1

    def default_value_callback(self, context):
        pass  # call after default_value is changed


#     socket_types = [("FLOAT", "Float", "Where your feet are"),
#                     ("INT", "Int", "Where your head should be"),
#                     ("SDF", "SDF", "Not right"),
#                     ("FLOAT_VEC", "Float_Vec", "Not left"),
#                     ("UNDEFINED", "Undefined", "N")]

#     mySocketType: bpy.props.EnumProperty(name="SocketType",
#                                          description="Just an example",
#                                          items=socket_types,
#                                          default='UNDEFINED')


# class CustomNodeSocket(bpy.types.NodeSocket):
#     bl_idname = "CustomNodeSocket"
#     bl_label = "Custom Node Socket"

#     # Enum items list
#     my_items = [("DOWN", "Down", "Where your feet are"),
#                 ("UP", "Up", "Where your head should be"),
#                 ("LEFT", "Left", "Not right"), ("RIGHT", "Right", "Not left")]

#     myEnumProperty: bpy.props.EnumProperty(name="Direction",
#                                            description="Just an example",
#                                            items=my_items,
#                                            default='UP')

#     myIntProp: bpy.props.IntProperty()

#     translation: bpy.props.FloatVectorProperty(subtype='TRANSLATION')

#     # Optional function for drawing the socket input value
#     def draw(self, context, layout, node, text):
#         if self.is_output or self.is_linked:
#             layout.label(text=self.name)
#         else:
#             col = layout.column()
#             col.prop(self, "translation", text=self.name)

#     def draw_color(self, context, node):
#         return (1, 1, 1, 1)

class DiffusionSocketGeneral(bpy.types.NodeSocket, BaseNodeSocket):
    bl_idname = "DiffusionSocketGeneral"
    bl_label = "Diffusion Node Socket General"

    def draw(self, context, layout, node, text):
        layout.label(text=text)

    def draw_color(self, context, node):
        return (0.82, 0.82, 0.82, 1)


class DiffusionSocketCLIP(bpy.types.NodeSocket, BaseNodeSocket):
    bl_idname = "DiffusionSocketCLIP"
    bl_label = "Diffusion Node Socket CLIP"

    def draw(self, context, layout, node, text):
        layout.label(text='CLIP')

    def draw_color(self, context, node):
        return (0.82, 0.64, 1.0, 1)


class DiffusionSocketModel(bpy.types.NodeSocket, BaseNodeSocket):
    bl_idname = "DiffusionSocketModel"
    bl_label = "Diffusion Node Socket Model"

    def draw(self, context, layout, node, text):
        layout.label(text='Model')

    def draw_color(self, context, node):
        return (0.62, 0.84, 0.8, 1)


class DiffusionSocketVAE(bpy.types.NodeSocket, BaseNodeSocket):
    bl_idname = "DiffusionSocketVAE"
    bl_label = "Diffusion Node Socket VAE"

    def draw(self, context, layout, node, text):
        layout.label(text='VAE')

    def draw_color(self, context, node):
        return (0.32, 0.74, 0.2, 1)


class DiffusionSocketConditioning(bpy.types.NodeSocket, BaseNodeSocket):
    bl_idname = "DiffusionSocketConditioning"
    bl_label = "Diffusion Node Socket Conditioning"

    def draw(self, context, layout, node, text):
        layout.label(text='Conditioning')

    def draw_color(self, context, node):
        return (0.25, 0.14, 0.59, 1)


class DiffusionSocketText(bpy.types.NodeSocket, BaseNodeSocket):
    bl_idname = "DiffusionSocketText"
    bl_label = "Diffusion Node Socket Text"

    default_value: bpy.props.StringProperty()

    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=self.name)
        else:
            layout.prop(self, "default_value", text=self.name)

    def draw_color(self, context, node):
        return (0.77, 1.0, 0.84, 1)


class DiffusionSocketPositiveInt(bpy.types.NodeSocket, BaseNodeSocket):
    bl_idname = "DiffusionSocketPositiveInt"
    bl_label = "Diffusion Node Socket Positive Int"

    default_value: bpy.props.IntProperty(
        soft_min=0, update=BaseNodeSocket.default_value_callback)

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=self.name)
        else:
            layout.prop(self, "default_value", text=self.name)

    def draw_color(self, context, node):
        return (0.7, 0.55, 0.2, 1)


class DiffusionSocketFloat(bpy.types.NodeSocket, BaseNodeSocket):
    bl_idname = "DiffusionSocketFloat"
    bl_label = "Diffusion Node Socket Float"

    default_value: bpy.props.FloatProperty(
        update=BaseNodeSocket.default_value_callback)
    # my_type: bpy.props.StringProperty(name='mySocketType', default='FLOAT')

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        # self.my_string = 'FLOAT'
        if self.is_output or self.is_linked:
            layout.label(text=self.name)
        else:
            layout.prop(self, "default_value", text=self.name)

    def draw_color(self, context, node):
        return (0.4, 0.5, 0.6, 1)


# class SdfNodeSocketPositiveFloat(bpy.types.NodeSocket, BaseNodeSocket):
#     bl_idname = "SdfNodeSocketPositiveFloat"
#     bl_label = "SDF Node Socket Positive Float"

#     default_value: bpy.props.FloatProperty(
#         soft_min=0.0, update=BaseNodeSocket.default_value_callback)

#     # Optional function for drawing the socket input value
#     def draw(self, context, layout, node, text):
#         if self.is_output or self.is_linked:
#             layout.label(text=self.name)
#         else:
#             layout.prop(self, "default_value", text=self.name)

#     def draw_color(self, context, node):
#         return (0.643, 0.788, 0.824, 1)


# class SdfNodeSocketFloatVector(bpy.types.NodeSocket, BaseNodeSocket):

#     bl_idname = "SdfNodeSocketFloatVector"
#     bl_label = "SDF Node Socket Float Vector"

#     default_value: bpy.props.FloatVectorProperty(
#         update=BaseNodeSocket.default_value_callback)

#     # Optional function for drawing the socket input value
#     def draw(self, context, layout, node, text):
#         if self.is_output or self.is_linked:
#             layout.label(text=text)
#         else:
#             col = layout.column()
#             col.prop(self, "default_value", text=text)

#     def draw_color(self, context, node):
#         return (0.3, 0.4, 0.7, 1)


# class SdfNodeSocketColor(bpy.types.NodeSocket, BaseNodeSocket):

#     bl_idname = "SdfNodeSocketColor"
#     bl_label = "SDF Node Socket Color"

#     default_value: bpy.props.FloatVectorProperty(
#         default=(1.0, 1.0, 1.0),
#         subtype='COLOR', update=BaseNodeSocket.default_value_callback)

#     # Optional function for drawing the socket input value
#     def draw(self, context, layout, node, text):
#         if self.is_output or self.is_linked:
#             layout.label(text=text)
#         else:
#             col = layout.column()
#             col.prop(self, "default_value", text=text)

#     def draw_color(self, context, node):
#         return (0.7, 0.6, 0.3, 1)


# class SdfNodeSocketVectorTranslation(bpy.types.NodeSocket, BaseNodeSocket):

#     bl_idname = "SdfNodeSocketVectorTranslation"
#     bl_label = "SDF Node Socket Vector Translation"

#     default_value: bpy.props.FloatVectorProperty(
#         subtype='TRANSLATION', update=BaseNodeSocket.default_value_callback)

#     # Optional function for drawing the socket input value
#     def draw(self, context, layout, node, text):
#         if self.is_output or self.is_linked:
#             layout.label(text=text)
#         else:
#             col = layout.column()
#             col.prop(self, "default_value", text=text)

#     def draw_color(self, context, node):
#         return (0.4, 0.4, 0.8, 1)


# class SdfNodeSocketEuler(bpy.types.NodeSocket, BaseNodeSocket):

#     bl_idname = "SdfNodeSocketEuler"
#     bl_label = "SDF Node Socket Euler"

#     default_value: bpy.props.FloatVectorProperty(
#         default=[0, 0, 0],
#         update=BaseNodeSocket.default_value_callback,
#         subtype="EULER")

#     # Optional function for drawing the socket input value
#     def draw(self, context, layout, node, text):
#         if self.is_output or self.is_linked:
#             layout.label(text)
#         else:
#             col = layout.column()
#             col.prop(self, "default_value", text=text)

#     def draw_color(self, context, node):
#         return (0.3, 0.7, 0.45, 1)


# class SdfNodeSocketSd(bpy.types.NodeSocket):
#     bl_idname = "SdfNodeSocketSd"
#     bl_label = "SdfNodeSocketSd"

#     def draw(self, context, layout, node, text):
#         layout.label(text='SDF')

#     def draw_color(self, context, node):
#         return (0.5, 0.5, 0.5, 1)


# class SdfNodeSocketOperation(bpy.types.NodeSocket, BaseNodeSocket):
#     bl_idname = "SdfNodeSocketOperation"
#     bl_label = "SDF Node Socket Operation"

#     default_value: bpy.props.FloatVectorProperty(
#         update=BaseNodeSocket.default_value_callback)

#     def draw(self, context, layout, node, text):
#         layout.label(text='Operation')

#     def draw_color(self, context, node):
#         return (0.8, 0.3, 0.023, 1)
