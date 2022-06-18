#searchresults screen



from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_resultsUI(object):
    def setupUi(self, resultsUI):
        resultsUI.setObjectName("resultsUI")
        resultsUI.resize(800, 600)
        self.label = QtWidgets.QLabel(resultsUI)
        self.label.setGeometry(QtCore.QRect(40, 30, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.frame = QtWidgets.QFrame(resultsUI)
        self.frame.setGeometry(QtCore.QRect(40, 70, 731, 441))
        self.frame.setStyleSheet("background-color: rgb(232, 230, 233);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.frame)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 731, 441))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.verticalLayoutWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 727, 437))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(resultsUI)
        QtCore.QMetaObject.connectSlotsByName(resultsUI)

    def retranslateUi(self, resultsUI):
        _translate = QtCore.QCoreApplication.translate
        resultsUI.setWindowTitle(_translate("resultsUI", "Dialog"))
        self.label.setText(_translate("resultsUI", "Search Results "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    resultsUI = QtWidgets.QDialog()
    ui = Ui_resultsUI()
    ui.setupUi(resultsUI)
    resultsUI.show()
    sys.exit(app.exec_())
