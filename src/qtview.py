"""
Created on 2013-12-16

@author: readon
@copyright: reserved
@note: View module for Qt backend
"""       
try:  
    from PySide.QtUiTools import QUiLoader as qloader
    from PySide.QtCore import QFile as qfile
except:
    raise Exception("Install Qt & PySide first.")

from mvp import View as Base, ViewOperations
from PySide import QtGui as Qt


class UiLoader(qloader):
    def __init__(self, custom_widget_types=[]):
        qloader.__init__(self)
        typedict = {}
        for each in custom_widget_types:
            typedict[each.__name__] = each
        self._custom_widgets = typedict

    def createWidget(self, clsname, parent=None, name=''):
        if clsname in self._custom_widgets:
            widget = self._custom_widgets[clsname](parent)
        else:
            widget = qloader.createWidget(self, clsname, parent, name)
        return widget


class QtOps(ViewOperations):
    @staticmethod
    def convertion(value):
        return value


class TextOps(QtOps):
    signal = "textChanged"
    get_func_name = "text"
    set_func_name = "setText"


class SpinOps(QtOps):
    signal = "valueChanged"
    get_func_name = "value"
    set_func_name = "setValue"


class View(Base):
    __BIND_OP__ = {
        Qt.QLineEdit: TextOps,
        Qt.QSpinBox: SpinOps,
    }

    def __init__(self, filename, custom_widget_types=[], extra_bind_op={}):
        super(View, self).__init__()
        
        pf = qfile(filename)
        pf.open(qfile.ReadOnly)                    
        loader = UiLoader(custom_widget_types)            
        self.top = loader.load(pf)
        
        self.update_binding_op(extra_bind_op)
        self.prepare_objects()

    def connect(self, entry, func):
        item = getattr(self, '_'+entry)
        ops = self._operations[entry]
        signal = getattr(item, ops.signal)
        signal.connect(func)
        return ops.convertion

    def disconnect(self, entry, func):
        item = getattr(self, '_'+entry)
        ops = self._operations[entry]
        signal = getattr(item, ops.signal)
        signal.disconnect(func)
        return

    def _traverse_tree(self, node):
        yield node
        for child in node.children():
            for each in self._traverse_tree(child):
                yield each

    def prepare_objects(self):
        for each in self._traverse_tree(self.top):
            name = each.objectName()
            if len(name) != 0:
                self.add_property(name, each)

    def get_object(self, name):
        return self.top.findChild(Qt.QWidget, name)

    
from mvp import Presenter, Binding
#from eventmodel import Model
from traitsmodel import Model
from traits.api import Range, String


class MyModel(Model):
    weight = Range(0.0, 90.0)
    text = String("hello")
    
    def __init__(self):
        super(MyModel, self).__init__()
        return


class MyView(View):
    def __init__(self, *arglist, **keywords):
        super(MyView, self).__init__(*arglist, **keywords)


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
    
from PySide import QtGui
from qtcustom import CustomLineEdit
import sys
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    custom_widgets = [CustomLineEdit]
    extra_ops = {CustomLineEdit: TextOps, Qt.QDoubleSpinBox: SpinOps}
    view = MyView('main.ui', custom_widgets, extra_ops)
    model = {'default': MyModel()}
    obj = MyPresenter(model, view)
    view.get_topview().show()
    #have to unbind before delete the presenter.
    obj.unbind_all()
    del obj

    #presenter could accept single model
    model = model['default']
    obj = SimplePresenter(model, view)

    #change model is possible when model has been changed.
    model1 = MyModel()
    model1.text = "NB"
    model1.weight = 88
    obj.change_model(model1)

    sys.exit(app.exec_())