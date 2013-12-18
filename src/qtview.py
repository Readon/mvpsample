'''
Created on 2013-12-16

@author: readon
@copyright: reserved
@note: View module for Qt backend
'''       
try:  
    from PySide.QtUiTools import QUiLoader as qloader
    from PySide.QtCore import QFile as qfile
except:
    raise Exception("Install Qt & PySide first.")

from mvp import View, BindOP
from PySide import QtGui as Qt

def qtconnect(widget, signalname):
    signal = getattr(widget, signalname)
    return signal.connect

class QtView(View, Qt.QWidget):
    __BIND_OP__ = {
        Qt.QLineEdit : lambda obj: BindOP(qtconnect(obj, "textChanged"), obj.text, obj.setText),
        Qt.QSpinBox : lambda obj: BindOP(qtconnect(obj, "valueChanged"), obj.value, obj.setValue),
    }
    def __init__(self, filename, custom_widget_types = [], extra_bind_op = {}): 
        View.__init__(self)
        Qt.QWidget.__init__(self)
        
        pf = qfile(filename)
        pf.open(qfile.ReadOnly)
        loader = qloader()
        for each in custom_widget_types:
            loader.registerCustomWidget(each)            
        self.top = loader.load(pf)
        
        setattr(self, "_" + self.top.objectName(), self.top)
        self.widgets[self.top] = self.top.objectName()
         
        self.__BIND_OP__.update(extra_bind_op)
        
    def get_object(self, name):
        return self.top.findChild(Qt.QWidget, name)
    
    def get_binding_op(self, widget):
        return self.__BIND_OP__[type(widget)](widget)
    
    def value_changed(self, *arglist):
        widget = self.sender()   
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
class MyView(QtView):
    def __init__(self, filename):
        super(MyView, self).__init__(filename)
        
class MyPresenter(Presenter):
    def __init__(self, model, view):
        super(MyPresenter, self).__init__(model, view)
        self.easy_bind("entry", "text")
        self.easy_bind("spinbutton", "weight")
#         
        self._model.text = "test"
#         self._model.weight = 80
    
from PySide import QtGui
import sys
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    obj = MyPresenter(MyModel(), MyView('main.ui'))
    obj._view.top.show()    
    sys.exit(app.exec_())
    