# This Python file uses the following encoding: utf-8
import os
import sys
from PyQt5 import QtWidgets
from PySide2.QtWidgets import QApplication
from PySide2.QtQuick import QQuickView
from PySide2.QtCore import QStringListModel, Qt, QUrl
from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine

# from style_rc import *

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    view = QQuickView()
    view.setResizeMode(QQuickView.SizeRootObjectToView)
    qmlFile = os.path.join(os.path.dirname(__file__), "view.qml")
    view.setSource(QUrl.fromLocalFile(os.path.abspath(qmlFile)))

    # Show the window
    if view.status() == QQuickView.Error:
        sys.exit(-1)
    view.showMaximized()
#    view.show()
    # execute main loop and cleanup
    app.exec_()
    del view
