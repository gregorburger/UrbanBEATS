# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ubeatsprojectinfogui.ui'
#
# Created: Mon Apr 16 00:43:41 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_UBeatsProjectInfoDialog(object):
    def setupUi(self, UBeatsProjectInfoDialog):
        UBeatsProjectInfoDialog.setObjectName(_fromUtf8("UBeatsProjectInfoDialog"))
        UBeatsProjectInfoDialog.resize(402, 491)
        self.verticalLayout = QtGui.QVBoxLayout(UBeatsProjectInfoDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.title_frame = QtGui.QFrame(UBeatsProjectInfoDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title_frame.sizePolicy().hasHeightForWidth())
        self.title_frame.setSizePolicy(sizePolicy)
        self.title_frame.setMinimumSize(QtCore.QSize(0, 50))
        self.title_frame.setMaximumSize(QtCore.QSize(16777215, 50))
        self.title_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.title_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.title_frame.setObjectName(_fromUtf8("title_frame"))
        self.dbtitle = QtGui.QLabel(self.title_frame)
        self.dbtitle.setGeometry(QtCore.QRect(50, 5, 441, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.dbtitle.setFont(font)
        self.dbtitle.setObjectName(_fromUtf8("dbtitle"))
        self.dbsubtitle = QtGui.QLabel(self.title_frame)
        self.dbsubtitle.setGeometry(QtCore.QRect(50, 25, 561, 16))
        self.dbsubtitle.setObjectName(_fromUtf8("dbsubtitle"))
        self.bpmlogo = QtGui.QLabel(self.title_frame)
        self.bpmlogo.setGeometry(QtCore.QRect(0, 0, 50, 50))
        self.bpmlogo.setMaximumSize(QtCore.QSize(50, 50))
        self.bpmlogo.setText(_fromUtf8(""))
        self.bpmlogo.setPixmap(QtGui.QPixmap(_fromUtf8("../../../../../../D4W-logoBPM.png")))
        self.bpmlogo.setObjectName(_fromUtf8("bpmlogo"))
        self.line = QtGui.QFrame(self.title_frame)
        self.line.setGeometry(QtCore.QRect(50, 40, 573, 20))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setMinimumSize(QtCore.QSize(573, 0))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.title_frame)
        self.widget = QtGui.QWidget(UBeatsProjectInfoDialog)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.scrollArea = QtGui.QScrollArea(self.widget)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, -267, 347, 628))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.general_widget = QtGui.QWidget(self.scrollAreaWidgetContents)
        self.general_widget.setMinimumSize(QtCore.QSize(0, 610))
        self.general_widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.general_widget.setObjectName(_fromUtf8("general_widget"))
        self.name_lbl = QtGui.QLabel(self.general_widget)
        self.name_lbl.setGeometry(QtCore.QRect(20, 34, 81, 16))
        self.name_lbl.setObjectName(_fromUtf8("name_lbl"))
        self.name_box = QtGui.QLineEdit(self.general_widget)
        self.name_box.setGeometry(QtCore.QRect(120, 30, 201, 20))
        self.name_box.setObjectName(_fromUtf8("name_box"))
        self.date_lbl = QtGui.QLabel(self.general_widget)
        self.date_lbl.setGeometry(QtCore.QRect(20, 64, 101, 16))
        self.date_lbl.setObjectName(_fromUtf8("date_lbl"))
        self.date_spin = QtGui.QDateEdit(self.general_widget)
        self.date_spin.setGeometry(QtCore.QRect(120, 60, 110, 22))
        self.date_spin.setCalendarPopup(True)
        self.date_spin.setObjectName(_fromUtf8("date_spin"))
        self.modellername_lbl = QtGui.QLabel(self.general_widget)
        self.modellername_lbl.setGeometry(QtCore.QRect(20, 218, 101, 16))
        self.modellername_lbl.setObjectName(_fromUtf8("modellername_lbl"))
        self.city_box = QtGui.QLineEdit(self.general_widget)
        self.city_box.setGeometry(QtCore.QRect(120, 90, 201, 20))
        self.city_box.setObjectName(_fromUtf8("city_box"))
        self.affiliation_lbl = QtGui.QLabel(self.general_widget)
        self.affiliation_lbl.setGeometry(QtCore.QRect(20, 248, 101, 16))
        self.affiliation_lbl.setObjectName(_fromUtf8("affiliation_lbl"))
        self.state_box = QtGui.QLineEdit(self.general_widget)
        self.state_box.setGeometry(QtCore.QRect(120, 120, 81, 20))
        self.state_box.setObjectName(_fromUtf8("state_box"))
        self.othermodellers_lbl = QtGui.QLabel(self.general_widget)
        self.othermodellers_lbl.setGeometry(QtCore.QRect(20, 278, 271, 16))
        self.othermodellers_lbl.setObjectName(_fromUtf8("othermodellers_lbl"))
        self.country_box = QtGui.QLineEdit(self.general_widget)
        self.country_box.setGeometry(QtCore.QRect(120, 150, 121, 20))
        self.country_box.setObjectName(_fromUtf8("country_box"))
        self.aboutproject_lbl = QtGui.QLabel(self.general_widget)
        self.aboutproject_lbl.setGeometry(QtCore.QRect(10, 10, 191, 16))
        self.aboutproject_lbl.setObjectName(_fromUtf8("aboutproject_lbl"))
        self.aboutmodeller_lbl = QtGui.QLabel(self.general_widget)
        self.aboutmodeller_lbl.setGeometry(QtCore.QRect(10, 194, 131, 16))
        self.aboutmodeller_lbl.setObjectName(_fromUtf8("aboutmodeller_lbl"))
        self.city_lbl = QtGui.QLabel(self.general_widget)
        self.city_lbl.setGeometry(QtCore.QRect(20, 94, 101, 16))
        self.city_lbl.setObjectName(_fromUtf8("city_lbl"))
        self.synopsis_lbl = QtGui.QLabel(self.general_widget)
        self.synopsis_lbl.setGeometry(QtCore.QRect(10, 340, 131, 16))
        self.synopsis_lbl.setObjectName(_fromUtf8("synopsis_lbl"))
        self.modellername_box = QtGui.QLineEdit(self.general_widget)
        self.modellername_box.setGeometry(QtCore.QRect(120, 220, 201, 20))
        self.modellername_box.setObjectName(_fromUtf8("modellername_box"))
        self.affiliation_box = QtGui.QLineEdit(self.general_widget)
        self.affiliation_box.setGeometry(QtCore.QRect(120, 250, 201, 20))
        self.affiliation_box.setObjectName(_fromUtf8("affiliation_box"))
        self.state_lbl = QtGui.QLabel(self.general_widget)
        self.state_lbl.setGeometry(QtCore.QRect(20, 120, 101, 20))
        self.state_lbl.setObjectName(_fromUtf8("state_lbl"))
        self.othermodellers_box = QtGui.QLineEdit(self.general_widget)
        self.othermodellers_box.setGeometry(QtCore.QRect(40, 300, 281, 20))
        self.othermodellers_box.setObjectName(_fromUtf8("othermodellers_box"))
        self.country_lbl = QtGui.QLabel(self.general_widget)
        self.country_lbl.setGeometry(QtCore.QRect(20, 150, 101, 20))
        self.country_lbl.setObjectName(_fromUtf8("country_lbl"))
        self.synopsis_box = QtGui.QPlainTextEdit(self.general_widget)
        self.synopsis_box.setGeometry(QtCore.QRect(10, 380, 311, 211))
        self.synopsis_box.setObjectName(_fromUtf8("synopsis_box"))
        self.synopsis_descr_lbl = QtGui.QLabel(self.general_widget)
        self.synopsis_descr_lbl.setGeometry(QtCore.QRect(20, 360, 291, 16))
        self.synopsis_descr_lbl.setObjectName(_fromUtf8("synopsis_descr_lbl"))
        self.verticalLayout_2.addWidget(self.general_widget)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scrollArea)
        self.verticalLayout.addWidget(self.widget)
        self.widget_4 = QtGui.QWidget(UBeatsProjectInfoDialog)
        self.widget_4.setMinimumSize(QtCore.QSize(0, 38))
        self.widget_4.setMaximumSize(QtCore.QSize(16777215, 38))
        self.widget_4.setObjectName(_fromUtf8("widget_4"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.widget_4)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.remarks = QtGui.QLabel(self.widget_4)
        self.remarks.setObjectName(_fromUtf8("remarks"))
        self.horizontalLayout_2.addWidget(self.remarks)
        self.remarks2 = QtGui.QLabel(self.widget_4)
        self.remarks2.setObjectName(_fromUtf8("remarks2"))
        self.horizontalLayout_2.addWidget(self.remarks2)
        self.buttonBox = QtGui.QDialogButtonBox(self.widget_4)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout_2.addWidget(self.buttonBox)
        self.verticalLayout.addWidget(self.widget_4)

        self.retranslateUi(UBeatsProjectInfoDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), UBeatsProjectInfoDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), UBeatsProjectInfoDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(UBeatsProjectInfoDialog)

    def retranslateUi(self, UBeatsProjectInfoDialog):
        UBeatsProjectInfoDialog.setWindowTitle(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.dbtitle.setText(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "New Project Setup", None, QtGui.QApplication.UnicodeUTF8))
        self.dbsubtitle.setText(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "Enter General Details about the Project and Simulations involved", None, QtGui.QApplication.UnicodeUTF8))
        self.name_lbl.setWhatsThis(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "Width of the square cell in the city grid in metres", None, QtGui.QApplication.UnicodeUTF8))
        self.name_lbl.setText(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Project Name</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.date_lbl.setWhatsThis(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "Width of the square cell in the city grid in metres", None, QtGui.QApplication.UnicodeUTF8))
        self.date_lbl.setText(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Simulation Date</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.modellername_lbl.setWhatsThis(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "Width of the square cell in the city grid in metres", None, QtGui.QApplication.UnicodeUTF8))
        self.modellername_lbl.setText(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Key Modeller</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.affiliation_lbl.setWhatsThis(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "Width of the square cell in the city grid in metres", None, QtGui.QApplication.UnicodeUTF8))
        self.affiliation_lbl.setText(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Affiliation</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.othermodellers_lbl.setWhatsThis(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "Width of the square cell in the city grid in metres", None, QtGui.QApplication.UnicodeUTF8))
        self.othermodellers_lbl.setText(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Other Persons (separate names with commas)</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.aboutproject_lbl.setWhatsThis(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "Width of the square cell in the city grid in metres", None, QtGui.QApplication.UnicodeUTF8))
        self.aboutproject_lbl.setText(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">About the Project</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.aboutmodeller_lbl.setWhatsThis(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "Width of the square cell in the city grid in metres", None, QtGui.QApplication.UnicodeUTF8))
        self.aboutmodeller_lbl.setText(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">About the Modellers</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.city_lbl.setWhatsThis(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "Width of the square cell in the city grid in metres", None, QtGui.QApplication.UnicodeUTF8))
        self.city_lbl.setText(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Region/City Name</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.synopsis_lbl.setWhatsThis(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "Width of the square cell in the city grid in metres", None, QtGui.QApplication.UnicodeUTF8))
        self.synopsis_lbl.setText(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Project Synopsis</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.state_lbl.setWhatsThis(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "Width of the square cell in the city grid in metres", None, QtGui.QApplication.UnicodeUTF8))
        self.state_lbl.setText(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">State</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.country_lbl.setWhatsThis(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "Width of the square cell in the city grid in metres", None, QtGui.QApplication.UnicodeUTF8))
        self.country_lbl.setText(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Country</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.synopsis_box.setPlainText(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "none", None, QtGui.QApplication.UnicodeUTF8))
        self.synopsis_descr_lbl.setWhatsThis(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "Width of the square cell in the city grid in metres", None, QtGui.QApplication.UnicodeUTF8))
        self.synopsis_descr_lbl.setText(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Provide a description of the key aspects of this project.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.remarks.setText(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-style:italic;\">UrbanBEATS.projectinfo</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.remarks2.setText(QtGui.QApplication.translate("UBeatsProjectInfoDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-style:italic;\">v0.80</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

