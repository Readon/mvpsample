"""
Created on 2013-12-16

@author: readon
@copyright: reserved
@note: View module for Gtk backend
"""
try:        
    from gi.repository import Gtk
    from gi.repository import GObject
except:    
    raise Exception("Install Gtk & PyGObject first.")
from mvp import View as Base, ViewOperations


class GtkOps(ViewOperations):
    @staticmethod
    def convertion(instance, get_func_name):
        return getattr(instance, get_func_name)()


class TextOps(GtkOps):
    signal = "changed"
    get_func_name = "get_text"
    set_func_name = "set_text"


class SpinOps(GtkOps):
    signal = "output"
    get_func_name = "get_value"
    set_func_name = "set_value"


class View(Base):
    __BIND_OP__ = {
        Gtk.Entry: TextOps,
        Gtk.SpinButton: SpinOps,
    }

    def __init__(self, filename, custom_widget_types=[], extra_bind_op={}):
        super(View, self).__init__()

        self.builder = Gtk.Builder()
        self.get_object = self.builder.get_object
        for each in custom_widget_types:
            GObject.type_register(each)
        self.builder.add_from_file(filename)
        self.top = [each for each in self.builder.get_objects() if each.get_parent() is None][0]
                
        self.update_binding_op(extra_bind_op)
        self.prepare_objects()
        self.signal_handlers = {}

    def connect(self, entry, func):
        item = getattr(self, '_'+entry)
        ops = self._operations[entry]
        self.signal_handlers[entry] = item.connect(ops.signal, func, ops.get_func_name)
        return ops.convertion

    def disconnect(self, entry, func):
        item = getattr(self, '_'+entry)
        handle_id = self.signal_handlers[entry]
        item.disconnect(handle_id)
        return

    def prepare_objects(self):
        for each in self.builder.get_objects():
            name = Gtk.Buildable.get_name(each)
            if len(name) != 0:
                self.add_property(name, each)

from mvp import Presenter, Binding
#from traitsmodel import Model
#from traits.api import String, Float, Range
from eventmodel import Model, Range
from eventize import Attribute


class MyModel(Model):
    #weight = Range(0, 90)
    #text = String("hello")
    weight = Range(0, 90)
    text = Attribute("hello")
    
    def __init__(self):
        super(MyModel, self).__init__()
        return


# test for pygobject     
class MyView(View):
    def __init__(self, *arglist, **keywords):
        super(MyView, self).__init__(*arglist, **keywords)
        adjustment = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
        self._spinbutton.set_adjustment(adjustment)
        adjustment = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
        self._dspinbtn.set_adjustment(adjustment)


class MyPresenter(Presenter):
    def __init__(self, model, view):
        super(MyPresenter, self).__init__(model, view)

        self._model['default'].text = "test"
        self._model['default'].weight = 80

    def bind_all(self):
        self._bindings += [Binding(self._view, "entry", self._model['default'], "text")]
        self._bindings += [Binding(self._view, "entry_copy", self._model['default'], "text")]
        self._bindings += [Binding(self._view, "spinbutton", self._model['default'], "weight")]
        self._bindings += [Binding(self._view, "dspinbtn", self._model['default'], "weight")]


class SimplePresenter(Presenter):
    def bind_all(self):
        self._bindings += [Binding(self._view, "entry", self._model, "text")]
        self._bindings += [Binding(self._view, "entry_copy", self._model, "text")]
        self._bindings += [Binding(self._view, "spinbutton", self._model, "weight")]
        self._bindings += [Binding(self._view, "dspinbtn", self._model, "weight")]

from gtkcustom import CustomEntry
if __name__ == '__main__':
    win = Gtk.Window()

    custom_widgets = [CustomEntry]
    extra_ops = {CustomEntry: TextOps}
    view = MyView('main.glade', custom_widgets, extra_ops)
    model = {'default': MyModel()}
    obj = MyPresenter(model, view)

    win.add(view.get_topview())
    win.show_all()
    win.connect("delete-event", Gtk.main_quit)

    #have to unbind before delete the presenter.
    obj.unbind_all()
    del obj

    #presenter could accept single model
    model = model['default']
    obj = SimplePresenter(model, view)

    #change model is possible when model has been changed.
    model1 = MyModel()
    model1.text = "NB"
    setattr(model1, "weight", 88)
    obj.change_model(model1)

    Gtk.main()