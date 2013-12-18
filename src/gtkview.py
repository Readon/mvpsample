'''
Created on 2013-12-16

@author: readon
@copyright: reserved
@note: View module for Gtk backend
'''
try:        
    from gi.repository import Gtk
    from gi.repository import GObject
except:    
    raise Exception("Install Gtk & PyGObject first.")
from mvp import View, BindOP
from functools import partial

class GtkView(View):
    __BIND_OP__ = {
        Gtk.Entry : lambda obj: BindOP(partial(obj.connect, "activate"), obj.get_text, obj.set_text),
        Gtk.SpinButton : lambda obj: BindOP(partial(obj.connect, "output"), obj.get_value_as_int, obj.set_value),
    }
    def __init__(self, filename, custom_widget_types = [], extra_bind_op = {}):
        View.__init__(self)
        
        self.builder = Gtk.Builder()
        self.get_object = self.builder.get_object
        for each in custom_widget_types:
            GObject.type_register(each)
        self.builder.add_from_file(filename)
        self.top = [each for each in self.builder.get_objects() if each.get_parent() is None][0]
                
        self.__BIND_OP__.update(extra_bind_op)
        
    def get_binding_op(self, widget):
        return self.__BIND_OP__[type(widget)](widget) 
    
    def value_changed(self, widget, *arglist):        
        self.presenter.view_changed(self.widgets[widget], widget._get_value()) 

from mvp import Model, Presenter    
from traits.api import Float, String
class MyModel(Model):    
    weight = Float(90.0)
    text = String("hello")
    
    def __init__(self):
        super(MyModel, self).__init__()
        return

# test for pygobject     
class MyView(GtkView):
    def __init__(self, *arglist, **keywords):
        super(MyView, self).__init__(*arglist, **keywords)
        adjustment = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
        self._spinbutton.set_adjustment(adjustment)
        
class MyPresenter(Presenter):
    def __init__(self, model, view):
        super(MyPresenter, self).__init__(model, view)
        self.easy_bind("entry", "text")
        self.easy_bind("spinbutton", "weight")
        
        self._model.text = "test"
        self._model.weight = 80
    
from gtkcustom import CustomEntry
if __name__ == '__main__':    
    win = Gtk.Window()
    
    custom_widget_types = [CustomEntry]
    extra_bind_op={CustomEntry : lambda obj: BindOP(partial(obj.connect, "activate"), obj.get_text, obj.set_text)}
    obj = MyPresenter(MyModel(), MyView('main.glade', custom_widget_types, extra_bind_op))
        
    win.add(obj._view.top)
    win.show_all()    
    win.connect("delete-event", Gtk.main_quit)
    
    Gtk.main()