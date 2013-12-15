'''
Created on 2013-12-14

@author: readon
@copyright: reserved
@note: Supervising Controller Model-View-Presenter Pattern
'''
# from uiloader import GtkLoader, QtLoader
from eventize import ObservedAttribute

class Model(object):
    '''
    Save & manage data.
    '''
    def __init__(self):
        return
        
class View(object):
    '''
    Manage widgets in view, which could be auto loaded.
    '''
    def __init__(self):
        self._get_object = None
        self._widgets = {}
        return
                
    def __getattr__(self, name):   
        #internal attribute should be start with "_"
        obj = self._get_object(name[1:])
        setattr(self, "_" + name[1:], obj)
        self._widgets[obj] = name[1:]
        return obj
    
    def _get_object(self, name):
        raise Exception("You have to implement _get_object function in Loader's subclass!")
        return 
            
    def set_presenter(self, presenter):
        self._presenter = presenter
        
    def change_value(self, widgetname, value):
        widget = getattr(self, "_" + widgetname)
        widget._set_text(value)
        
    def bind_signal(self, widgetname):
        widget = getattr(self, "_" + widgetname)
        widget._connect("activate", self._value_changed)
        
    def _value_changed(self, widget):
        self._presenter.view_changed(self._widgets[widget], widget._get_text())
        
try:    
    from gi.repository import Gtk
    from gi.repository import GObject
except:
    pass  
class GtkView(View):
    def __init__(self, filename, custom_widget_types = []):
        View.__init__(self)
        
        self._builder = Gtk.Builder()
        self._get_object = self._builder.get_object
        for each in custom_widget_types:
            GObject.type_register(each)
        self._builder.add_from_file(filename)
        self.top = [each for each in self._builder.get_objects() if each.get_parent() is None][0]
        
try:  
    from PySide.QtUiTools import QUiLoader as qloader
    from PySide.QtCore import QFile as qfile
except:
    pass
class QtView(View):    
    def __init__(self, filename, custom_widget_types = []): 
        View.__init__(self)
        
        pf = qfile(filename)
        pf.open(qfile.ReadOnly)
        loader = qloader()
        for each in custom_widget_types:
            loader.registerCustomWidget(each)
        self.top = loader.load(pf)
        setattr(self, "_" + self.top.objectName(), self.top)
        self.widgets[self.top] = self.top.objectName() 
        
    def _get_object(self, name):
        from PySide.QtGui import QWidget
        return self.top.findChild(QWidget, name)
    
class Presenter(object):
    '''
    Bind parts of widgets and model entries specified.
    Implement complex business logic.  
    '''
    def __init__(self, model, view):
        self._model = model
        self._view = view
        view.set_presenter(self)
        self._model_view = {}
        self._view_model = {}
        
    def easy_bind(self, widgetname, modelname):
        self._model_view[modelname] = widgetname
        self._view_model[widgetname] = modelname
        
        entry = getattr(self._model, modelname)        
        entry.on_set += self.model_changed
        
        self._view.bind_signal(widgetname)
        
    def view_changed(self, widgetname, value):
        print "view", widgetname, value
        setattr(self._model, self._view_model[widgetname], value)
        
    def model_changed(self, event):
        print "model", event.name, event.value
        self._view.change_value(self._model_view[event.name], event.value)
        
class MyModel(Model):    
    weight = ObservedAttribute(90.0)
    text = ObservedAttribute("hello")
    
    def __init__(self):
        super(MyModel, self).__init__()
        return

# test for pygobject     
class MyGtkView(GtkView):
    def __init__(self, filename):
        super(MyGtkView, self).__init__(filename)
        
    def clicked(self, widget):
        print widget
        
class MyPresenter(Presenter):
    def __init__(self, model, view):
        super(MyPresenter, self).__init__(model, view)
        self.easy_bind("entry", "text")
        
        self._model.text = "test"
    
# from PySide import QtGui
from gi.repository import Gtk
import sys
if __name__ == '__main__':
#     app = QtGui.QApplication(sys.argv)
#     qt = MyQtView('main.ui')
#     print qt.top
    
    win = Gtk.Window()
    obj = MyPresenter(MyModel(), MyGtkView('main.glade'))
    win.add(obj._view.top)
    win.show_all()    
    win.connect("delete-event", Gtk.main_quit)
    Gtk.main()
    print obj._view.top