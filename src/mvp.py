'''
Created on 2013-12-14

@author: readon
@copyright: reserved
@note: Supervising Controller Model-View-Presenter Pattern
'''
from traits.api import HasTraits
class Model(HasTraits):
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
        
class View(object):
    '''
    Manage widgets in view, which could be auto loaded.
    '''
    def __init__(self):
        self.get_object = None
        self.widgets = {}
        return
                
    def __getattr__(self, name):   
        #internal attribute should be start with "_"
        print self.get_object
        obj = self.get_object(name[1:])
        setattr(self, "_" + name[1:], obj)
        self.widgets[obj] = name[1:]
        
        opset = self.get_binding_op(obj)
        setattr(obj, "_connect", opset.connect)
        setattr(obj, "_get_value", opset.get_value)
        setattr(obj, "_set_value", opset.set_value)
        return obj
    
    def get_object(self, name):
        raise Exception("You have to implement get_object function in Loader's subclass!")
        return 
            
    def set_presenter(self, presenter):
        self.presenter = presenter
        
    def change_value(self, widgetname, value):
        widget = getattr(self, "_" + widgetname)
        widget._set_value(value)
        
    def bind_signal(self, widgetname):
        widget = getattr(self, "_" + widgetname)
        widget._connect(self.value_changed)
        
    def value_changed(self, widget):
        self.presenter.view_changed(self.widgets[widget], widget._get_value())
        
    def get_binding_op(self, widget):
        raise Exception("You have to implement get_binding_op function in Loader's subclass!")
   
from eventize.events import Expect 
class Presenter(object):
    '''
    Bind parts of widgets and model entries specified.
    Implement complex business logic.  
    '''
    def __init__(self, model, view):
        self._model = model
        self._view = view
        view.set_presenter(self)
        self._model2view = {}
        self._view2model = {}
        
    def easy_bind(self, widgetname, modelname):
        self._model2view[modelname] = widgetname
        self._view2model[widgetname] = modelname
        
        self._model.on_trait_change(self.model_changed, modelname)
        self._view.bind_signal(widgetname)
 
    def conversion_bind(self, widgetname, modelname):
        self._model2view[modelname] = widgetname
        self._view2model[widgetname] = modelname
        
        self._model.on_trait_change(self.model_changed, modelname)
        self._view.bind_signal(widgetname)
        
    def view_changed(self, widgetname, value):
#         print "view", widgetname, value
        setattr(self._model, self._view2model[widgetname], value)
        
    def model_changed(self, widget, value):
#         print "model", widget, value
        self._view.change_value(self._model2view[widget], value)
        
