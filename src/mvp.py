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
        return self._convertion

    def disconnect(self, entry, func):
        return

    def _convertion(self, *args):
        return args[0]


class Binding():
    def __init__(self, view, widget_name, model, entry_name):
        self._view = view
        self._widget_name = widget_name
        self._model = model
        self._entry_name = entry_name

        value = getattr(model, entry_name)
        setattr(view, widget_name, value)

        if view.is_bindable(widget_name):
            self._view_convertion = view.connect(widget_name, self.update_model)
        if model.is_bindable(entry_name):
            self._model_convertion = model.connect(entry_name, self.update_view)
        return

    def unbind(self):
        if self._view.is_bindable(self._widget_name):
            self._view.disconnect(self._widget_name, self.update_model)
        if self._model.is_bindable(self._entry_name):
            self._model.disconnect(self._entry_name, self.update_view)
        return

    def update_view(self, event):
        value = self._model_convertion(event)
        if value != getattr(self._view, self._widget_name):
            setattr(self._view, self._widget_name, value)
        return

    def update_model(self, *args):
        value = self._view_convertion(*args)
        try:
            setattr(self._model, self._entry_name, value)
        except:
            setattr(self._view, self._widget_name, getattr(self._model, self._entry_name))
        return

    def set_view_convertion(self, function):
        self._view_convertion = function
    
    def set_model_convertion(self, function):
        self._model_convertion = function


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
    def convertion(*args):
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

