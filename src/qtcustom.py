'''
Created on 2013-12-16

@author: readon
@copyright: reserved
@note: CustomWidget example for mvp
'''
from PySide.QtGui import QLineEdit
class CustomLineEdit(QLineEdit):
    '''
    dummy custom line edit widget for test
    '''        
    def __init__(self, parent):
        QLineEdit.__init__(self, parent)
        print "this is a custom widget loading"