"""
Created on 2013-12-16

@author: readon
@copyright: reserved
@note: CustomWidget example for mvp
"""
from gi.repository import Gtk
from gi.repository import GObject


class CustomEntry(Gtk.Entry):
    """
    custom widget inherit from gtkentry.
    """
    def __init__(self):
        Gtk.Entry.__init__(self)
        print "this is a custom widget loading"
        
GObject.type_register(CustomEntry)
        