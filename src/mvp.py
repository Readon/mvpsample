'''
Created on 2013-12-14

@author: readon
@copyright: reserved
@note: Supervising Controller Model-View-Presenter Pattern
'''


class Model():
    '''
    Save & manage data.
    '''
    def __init__(self):
        return


class BindOP(object):
    def __init__(self, conn_func, get_func, set_func):
        self.connect = conn_func
        self.get_value = get_func
        self.set_value = set_func

import inspect


def mixin_to(cls):
    def f(fn):
        if inspect.isfunction(fn):
            setattr(cls, fn.func_name, fn)
        elif inspect.isclass(fn):
            for name in dir(fn):
                attr = getattr(fn, name)
                if inspect.ismethod(attr):
                    setattr(cls, name, attr.im_func)
        return fn
    return f


class View(object):
    '''
    Manage widgets in view, which could be auto loaded.
    '''
    __BIND_OP__ = {}
    def __init__(self):
        self.widgets = {}
        return
                
    def __getattr__(self, name):   
        #internal attribute should be start with "_"
        obj = self.get_object(name[1:])
        setattr(self, "_" + name[1:], obj)
        self.widgets[obj] = name[1:]
        
        opset = self.get_binding_op(obj)
        if opset is not None:
            setattr(obj, "_connect", opset.connect)
            setattr(obj, "_get_value", opset.get_value)
            setattr(obj, "_set_value", opset.set_value)
        return obj
    
    def get_object(self, name):
        raise Exception("You have to implement get_object function in Loader's subclass!")
        return 
    
    def get_topview(self):
        return self._view.top
            
    def set_presenter(self, presenter):
        self.presenter = presenter
        
    def change_value(self, widgetname, value):
        widget = getattr(self, "_" + widgetname)
        widget._set_value(value)
        
    def bind_signal(self, widgetname):
        widget = getattr(self, "_" + widgetname)
        widget._connect(self.value_changed)
        
    def value_changed(self, widget):
        raise Exception("You have to implement get_object function in Loader's subclass!")
            
    def get_binding_op(self, widget):
        widgettype = type(widget) 
        if widgettype in self.__BIND_OP__:
            return self.__BIND_OP__[widgettype](widget)
        return None
    
    def update_binding_op(self, opdict):
        self.__BIND_OP__.update(opdict)
        return self.__BIND_OP__


class Presenter(object):
    '''
    Bind parts of widgets and model entries specified.
    Implement complex business logic.  
    '''
    def __init__(self, model, view):
        self._model = model
        self._view = view
        view.set_presenter(self)
        self._model2view_map = {}
        self._view2model_map = {}
        
    def easy_bind(self, widgetname, model, entryname):
        if model not in self._model2view_map:
            self._model2view_map[model] = {}
        self._model2view_map[model][entryname] = widgetname
        self._view2model_map[widgetname] = (model, entryname)
        
        model.on_trait_change(self.model_changed, entryname)
        self._view.bind_signal(widgetname)
        
    def view_changed(self, widgetname, value):
        print "view", widgetname, value
        model, entryname = self._view2model_map[widgetname]
        setattr(model, entryname, value)
        
    def model_changed(self, model, entryname, value):
        print "model", self, model, entryname, value
        self._view.change_value(self._model2view_map[model][entryname], value)
        
