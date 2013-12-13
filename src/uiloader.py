#coding=UTF-8
'''
  Loader for View.
'''

class Loader(object):
    '''
    implement ui autoload and properties creation.
    '''
    def __init__(self, filename, custom_widget_types = []):
        '''
        Constructor define private virtual function _get_object
        '''
        self._get_object = None
        
    def __getattr__(self, name):   
        #internal attribute should be start with "_"
        obj = self._get_object(name[1:])
        setattr(self, "_" + name[1:], obj)
        return obj
    
    def _get_object(self, name):
        raise Exception("You have to implement _get_object function in Loader's subclass!")
        return
        
class GtkLoader(Loader):
    '''
        autoload glade file
    ''' 
    def __init__(self, filename):
        from gi.repository import Gtk
        self.builder = Gtk.Builder()
        self._get_object = self.builder.get_object
        self.builder.add_from_file(filename)
        self.builder.connect_signals(self)
    
class QtLoader(Loader):    
    '''
        autoload qt ui file
    '''
    def __init__(self, filename, custom_widget_types = []):        
        from PySide.QtUiTools import QUiLoader as qloader
        from PySide.QtCore import QFile as qfile
        
        pf = qfile(filename)
        pf.open(qfile.ReadOnly)
        loader = qloader()
        for each in custom_widget_types:
            loader.registerCustomWidget(each)
        self.builder = loader.load(pf)
        return
    
    def _get_object(self, name):
        if self.builder.objectName() == name:
            return self.builder
        from PySide.QtGui import QWidget
        return self.builder.findChild(QWidget, name)
    
# test for pyside
class MyQtView(QtLoader):
    def __init__(self, filename):
        QtLoader.__init__(self, filename)

# test for pygobject     
class MyGtkView(GtkLoader):
    def __init__(self, filename):
        GtkLoader.__init__(self, filename)
        
    def clicked(self, widget):
        print widget
 
from PySide import QtGui
import sys
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    qt = MyQtView('main.ui')
    print qt._pushButton.text()
    
    obj = MyGtkView('main.glade')
    print obj._button1.get_name()
