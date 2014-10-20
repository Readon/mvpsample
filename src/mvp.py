"""
Created on 2013-12-14

@author: readon
@copyright: reserved
@note: Supervising Controller Model-View-Presenter Pattern
"""
from functools import partial


class Bindable(object):
    def is_bindable(self, entry):
        return False

    def connect(self, entry, func):
        return self._conversion

    def disconnect(self, entry, func):
        return

    def _conversion(self, *args):
        return args[0]


class UniDirBinding(object):
    def __init__(self, container, name, target_container, target_name, update_args=0, retreatable=False, check=False):
        update_functions = [self._update, self._update_1, self._update_2, self._update_3, self._update_4]

        #self.get_source = partial(getattr, container, name)
        self.set_source = partial(setattr, container, name)
        self.get_target = partial(getattr, target_container, target_name)
        self.set_target = partial(setattr, target_container, target_name)

        self.update = update_functions[update_args]
        self.unbind = partial(container.disconnect, name, self.update)
        self.retreatable = retreatable
        self.check_change = check

        self._conversion = container.connect(name, self.update)

    def _real_update(self, value):
        if self.check_change and value == self.get_target():
            return

        try:
            self.set_target(value)
        except:
            if self.retreatable:
                value = self.get_target()
                self.set_source(value)

    def _update(self, *args):
        value = self._conversion(*args)
        self._real_update(value)

    def _update_1(self, new):
        value = self._conversion(new)
        self._real_update(value)

    def _update_2(self, name, new):
        value = self._conversion(name, new)
        self._real_update(value)

    def _update_3(self, container, name, new):
        value = self._conversion(container, name, new)
        self._real_update(value)

    def _update_4(self, container, name, old, new):
        value = self._conversion(container, name, old, new)
        self._real_update(value)

    def set_conversion(self, function):
        self._conversion = function


class Binding(object):
    def __init__(self, view, widget_name, model, entry_name):
        value = getattr(model, entry_name)
        setattr(view, widget_name, value)

        self._model_bind = UniDirBinding(model, entry_name, view, widget_name, update_args=1, check=True)
        self._view_bind = UniDirBinding(view, widget_name, model, entry_name, retreatable=True)
        return

    def unbind(self):
        self._view_bind.unbind()
        self._model_bind.unbind()
        return

    def set_view_conversion(self, function):
        self._view_bind.set_conversion(function)
    
    def set_model_conversion(self, function):
        self._model_bind.set_conversion(function)


class Model(Bindable):
    """
    Save & manage data.
    """
    def __init__(self):
        return


class ViewOperations(object):
    signal = ""
    get_func_name = ""
    set_func_name = ""

    @staticmethod
    def conversion(*args):
        return args

    @classmethod
    def get(cls, name, container):
        instance = getattr(container, name)
        return getattr(instance, cls.get_func_name)()

    @classmethod
    def set(cls, name, container, value):
        instance = getattr(container, name)
        return getattr(instance, cls.set_func_name)(value)


class View(Bindable):
    """
    Manage widgets in view, which could be auto loaded.
    """
    __BIND_OP__ = {}
    def __init__(self):
        self._operations = {}
        return

    def is_bindable(self, entry):
        ops = self._operations[entry]
        return ops is not None

    def prepare_objects(self):
        raise Exception("You have to implement prepare_object function in Loader's subclass!")
        return
    
    def get_object(self, name):
        raise Exception("You have to implement get_object function in Loader's subclass!")
        return None
    
    def get_topview(self):
        return self.top

    def add_property(self, name, instance):
        inst_name = "_"+name
        setattr(self, inst_name, instance)
        ops = self.get_binding_ops(instance)
        self._operations[name] = ops

        if ops is not None and not hasattr(self.__class__, name):
            fget = partial(ops.get, inst_name)
            fset = partial(ops.set, inst_name)
            setattr(self.__class__, name, property(fget, fset))

    def get_binding_ops(self, widget):
        widget_type = type(widget)
        try:
            return self.__BIND_OP__[widget_type]
        except:
            return None
    
    def update_binding_op(self, opdict):
        self.__BIND_OP__.update(opdict)
        return self.__BIND_OP__


class Presenter(object):
    """
    Bind parts of widgets and model entries specified.
    Implement complex business logic.  
    """
    def __init__(self, model, view):
        self._model = model
        self._view = view
        self._bindings = []
        self.bind_all()

    def bind_all(self):
        pass

    def unbind_all(self):
        for each in self._bindings:
            each.unbind()
        self._bindings = []

    def change_model(self, model):
        self.unbind_all()
        self._model = model
        self.bind_all()

if __name__ == '__main__':
    pass

