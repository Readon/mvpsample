"""
Created on 2013-12-14

@author: readon
@copyright: reserved
@note: Supervising Controller Model-View-Presenter Pattern
"""


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

        value = getattr(self._model, self._entry_name)
        setattr(self._view, self._widget_name, value)
        value = getattr(self._view, self._widget_name)
        setattr(self._model, self._entry_name, value)

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
        setattr(self._view, self._widget_name, value)
        return

    def update_model(self, *args):
        value = self._view_convertion(*args)
        setattr(self._model, self._entry_name, value)
        return


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
        raise Exception("You have to implement get_object function in Loader's subclass!")
        return []
    
    def get_object(self, name):
        raise Exception("You have to implement get_object function in Loader's subclass!")
        return None
    
    def get_topview(self):
        return self.top

    def add_property(self, name, instance):
        setattr(self, "_"+name, instance)
        ops = self.get_binding_ops(instance)
        self._operations[name] = ops

        if ops is not None:
            fget = lambda self: getattr(instance, ops.get_func_name)()
            fset = lambda self, value: getattr(instance, ops.set_func_name)(value)
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

    def unbind_all(self):
        for each in self._bindings:
            each.unbind()
        self._bindings = []

if __name__ == '__main__':
    pass

