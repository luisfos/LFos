from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import QtCore

import logic
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Interface(QtWidgets.QWidget):
    def __init__(self):
        super(Interface, self).__init__()
        self.setProperty("houdiniStyle", True)
        print "fuck"
        logger.info("initialized interface class")

    def buildGUI(self):
        self.okButton = QtWidgets.QPushButton()



