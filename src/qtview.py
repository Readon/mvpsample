'''
Created on 2013-12-16

@author: readon
@copyright: reserved
@note: View module for Qt backend
'''       
try:  
    from mvp import View, BindOP
    from PySide.QtUiTools import QUiLoader as qloader
    from PySide.QtCore import QFile as qfile
except:
    raise Exception("Install Qt & PySide first.")


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
        
    def __get_object(self, name):
        from PySide.QtGui import QWidget
        return self.top.findChild(QWidget, name)
    
from mvp import Model, Presenter    
from eventize import ObservedAttribute
class MyModel(Model):    
    weight = ObservedAttribute(90.0)
    text = ObservedAttribute("hello")
    
    def __init__(self):
        super(MyModel, self).__init__()
        return

# test for pygobject     
class MyQtView(QtView):
    def __init__(self, filename):
        super(MyQtView, self).__init__(filename)
        
    def clicked(self, widget):
        print widget
        
class MyPresenter(Presenter):
    def __init__(self, model, view):
        super(MyPresenter, self).__init__(model, view)
        self.easy_bind("entry", "text")
        
        self._model.text = "test"
    
from PySide import QtGui
import sys
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    qt = MyQtView('main.ui')
    print qt.top