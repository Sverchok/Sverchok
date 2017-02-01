
import bpy
from bpy.props import EnumProperty


_node_funcs = {}


class NodeBase:

    @staticmethod
    def add_func(func):
        _node_funcs[func.bl_idname] = func

    @staticmethod
    def get_func(bl_idname):
        return _node_funcs.get(bl_idname)

    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname in {'SvRxTree'}

    def init(self, context):
        self.adjust_sockets()

    def compile(self):
        return _node_funcs[self.bl_idname]

    def draw_buttons(self, context, layout):
        props = self.compile().properties

        for name in props.keys():
            layout.prop(self, name)

    def adjust_sockets(self):
        func = self.compile()
        self.adjust_inputs(func.inputs_template)
        self.adjust_outputs(func.inputs_template)


    def adjust_inputs(self, template):
        inputs_template = template
        for socket, socket_data in zip(self.inputs, inputs_template):
            socket.replace_socket(*socket_data)

        diff = len(self.inputs) - len(inputs_template)

        if diff > 0:
            for i in range(diff):
                self.inputs.remove(self.inputs[-1])
        elif diff < 0:
            for bl_id, name, default in inputs_template[diff:]:
                print(bl_id, name, default)
                s = self.inputs.new(bl_id, name)
                if default is not None:
                    s.default_value = default

    def adjust_outputs(self, template):
        outputs_template = template

        for socket, socket_data in zip(self.outputs, outputs_template):
            socket.replace_socket(*socket_data)

        diff = len(self.outputs) - len(outputs_template)

        if diff > 0:
            for i in range(diff):
                self.outputs.remove(self.outputs[-1])
        elif diff < 0:
            for bl_id, name in outputs_template[diff:]:
                s = self.outputs.new(bl_id, name)


_node_classes = {}

class NodeStateful(NodeBase):

    @staticmethod
    def add_cls(bl_idname, func_cls):
        _node_classes[bl_idname] = func_cls

    @staticmethod
    def get_cls(bl_idname):
        return _node_classes[bl_idname]

    def compile(self):
        return NodeStateful.get_cls(self.bl_idname)(self)


_multi_storage = {}

class NodeDynSignature(NodeBase):

    @staticmethod
    def add_multi(func):
        if not func.bl_idname in _multi_storage:
            _multi_storage[func.bl_idname] = ({}, [])
        func_dict, func_list = _multi_storage[func.bl_idname]
        func_list.append((func.label, func.label, func.label, func.id))
        func_dict[func.label] = func

    @staticmethod
    def get_multi(func):
        return _multi_storage[func.bl_idname]


    def compile(self):
        func_dict, _ = _multi_storage[self.bl_idname]
        return func_dict[self.mode]

    def update_mode(self, context):
        self.adjust_sockets()
        self.id_data.update()

    def draw_buttons(self, context, layout):
        layout.prop(self, 'mode')
        super().draw_buttons(context, layout)



socket_types = [
    ('default', 'default', 'default', 0),
    ('SvRxFloatSocket', 'Float', 'Float', 1),
    ('SvRxIntSocket', 'Int', 'Int', 2),

]


class NodeMathBase(NodeDynSignature):

    first_input = EnumProperty(items=socket_types,
                              default="default",
                              update=NodeDynSignature.update_mode)
    second_input = EnumProperty(items=socket_types,
                                default="default",
                                update=NodeDynSignature.update_mode)

    def draw_label(self):
        """
        draws label for mutli mode nodes like math, logic and trigonometey
        """
        if not self.hide:
            return self.label or self.name

        name_or_value = [self.mode.title()]
        for socket in self.inputs:
            if socket.is_linked:
                name_or_value.append(socket.name.title())
            else:
                name_or_value.append(str(socket.default_value))
        return ' '.join(name_or_value)

    def draw_buttons_ext(self, context, layout):
        super().draw_buttons(context, layout)
        if self.inputs:
            layout.prop(self, "first_input", text="First input")
        if len(self.inputs) > 1:
            layout.prop(self, "second_input", text="Second input")



    def adjust_sockets(self):
        """Allow overrideing input types
        """
        func = self.compile()
        inputs_template = func.inputs_template.copy()

        if self.first_input != 'default' and inputs_template:
            inputs_template[0] = (self.first_input,) + inputs_template[0][1:]
        if self.second_input != 'default' and len(inputs_template) > 1:
            inputs_template[1] = (self.second_input,) + inputs_template[1][1:]

        self.adjust_inputs(inputs_template)
        self.adjust_outputs(func.outputs_template)


def register():

    for func in _node_funcs.values():
        bpy.utils.register_class(func.cls)
    for cls in _node_classes.values():
        bpy.utils.register_class(cls.node_cls)



def unregister():
    for func in _node_funcs.values():
        bpy.utils.unregister_class(func.cls)

    for cls in _node_classes.values():
        bpy.utils.unregister_class(cls.node_cls)
