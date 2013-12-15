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
        self._widgets = {}
        
    def __getattr__(self, name):   
        #internal attribute should be start with "_"
        obj = self._get_object(name[1:])
        setattr(self, "_" + name[1:], obj)
        print obj, name
        self._widgets[obj] = name[1:]
        return obj
    
    def _get_object(self, name):
        raise Exception("You have to implement _get_object function in Loader's subclass!")
        return    
        
try:    
    from gi.repository import Gtk
    from gi.repository import GObject
except:
    pass
class GtkLoader(Loader):
    '''
        autoload gtk glade file
    ''' 
    def __init__(self, filename, custom_widget_types = []):
        super(GtkLoader, self).__init__(filename)
        self._builder = Gtk.Builder()
        self._get_object = self._builder.get_object
        for each in custom_widget_types:
            GObject.type_register(each)
        self._builder.add_from_file(filename)
        self.top = [each for each in self._builder.get_objects() if each.get_parent() is None][0]
#         self.builder.connect_signals(self)
               
try:  
    from PySide.QtUiTools import QUiLoader as qloader
    from PySide.QtCore import QFile as qfile
except:
    pass
class QtLoader(Loader):    
    '''
        autoload qt ui file
    '''
    def __init__(self, filename, custom_widget_types = []): 
        super(QtLoader, self).__init__(filename)
        pf = qfile(filename)
        pf.open(qfile.ReadOnly)
        loader = qloader()
        for each in custom_widget_types:
            loader.registerCustomWidget(each)
        self.top = loader.load(pf)
        setattr(self, "_" + self.top.objectName(), self.top)
        self.widgets[self.top] = self.top.objectName() 
        return
     
    def _get_object(self, name):
        from PySide.QtGui import QWidget
        return self.top.findChild(QWidget, name)

        
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
#     app = QtGui.QApplication(sys.argv)
#     qt = MyQtView('main.ui')
#     print qt.top
    
    from gi.repository import Gtk
    win = Gtk.Window()    
    obj = MyGtkView('main.glade')
    win.add(obj.top)
    win.show_all()
    Gtk.main()
    print obj.top
