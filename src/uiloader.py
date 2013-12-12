#coding=UTF-8
'''
  Loader for View.
'''

class Loader(object):
    '''
    implement ui autoload and properties creation.
    '''
    def __init__(self, filename):
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
    def __init__(self, filename):        
        from PySide.QtUiTools import QUiLoader as qloader
        from PySide.QtCore import QFile as qfile
        
        pf = qfile(filename)
        pf.open(qfile.ReadOnly)
        self.builder = qloader().load(pf, self)
        return
    
    def _get_object(self, name):
        from PySide.QtGui import QWidget
        return self.builder.findChild(QWidget, name)
    
# test for pyside
from PySide.QtGui import QWidget
class MyQtWidget(QWidget, QtLoader):
    def __init__(self, filename):
        QWidget.__init__(self)
        QtLoader.__init__(self, filename)

# test for pygobject     
from gi.repository.Gtk import Widget
class MyGtkWidget(Widget, GtkLoader):
    def __init__(self, filename):
        Widget.__init__(self)
        GtkLoader.__init__(self, filename)
        
    def clicked(self, widget):
        print widget
 
from PySide import QtGui
import sys
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    qt = MyQtWidget('main.ui')
    print qt._pushButton.text()
    
    obj = MyGtkWidget('main.glade')
    print obj._button1.get_name()
