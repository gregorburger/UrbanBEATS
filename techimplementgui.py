# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'techimplementgui.ui'
#
# Created: Thu Jul 19 10:33:52 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_TechImplement_Dialog(object):
    def setupUi(self, TechImplement_Dialog):
        TechImplement_Dialog.setObjectName(_fromUtf8("TechImplement_Dialog"))
        TechImplement_Dialog.resize(771, 598)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(TechImplement_Dialog.sizePolicy().hasHeightForWidth())
        TechImplement_Dialog.setSizePolicy(sizePolicy)
        TechImplement_Dialog.setWindowTitle(QtGui.QApplication.translate("TechImplement_Dialog", "Technology Implementation", None, QtGui.QApplication.UnicodeUTF8))
        self.verticalLayout = QtGui.QVBoxLayout(TechImplement_Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.techimplement_title = QtGui.QFrame(TechImplement_Dialog)
        self.techimplement_title.setMinimumSize(QtCore.QSize(0, 50))
        self.techimplement_title.setMaximumSize(QtCore.QSize(16777215, 50))
        self.techimplement_title.setFrameShape(QtGui.QFrame.StyledPanel)
        self.techimplement_title.setFrameShadow(QtGui.QFrame.Raised)
        self.techimplement_title.setObjectName(_fromUtf8("techimplement_title"))
        self.tech_heading = QtGui.QLabel(self.techimplement_title)
        self.tech_heading.setGeometry(QtCore.QRect(50, 5, 451, 21))
        self.tech_heading.setText(QtGui.QApplication.translate("TechImplement_Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600;\">Decentralised Technology Implementation</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.tech_heading.setObjectName(_fromUtf8("tech_heading"))
        self.tech_subheading = QtGui.QLabel(self.techimplement_title)
        self.tech_subheading.setGeometry(QtCore.QRect(50, 25, 531, 16))
        self.tech_subheading.setText(QtGui.QApplication.translate("TechImplement_Dialog", "Set Rules for implementing technology configurations found from the input masterplan", None, QtGui.QApplication.UnicodeUTF8))
        self.tech_subheading.setObjectName(_fromUtf8("tech_subheading"))
        self.label = QtGui.QLabel(self.techimplement_title)
        self.label.setGeometry(QtCore.QRect(0, 0, 50, 50))
        self.label.setMinimumSize(QtCore.QSize(50, 50))
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8("../../../../../../D4W-logoBPM.png")))
        self.label.setObjectName(_fromUtf8("label"))
        self.line = QtGui.QFrame(self.techimplement_title)
        self.line.setGeometry(QtCore.QRect(50, 49, 703, 3))
        self.line.setMinimumSize(QtCore.QSize(703, 0))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.techimplement_title)
        self.techimplement_input = QtGui.QTabWidget(TechImplement_Dialog)
        self.techimplement_input.setObjectName(_fromUtf8("techimplement_input"))
        self.DesignCriteria = QtGui.QWidget()
        self.DesignCriteria.setObjectName(_fromUtf8("DesignCriteria"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.DesignCriteria)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.techimplement_widget = QtGui.QWidget(self.DesignCriteria)
        self.techimplement_widget.setObjectName(_fromUtf8("techimplement_widget"))
        self.gridLayout_22 = QtGui.QGridLayout(self.techimplement_widget)
        self.gridLayout_22.setMargin(0)
        self.gridLayout_22.setObjectName(_fromUtf8("gridLayout_22"))
        self.techimplement_inputs = QtGui.QScrollArea(self.techimplement_widget)
        self.techimplement_inputs.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.techimplement_inputs.setWidgetResizable(True)
        self.techimplement_inputs.setObjectName(_fromUtf8("techimplement_inputs"))
        self.design_crit_inputs_widget = QtGui.QWidget()
        self.design_crit_inputs_widget.setGeometry(QtCore.QRect(0, 0, 465, 468))
        self.design_crit_inputs_widget.setObjectName(_fromUtf8("design_crit_inputs_widget"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.design_crit_inputs_widget)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.driver_title = QtGui.QLabel(self.design_crit_inputs_widget)
        self.driver_title.setMinimumSize(QtCore.QSize(0, 16))
        self.driver_title.setMaximumSize(QtCore.QSize(16777215, 16))
        self.driver_title.setWhatsThis(QtGui.QApplication.translate("TechImplement_Dialog", "Select what design goals to consider and what priority they take over each other. Highest priority (1) and Lowest priority (3) influence technology\'s chance of being implemented. Note that equal priority can be set as well, in which case no one design rationale is more important than the other.", None, QtGui.QApplication.UnicodeUTF8))
        self.driver_title.setText(QtGui.QApplication.translate("TechImplement_Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Select Drivers for Implementation</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.driver_title.setObjectName(_fromUtf8("driver_title"))
        self.verticalLayout_5.addWidget(self.driver_title)
        self.driver_widget = QtGui.QWidget(self.design_crit_inputs_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.driver_widget.sizePolicy().hasHeightForWidth())
        self.driver_widget.setSizePolicy(sizePolicy)
        self.driver_widget.setMinimumSize(QtCore.QSize(0, 100))
        self.driver_widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.driver_widget.setObjectName(_fromUtf8("driver_widget"))
        self.driver_people_check = QtGui.QCheckBox(self.driver_widget)
        self.driver_people_check.setEnabled(False)
        self.driver_people_check.setGeometry(QtCore.QRect(20, 10, 131, 17))
        self.driver_people_check.setText(QtGui.QApplication.translate("TechImplement_Dialog", "People Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.driver_people_check.setObjectName(_fromUtf8("driver_people_check"))
        self.driver_legal_check = QtGui.QCheckBox(self.driver_widget)
        self.driver_legal_check.setEnabled(False)
        self.driver_legal_check.setGeometry(QtCore.QRect(20, 40, 141, 17))
        self.driver_legal_check.setText(QtGui.QApplication.translate("TechImplement_Dialog", "Legal Provisions", None, QtGui.QApplication.UnicodeUTF8))
        self.driver_legal_check.setObjectName(_fromUtf8("driver_legal_check"))
        self.driver_establish_check = QtGui.QCheckBox(self.driver_widget)
        self.driver_establish_check.setEnabled(False)
        self.driver_establish_check.setGeometry(QtCore.QRect(20, 70, 151, 17))
        self.driver_establish_check.setText(QtGui.QApplication.translate("TechImplement_Dialog", "Establishment Procedures", None, QtGui.QApplication.UnicodeUTF8))
        self.driver_establish_check.setObjectName(_fromUtf8("driver_establish_check"))
        self.verticalLayout_5.addWidget(self.driver_widget)
        self.implement_rule_title = QtGui.QLabel(self.design_crit_inputs_widget)
        self.implement_rule_title.setMinimumSize(QtCore.QSize(0, 16))
        self.implement_rule_title.setMaximumSize(QtCore.QSize(16777215, 16))
        self.implement_rule_title.setText(QtGui.QApplication.translate("TechImplement_Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Rate of Implementation for different Scales</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.implement_rule_title.setObjectName(_fromUtf8("implement_rule_title"))
        self.verticalLayout_5.addWidget(self.implement_rule_title)
        self.implement_rule_widget = QtGui.QWidget(self.design_crit_inputs_widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(190)
        sizePolicy.setHeightForWidth(self.implement_rule_widget.sizePolicy().hasHeightForWidth())
        self.implement_rule_widget.setSizePolicy(sizePolicy)
        self.implement_rule_widget.setMinimumSize(QtCore.QSize(0, 300))
        self.implement_rule_widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.implement_rule_widget.setObjectName(_fromUtf8("implement_rule_widget"))
        self.impl_rule_lot_title = QtGui.QLabel(self.implement_rule_widget)
        self.impl_rule_lot_title.setGeometry(QtCore.QRect(20, 10, 131, 16))
        self.impl_rule_lot_title.setText(QtGui.QApplication.translate("TechImplement_Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600; font-style:italic;\">Lot Scale</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.impl_rule_lot_title.setObjectName(_fromUtf8("impl_rule_lot_title"))
        self.impl_rule_lot_lbl = QtGui.QLabel(self.implement_rule_widget)
        self.impl_rule_lot_lbl.setGeometry(QtCore.QRect(20, 30, 171, 16))
        self.impl_rule_lot_lbl.setText(QtGui.QApplication.translate("TechImplement_Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Choose implementation dynamic:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.impl_rule_lot_lbl.setObjectName(_fromUtf8("impl_rule_lot_lbl"))
        self.impl_rule_lot_combo = QtGui.QComboBox(self.implement_rule_widget)
        self.impl_rule_lot_combo.setGeometry(QtCore.QRect(210, 30, 211, 16))
        self.impl_rule_lot_combo.setObjectName(_fromUtf8("impl_rule_lot_combo"))
        self.impl_rule_lot_combo.addItem(_fromUtf8(""))
        self.impl_rule_lot_combo.setItemText(0, QtGui.QApplication.translate("TechImplement_Dialog", "Gradual (maintaining level of service)", None, QtGui.QApplication.UnicodeUTF8))
        self.impl_rule_lot_combo.addItem(_fromUtf8(""))
        self.impl_rule_lot_combo.setItemText(1, QtGui.QApplication.translate("TechImplement_Dialog", "Immediate (all at once where possible)", None, QtGui.QApplication.UnicodeUTF8))
        self.impl_rule_lot_combo.addItem(_fromUtf8(""))
        self.impl_rule_lot_combo.setItemText(2, QtGui.QApplication.translate("TechImplement_Dialog", "Delayed (slowed implementation)", None, QtGui.QApplication.UnicodeUTF8))
        self.impl_rule_street_title = QtGui.QLabel(self.implement_rule_widget)
        self.impl_rule_street_title.setGeometry(QtCore.QRect(20, 60, 131, 16))
        self.impl_rule_street_title.setText(QtGui.QApplication.translate("TechImplement_Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600; font-style:italic;\">Street Scale</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.impl_rule_street_title.setObjectName(_fromUtf8("impl_rule_street_title"))
        self.impl_rule_street_combo = QtGui.QComboBox(self.implement_rule_widget)
        self.impl_rule_street_combo.setGeometry(QtCore.QRect(210, 80, 211, 16))
        self.impl_rule_street_combo.setObjectName(_fromUtf8("impl_rule_street_combo"))
        self.impl_rule_street_combo.addItem(_fromUtf8(""))
        self.impl_rule_street_combo.setItemText(0, QtGui.QApplication.translate("TechImplement_Dialog", "Gradual (maintaining level of service)", None, QtGui.QApplication.UnicodeUTF8))
        self.impl_rule_street_combo.addItem(_fromUtf8(""))
        self.impl_rule_street_combo.setItemText(1, QtGui.QApplication.translate("TechImplement_Dialog", "Immediate (all at once where possible)", None, QtGui.QApplication.UnicodeUTF8))
        self.impl_rule_street_combo.addItem(_fromUtf8(""))
        self.impl_rule_street_combo.setItemText(2, QtGui.QApplication.translate("TechImplement_Dialog", "Delayed (slowed implementation)", None, QtGui.QApplication.UnicodeUTF8))
        self.impl_rule_street_lbl = QtGui.QLabel(self.implement_rule_widget)
        self.impl_rule_street_lbl.setGeometry(QtCore.QRect(20, 80, 171, 16))
        self.impl_rule_street_lbl.setText(QtGui.QApplication.translate("TechImplement_Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Choose implementation dynamic:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.impl_rule_street_lbl.setObjectName(_fromUtf8("impl_rule_street_lbl"))
        self.impl_rule_neigh_combo = QtGui.QComboBox(self.implement_rule_widget)
        self.impl_rule_neigh_combo.setGeometry(QtCore.QRect(210, 130, 211, 16))
        self.impl_rule_neigh_combo.setObjectName(_fromUtf8("impl_rule_neigh_combo"))
        self.impl_rule_neigh_combo.addItem(_fromUtf8(""))
        self.impl_rule_neigh_combo.setItemText(0, QtGui.QApplication.translate("TechImplement_Dialog", "Gradual (maintaining level of service)", None, QtGui.QApplication.UnicodeUTF8))
        self.impl_rule_neigh_combo.addItem(_fromUtf8(""))
        self.impl_rule_neigh_combo.setItemText(1, QtGui.QApplication.translate("TechImplement_Dialog", "Immediate (all at once where possible)", None, QtGui.QApplication.UnicodeUTF8))
        self.impl_rule_neigh_combo.addItem(_fromUtf8(""))
        self.impl_rule_neigh_combo.setItemText(2, QtGui.QApplication.translate("TechImplement_Dialog", "Delayed (slowed implementation)", None, QtGui.QApplication.UnicodeUTF8))
        self.impl_rule_neigh_title = QtGui.QLabel(self.implement_rule_widget)
        self.impl_rule_neigh_title.setGeometry(QtCore.QRect(20, 110, 131, 16))
        self.impl_rule_neigh_title.setText(QtGui.QApplication.translate("TechImplement_Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600; font-style:italic;\">Neighbourhood Scale</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.impl_rule_neigh_title.setObjectName(_fromUtf8("impl_rule_neigh_title"))
        self.impl_rule_neigh_lbl = QtGui.QLabel(self.implement_rule_widget)
        self.impl_rule_neigh_lbl.setGeometry(QtCore.QRect(20, 130, 171, 16))
        self.impl_rule_neigh_lbl.setText(QtGui.QApplication.translate("TechImplement_Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Choose implementation dynamic:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.impl_rule_neigh_lbl.setObjectName(_fromUtf8("impl_rule_neigh_lbl"))
        self.impl_rule_prec_lbl = QtGui.QLabel(self.implement_rule_widget)
        self.impl_rule_prec_lbl.setGeometry(QtCore.QRect(20, 210, 171, 16))
        self.impl_rule_prec_lbl.setText(QtGui.QApplication.translate("TechImplement_Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Choose implementation dynamic:</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.impl_rule_prec_lbl.setObjectName(_fromUtf8("impl_rule_prec_lbl"))
        self.impl_rule_prec_combo = QtGui.QComboBox(self.implement_rule_widget)
        self.impl_rule_prec_combo.setGeometry(QtCore.QRect(210, 210, 211, 16))
        self.impl_rule_prec_combo.setObjectName(_fromUtf8("impl_rule_prec_combo"))
        self.impl_rule_prec_combo.addItem(_fromUtf8(""))
        self.impl_rule_prec_combo.setItemText(0, QtGui.QApplication.translate("TechImplement_Dialog", "Gradual (maintaining level of service)", None, QtGui.QApplication.UnicodeUTF8))
        self.impl_rule_prec_combo.addItem(_fromUtf8(""))
        self.impl_rule_prec_combo.setItemText(1, QtGui.QApplication.translate("TechImplement_Dialog", "Immediate (all at once where possible)", None, QtGui.QApplication.UnicodeUTF8))
        self.impl_rule_prec_combo.addItem(_fromUtf8(""))
        self.impl_rule_prec_combo.setItemText(2, QtGui.QApplication.translate("TechImplement_Dialog", "Delayed (slowed implementation)", None, QtGui.QApplication.UnicodeUTF8))
        self.impl_rule_prec_title = QtGui.QLabel(self.implement_rule_widget)
        self.impl_rule_prec_title.setGeometry(QtCore.QRect(20, 190, 131, 16))
        self.impl_rule_prec_title.setText(QtGui.QApplication.translate("TechImplement_Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600; font-style:italic;\">Precinct Scale</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.impl_rule_prec_title.setObjectName(_fromUtf8("impl_rule_prec_title"))
        self.impl_rule_neigh_check = QtGui.QCheckBox(self.implement_rule_widget)
        self.impl_rule_neigh_check.setGeometry(QtCore.QRect(20, 160, 331, 17))
        self.impl_rule_neigh_check.setText(QtGui.QApplication.translate("TechImplement_Dialog", "Implement even if allocated area has not yet been zoned", None, QtGui.QApplication.UnicodeUTF8))
        self.impl_rule_neigh_check.setObjectName(_fromUtf8("impl_rule_neigh_check"))
        self.impl_rule_prec_check = QtGui.QCheckBox(self.implement_rule_widget)
        self.impl_rule_prec_check.setGeometry(QtCore.QRect(20, 240, 331, 17))
        self.impl_rule_prec_check.setText(QtGui.QApplication.translate("TechImplement_Dialog", "Implement even if allocated area has not yet been zoned", None, QtGui.QApplication.UnicodeUTF8))
        self.impl_rule_prec_check.setObjectName(_fromUtf8("impl_rule_prec_check"))
        self.impl_rule_prec_allow = QtGui.QCheckBox(self.implement_rule_widget)
        self.impl_rule_prec_allow.setGeometry(QtCore.QRect(20, 270, 321, 17))
        self.impl_rule_prec_allow.setText(QtGui.QApplication.translate("TechImplement_Dialog", "Allow implementation if upstream development > % threshold", None, QtGui.QApplication.UnicodeUTF8))
        self.impl_rule_prec_allow.setObjectName(_fromUtf8("impl_rule_prec_allow"))
        self.impl_rule_prec_spin = QtGui.QSpinBox(self.implement_rule_widget)
        self.impl_rule_prec_spin.setGeometry(QtCore.QRect(350, 270, 61, 16))
        self.impl_rule_prec_spin.setSuffix(QtGui.QApplication.translate("TechImplement_Dialog", "%", None, QtGui.QApplication.UnicodeUTF8))
        self.impl_rule_prec_spin.setMaximum(100)
        self.impl_rule_prec_spin.setObjectName(_fromUtf8("impl_rule_prec_spin"))
        self.verticalLayout_5.addWidget(self.implement_rule_widget)
        self.techimplement_inputs.setWidget(self.design_crit_inputs_widget)
        self.gridLayout_22.addWidget(self.techimplement_inputs, 0, 0, 2, 2)
        self.horizontalLayout_4.addWidget(self.techimplement_widget)
        self.implement_sidebar = QtGui.QFrame(self.DesignCriteria)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.implement_sidebar.sizePolicy().hasHeightForWidth())
        self.implement_sidebar.setSizePolicy(sizePolicy)
        self.implement_sidebar.setMinimumSize(QtCore.QSize(221, 0))
        self.implement_sidebar.setMaximumSize(QtCore.QSize(221, 16777215))
        self.implement_sidebar.setFrameShape(QtGui.QFrame.StyledPanel)
        self.implement_sidebar.setFrameShadow(QtGui.QFrame.Raised)
        self.implement_sidebar.setObjectName(_fromUtf8("implement_sidebar"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.implement_sidebar)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.implement_sidebar_img = QtGui.QLabel(self.implement_sidebar)
        self.implement_sidebar_img.setMinimumSize(QtCore.QSize(0, 145))
        self.implement_sidebar_img.setText(_fromUtf8(""))
        self.implement_sidebar_img.setPixmap(QtGui.QPixmap(_fromUtf8("../../../../../D4W-wsudimplement.png")))
        self.implement_sidebar_img.setObjectName(_fromUtf8("implement_sidebar_img"))
        self.verticalLayout_3.addWidget(self.implement_sidebar_img)
        self.implement_sidebar_descr = QtGui.QTextBrowser(self.implement_sidebar)
        self.implement_sidebar_descr.setHtml(QtGui.QApplication.translate("TechImplement_Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Adust dynamics settings for technology implementation. Set different rules for various scales and determine driving forces behind system implementation.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.implement_sidebar_descr.setObjectName(_fromUtf8("implement_sidebar_descr"))
        self.verticalLayout_3.addWidget(self.implement_sidebar_descr)
        self.horizontalLayout_4.addWidget(self.implement_sidebar)
        self.techimplement_input.addTab(self.DesignCriteria, _fromUtf8(""))
        self.verticalLayout.addWidget(self.techimplement_input)
        self.techimplement_footer = QtGui.QWidget(TechImplement_Dialog)
        self.techimplement_footer.setMaximumSize(QtCore.QSize(16777215, 38))
        self.techimplement_footer.setObjectName(_fromUtf8("techimplement_footer"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.techimplement_footer)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.remarks = QtGui.QLabel(self.techimplement_footer)
        self.remarks.setText(QtGui.QApplication.translate("TechImplement_Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-style:italic;\">UrbanBEATS.techimplement - v0.80 - (C) 2012 Peter M. Bach </span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.remarks.setObjectName(_fromUtf8("remarks"))
        self.horizontalLayout.addWidget(self.remarks)
        self.buttonBox = QtGui.QDialogButtonBox(self.techimplement_footer)
        self.buttonBox.setMaximumSize(QtCore.QSize(16777215, 23))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout.addWidget(self.buttonBox)
        self.helpButton = QtGui.QPushButton(self.techimplement_footer)
        self.helpButton.setWhatsThis(QtGui.QApplication.translate("TechImplement_Dialog", "Are you serious?", None, QtGui.QApplication.UnicodeUTF8))
        self.helpButton.setText(QtGui.QApplication.translate("TechImplement_Dialog", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.helpButton.setObjectName(_fromUtf8("helpButton"))
        self.horizontalLayout.addWidget(self.helpButton)
        self.verticalLayout.addWidget(self.techimplement_footer)

        self.retranslateUi(TechImplement_Dialog)
        self.techimplement_input.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TechImplement_Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TechImplement_Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TechImplement_Dialog)

    def retranslateUi(self, TechImplement_Dialog):
        self.techimplement_input.setTabText(self.techimplement_input.indexOf(self.DesignCriteria), QtGui.QApplication.translate("TechImplement_Dialog", "Implementation Rules", None, QtGui.QApplication.UnicodeUTF8))

