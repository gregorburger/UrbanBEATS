# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'delinblocksgui.ui'
#
# Created: Wed Mar 28 18:32:28 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DelinBlocksDialog(object):
    def setupUi(self, DelinBlocksDialog):
        DelinBlocksDialog.setObjectName(_fromUtf8("DelinBlocksDialog"))
        DelinBlocksDialog.resize(641, 371)
        self.verticalLayout = QtGui.QVBoxLayout(DelinBlocksDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.title_frame = QtGui.QFrame(DelinBlocksDialog)
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
        self.widget = QtGui.QWidget(DelinBlocksDialog)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.scrollArea = QtGui.QScrollArea(self.widget)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 429, 605))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.gensim_widget = QtGui.QWidget(self.scrollAreaWidgetContents)
        self.gensim_widget.setMinimumSize(QtCore.QSize(0, 60))
        self.gensim_widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.gensim_widget.setObjectName(_fromUtf8("gensim_widget"))
        self.urbansim_in_check = QtGui.QCheckBox(self.gensim_widget)
        self.urbansim_in_check.setGeometry(QtCore.QRect(210, 30, 141, 17))
        self.urbansim_in_check.setObjectName(_fromUtf8("urbansim_in_check"))
        self.blocksize_lbl = QtGui.QLabel(self.gensim_widget)
        self.blocksize_lbl.setGeometry(QtCore.QRect(20, 29, 71, 16))
        self.blocksize_lbl.setObjectName(_fromUtf8("blocksize_lbl"))
        self.blocksize_in = QtGui.QLineEdit(self.gensim_widget)
        self.blocksize_in.setGeometry(QtCore.QRect(100, 29, 71, 20))
        self.blocksize_in.setObjectName(_fromUtf8("blocksize_in"))
        self.optionsgs_lbl = QtGui.QLabel(self.gensim_widget)
        self.optionsgs_lbl.setGeometry(QtCore.QRect(10, 5, 111, 16))
        self.optionsgs_lbl.setObjectName(_fromUtf8("optionsgs_lbl"))
        self.verticalLayout_3.addWidget(self.gensim_widget)
        self.addpar_widget = QtGui.QWidget(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addpar_widget.sizePolicy().hasHeightForWidth())
        self.addpar_widget.setSizePolicy(sizePolicy)
        self.addpar_widget.setMinimumSize(QtCore.QSize(0, 165))
        self.addpar_widget.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.addpar_widget.setObjectName(_fromUtf8("addpar_widget"))
        self.soc_par1_box = QtGui.QLineEdit(self.addpar_widget)
        self.soc_par1_box.setGeometry(QtCore.QRect(230, 110, 161, 20))
        self.soc_par1_box.setText(_fromUtf8(""))
        self.soc_par1_box.setObjectName(_fromUtf8("soc_par1_box"))
        self.soc_par1_check = QtGui.QCheckBox(self.addpar_widget)
        self.soc_par1_check.setGeometry(QtCore.QRect(30, 110, 191, 17))
        self.soc_par1_check.setObjectName(_fromUtf8("soc_par1_check"))
        self.soc_par2_check = QtGui.QCheckBox(self.addpar_widget)
        self.soc_par2_check.setGeometry(QtCore.QRect(30, 135, 221, 17))
        self.soc_par2_check.setObjectName(_fromUtf8("soc_par2_check"))
        self.soc_par2_box = QtGui.QLineEdit(self.addpar_widget)
        self.soc_par2_box.setGeometry(QtCore.QRect(230, 135, 161, 20))
        self.soc_par2_box.setText(_fromUtf8(""))
        self.soc_par2_box.setObjectName(_fromUtf8("soc_par2_box"))
        self.optionsadin_lbl = QtGui.QLabel(self.addpar_widget)
        self.optionsadin_lbl.setGeometry(QtCore.QRect(10, 5, 141, 16))
        self.optionsadin_lbl.setObjectName(_fromUtf8("optionsadin_lbl"))
        self.planmap_check = QtGui.QCheckBox(self.addpar_widget)
        self.planmap_check.setGeometry(QtCore.QRect(30, 50, 101, 17))
        self.planmap_check.setObjectName(_fromUtf8("planmap_check"))
        self.localmap_check = QtGui.QCheckBox(self.addpar_widget)
        self.localmap_check.setGeometry(QtCore.QRect(140, 50, 101, 17))
        self.localmap_check.setObjectName(_fromUtf8("localmap_check"))
        self.urbinfo_lbl = QtGui.QLabel(self.addpar_widget)
        self.urbinfo_lbl.setGeometry(QtCore.QRect(15, 30, 161, 16))
        self.urbinfo_lbl.setObjectName(_fromUtf8("urbinfo_lbl"))
        self.roadnet_check = QtGui.QCheckBox(self.addpar_widget)
        self.roadnet_check.setEnabled(False)
        self.roadnet_check.setGeometry(QtCore.QRect(240, 50, 101, 17))
        self.roadnet_check.setObjectName(_fromUtf8("roadnet_check"))
        self.soc_params_lbl = QtGui.QLabel(self.addpar_widget)
        self.soc_params_lbl.setGeometry(QtCore.QRect(15, 85, 201, 16))
        self.soc_params_lbl.setObjectName(_fromUtf8("soc_params_lbl"))
        self.verticalLayout_3.addWidget(self.addpar_widget)
        self.connect_widget = QtGui.QWidget(self.scrollAreaWidgetContents)
        self.connect_widget.setMinimumSize(QtCore.QSize(0, 350))
        self.connect_widget.setObjectName(_fromUtf8("connect_widget"))
        self.radioVNeum = QtGui.QRadioButton(self.connect_widget)
        self.radioVNeum.setGeometry(QtCore.QRect(80, 110, 101, 16))
        self.radioVNeum.setChecked(False)
        self.radioVNeum.setObjectName(_fromUtf8("radioVNeum"))
        self.img_Moore = QtGui.QLabel(self.connect_widget)
        self.img_Moore.setGeometry(QtCore.QRect(30, 55, 41, 41))
        self.img_Moore.setText(_fromUtf8(""))
        self.img_Moore.setPixmap(QtGui.QPixmap(_fromUtf8("../../../../../../D4W-MooreNH.png")))
        self.img_Moore.setObjectName(_fromUtf8("img_Moore"))
        self.neighb_lbl = QtGui.QLabel(self.connect_widget)
        self.neighb_lbl.setGeometry(QtCore.QRect(20, 30, 231, 16))
        self.neighb_lbl.setObjectName(_fromUtf8("neighb_lbl"))
        self.img_vNeum = QtGui.QLabel(self.connect_widget)
        self.img_vNeum.setGeometry(QtCore.QRect(30, 100, 41, 41))
        self.img_vNeum.setText(_fromUtf8(""))
        self.img_vNeum.setPixmap(QtGui.QPixmap(_fromUtf8("../../../../../../D4W-vNeumann.png")))
        self.img_vNeum.setObjectName(_fromUtf8("img_vNeum"))
        self.radioMoore = QtGui.QRadioButton(self.connect_widget)
        self.radioMoore.setEnabled(True)
        self.radioMoore.setGeometry(QtCore.QRect(80, 65, 82, 16))
        self.radioMoore.setCheckable(True)
        self.radioMoore.setObjectName(_fromUtf8("radioMoore"))
        self.optionsmc_lbl = QtGui.QLabel(self.connect_widget)
        self.optionsmc_lbl.setGeometry(QtCore.QRect(10, 5, 231, 16))
        self.optionsmc_lbl.setObjectName(_fromUtf8("optionsmc_lbl"))
        self.flowpath_lbl = QtGui.QLabel(self.connect_widget)
        self.flowpath_lbl.setGeometry(QtCore.QRect(20, 155, 131, 16))
        self.flowpath_lbl.setObjectName(_fromUtf8("flowpath_lbl"))
        self.flowpath_combo = QtGui.QComboBox(self.connect_widget)
        self.flowpath_combo.setGeometry(QtCore.QRect(30, 180, 191, 22))
        self.flowpath_combo.setObjectName(_fromUtf8("flowpath_combo"))
        self.flowpath_combo.addItem(_fromUtf8(""))
        self.flowpath_combo.addItem(_fromUtf8(""))
        self.conceptsewer_check = QtGui.QCheckBox(self.connect_widget)
        self.conceptsewer_check.setEnabled(False)
        self.conceptsewer_check.setGeometry(QtCore.QRect(30, 310, 181, 17))
        self.conceptsewer_check.setObjectName(_fromUtf8("conceptsewer_check"))
        self.conceptnet_lbl = QtGui.QLabel(self.connect_widget)
        self.conceptnet_lbl.setGeometry(QtCore.QRect(20, 290, 131, 16))
        self.conceptnet_lbl.setObjectName(_fromUtf8("conceptnet_lbl"))
        self.conceptsupply_check = QtGui.QCheckBox(self.connect_widget)
        self.conceptsupply_check.setEnabled(False)
        self.conceptsupply_check.setGeometry(QtCore.QRect(30, 330, 191, 17))
        self.conceptsupply_check.setObjectName(_fromUtf8("conceptsupply_check"))
        self.demsmooth_check = QtGui.QCheckBox(self.connect_widget)
        self.demsmooth_check.setGeometry(QtCore.QRect(30, 215, 161, 17))
        self.demsmooth_check.setObjectName(_fromUtf8("demsmooth_check"))
        self.demsmooth_spin = QtGui.QSpinBox(self.connect_widget)
        self.demsmooth_spin.setGeometry(QtCore.QRect(190, 215, 31, 20))
        self.demsmooth_spin.setMinimum(1)
        self.demsmooth_spin.setMaximum(2)
        self.demsmooth_spin.setObjectName(_fromUtf8("demsmooth_spin"))
        self.delinbasin_lbl = QtGui.QLabel(self.connect_widget)
        self.delinbasin_lbl.setGeometry(QtCore.QRect(20, 240, 131, 16))
        self.delinbasin_lbl.setObjectName(_fromUtf8("delinbasin_lbl"))
        self.delinbasin_check = QtGui.QCheckBox(self.connect_widget)
        self.delinbasin_check.setGeometry(QtCore.QRect(30, 260, 231, 17))
        self.delinbasin_check.setObjectName(_fromUtf8("delinbasin_check"))
        self.neighb_vnfp_check = QtGui.QCheckBox(self.connect_widget)
        self.neighb_vnfp_check.setGeometry(QtCore.QRect(210, 100, 191, 17))
        self.neighb_vnfp_check.setObjectName(_fromUtf8("neighb_vnfp_check"))
        self.neighb_vnpd_check = QtGui.QCheckBox(self.connect_widget)
        self.neighb_vnpd_check.setGeometry(QtCore.QRect(210, 120, 191, 17))
        self.neighb_vnpd_check.setObjectName(_fromUtf8("neighb_vnpd_check"))
        self.neighb_lbl2 = QtGui.QLabel(self.connect_widget)
        self.neighb_lbl2.setGeometry(QtCore.QRect(180, 80, 221, 16))
        self.neighb_lbl2.setObjectName(_fromUtf8("neighb_lbl2"))
        self.delinbasin_box = QtGui.QLineEdit(self.connect_widget)
        self.delinbasin_box.setGeometry(QtCore.QRect(240, 260, 61, 21))
        self.delinbasin_box.setObjectName(_fromUtf8("delinbasin_box"))
        self.delinbasin_lbl2 = QtGui.QLabel(self.connect_widget)
        self.delinbasin_lbl2.setGeometry(QtCore.QRect(310, 260, 61, 16))
        self.delinbasin_lbl2.setObjectName(_fromUtf8("delinbasin_lbl2"))
        self.verticalLayout_3.addWidget(self.connect_widget)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scrollArea)
        self.widget_2 = QtGui.QWidget(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy)
        self.widget_2.setMinimumSize(QtCore.QSize(151, 0))
        self.widget_2.setMaximumSize(QtCore.QSize(151, 16777215))
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget_2)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.img_blocks = QtGui.QLabel(self.widget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.img_blocks.sizePolicy().hasHeightForWidth())
        self.img_blocks.setSizePolicy(sizePolicy)
        self.img_blocks.setMinimumSize(QtCore.QSize(0, 90))
        self.img_blocks.setMaximumSize(QtCore.QSize(16777215, 90))
        self.img_blocks.setText(_fromUtf8(""))
        self.img_blocks.setPixmap(QtGui.QPixmap(_fromUtf8("../../../../../../D4W-BBcells.png")))
        self.img_blocks.setObjectName(_fromUtf8("img_blocks"))
        self.verticalLayout_2.addWidget(self.img_blocks)
        self.descr_blocks = QtGui.QTextBrowser(self.widget_2)
        self.descr_blocks.setObjectName(_fromUtf8("descr_blocks"))
        self.verticalLayout_2.addWidget(self.descr_blocks)
        self.horizontalLayout.addWidget(self.widget_2)
        self.verticalLayout.addWidget(self.widget)
        self.widget_4 = QtGui.QWidget(DelinBlocksDialog)
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
        self.helpButton = QtGui.QPushButton(self.widget_4)
        self.helpButton.setEnabled(True)
        self.helpButton.setObjectName(_fromUtf8("helpButton"))
        self.horizontalLayout_2.addWidget(self.helpButton)
        self.verticalLayout.addWidget(self.widget_4)

        self.retranslateUi(DelinBlocksDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DelinBlocksDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DelinBlocksDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(DelinBlocksDialog)

    def retranslateUi(self, DelinBlocksDialog):
        DelinBlocksDialog.setWindowTitle(QtGui.QApplication.translate("DelinBlocksDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.dbtitle.setText(QtGui.QApplication.translate("DelinBlocksDialog", "Delineate Blocks", None, QtGui.QApplication.UnicodeUTF8))
        self.dbsubtitle.setText(QtGui.QApplication.translate("DelinBlocksDialog", "Creates the grid of cells that represents a discretised version of the input region or city.", None, QtGui.QApplication.UnicodeUTF8))
        self.urbansim_in_check.setWhatsThis(QtGui.QApplication.translate("DelinBlocksDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Check this box if the input data is derived from UrbanSim Output. Check this is part of a DAnCE4Water simulation where the Urban Development Module (UDM) has been initialised.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.urbansim_in_check.setText(QtGui.QApplication.translate("DelinBlocksDialog", "Input from UrbanSim?", None, QtGui.QApplication.UnicodeUTF8))
        self.blocksize_lbl.setWhatsThis(QtGui.QApplication.translate("DelinBlocksDialog", "Width of the square cell in the city grid in metres", None, QtGui.QApplication.UnicodeUTF8))
        self.blocksize_lbl.setText(QtGui.QApplication.translate("DelinBlocksDialog", "Block Size [m]", None, QtGui.QApplication.UnicodeUTF8))
        self.optionsgs_lbl.setWhatsThis(QtGui.QApplication.translate("DelinBlocksDialog", "Width of the square cell in the city grid in metres", None, QtGui.QApplication.UnicodeUTF8))
        self.optionsgs_lbl.setText(QtGui.QApplication.translate("DelinBlocksDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">General Simulation</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.soc_par1_check.setWhatsThis(QtGui.QApplication.translate("DelinBlocksDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Check this box if you would like to experiment with social parameters. DAnCE4Water-BPM (when used as standalone) allows for a maximum of two socio-economic parameters to be specified. Input must be in the form of probabilities (between 0 and 1).</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.soc_par1_check.setText(QtGui.QApplication.translate("DelinBlocksDialog", "Include Social Parameter 1 - Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.soc_par2_check.setWhatsThis(QtGui.QApplication.translate("DelinBlocksDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Check this box if you would like to experiment with social parameters. DAnCE4Water-BPM (when used as standalone) allows for a maximum of two socio-economic parameters to be specified. Input must be in the form of probabilities (between 0 and 1).</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.soc_par2_check.setText(QtGui.QApplication.translate("DelinBlocksDialog", "Include Social Parameter 2 - Name:", None, QtGui.QApplication.UnicodeUTF8))
        self.optionsadin_lbl.setWhatsThis(QtGui.QApplication.translate("DelinBlocksDialog", "Width of the square cell in the city grid in metres", None, QtGui.QApplication.UnicodeUTF8))
        self.optionsadin_lbl.setText(QtGui.QApplication.translate("DelinBlocksDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Additional Inputs</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.planmap_check.setWhatsThis(QtGui.QApplication.translate("DelinBlocksDialog", "A raster layer that is aligned the basic inputs zoning and population map. The planner\'s map contains typology-ratios for all land zones, specified according to the user\'s urban planning snapshot for the region in question. Refer to user guide for more information on how to create this map.", None, QtGui.QApplication.UnicodeUTF8))
        self.planmap_check.setText(QtGui.QApplication.translate("DelinBlocksDialog", "Planner\'s Map", None, QtGui.QApplication.UnicodeUTF8))
        self.localmap_check.setWhatsThis(QtGui.QApplication.translate("DelinBlocksDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">A raster layer that contains information on the location of the central business district and/or activity centres for the region.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">1-2 are urban centres</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">1 = CBD</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">2 = Activity Centre</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">3-7 are water-related point landmarks</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">3 = WWTP</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">4 = DWTP</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">5 = Outfall/Outlet</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.localmap_check.setText(QtGui.QApplication.translate("DelinBlocksDialog", "Locality Map", None, QtGui.QApplication.UnicodeUTF8))
        self.urbinfo_lbl.setText(QtGui.QApplication.translate("DelinBlocksDialog", "Urban Planning Information", None, QtGui.QApplication.UnicodeUTF8))
        self.roadnet_check.setWhatsThis(QtGui.QApplication.translate("DelinBlocksDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">A network maps of all road networks (polylines) in the region</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.roadnet_check.setText(QtGui.QApplication.translate("DelinBlocksDialog", "Road Networks", None, QtGui.QApplication.UnicodeUTF8))
        self.soc_params_lbl.setText(QtGui.QApplication.translate("DelinBlocksDialog", "Societal and Demographic Information", None, QtGui.QApplication.UnicodeUTF8))
        self.radioVNeum.setWhatsThis(QtGui.QApplication.translate("DelinBlocksDialog", "Von Neumann, four cardinal directions on either side of the central block.", None, QtGui.QApplication.UnicodeUTF8))
        self.radioVNeum.setText(QtGui.QApplication.translate("DelinBlocksDialog", "Von Neumann", None, QtGui.QApplication.UnicodeUTF8))
        self.neighb_lbl.setWhatsThis(QtGui.QApplication.translate("DelinBlocksDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">How many blocks to consider when determining drainage fluxes (the greater the number, the greater the computational burden).</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.neighb_lbl.setText(QtGui.QApplication.translate("DelinBlocksDialog", "Select Neighbourhood (default: Moore):", None, QtGui.QApplication.UnicodeUTF8))
        self.radioMoore.setWhatsThis(QtGui.QApplication.translate("DelinBlocksDialog", "Moore, all eight neighbours around the central block.", None, QtGui.QApplication.UnicodeUTF8))
        self.radioMoore.setText(QtGui.QApplication.translate("DelinBlocksDialog", "Moore", None, QtGui.QApplication.UnicodeUTF8))
        self.optionsmc_lbl.setWhatsThis(QtGui.QApplication.translate("DelinBlocksDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">How many blocks to consider when determining drainage fluxes (the greater the number, the greater the computational burden).</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.optionsmc_lbl.setText(QtGui.QApplication.translate("DelinBlocksDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Regional Extents &amp; Map Connectivity</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.flowpath_lbl.setWhatsThis(QtGui.QApplication.translate("DelinBlocksDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Method of finding flow direction in the digital elevation model or in this case the grid of blocks. Refer to publications for further information.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">D-infinity - Tarboton, 1997. A new method for the determination of flow directions and upslope areas in grid digital elevation models. Water Resources Research v33.2, 309-319</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">D8 - O\'Callaghan &amp; Mark, 1984. The Extraction of Drainage Networks from Digital Elevation Data. Computer Vision, Graphics and Image Processing v28, 323-344</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Divergent Flows - Freeman, 1991</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.flowpath_lbl.setText(QtGui.QApplication.translate("DelinBlocksDialog", "Flow Path Method:", None, QtGui.QApplication.UnicodeUTF8))
        self.flowpath_combo.setItemText(0, QtGui.QApplication.translate("DelinBlocksDialog", "D8 (O\'Callaghan & Mark, 1984)", None, QtGui.QApplication.UnicodeUTF8))
        self.flowpath_combo.setItemText(1, QtGui.QApplication.translate("DelinBlocksDialog", "D-infinity (Tarboton, 1997)", None, QtGui.QApplication.UnicodeUTF8))
        self.conceptsewer_check.setText(QtGui.QApplication.translate("DelinBlocksDialog", "Create conceptual sewer network", None, QtGui.QApplication.UnicodeUTF8))
        self.conceptnet_lbl.setWhatsThis(QtGui.QApplication.translate("DelinBlocksDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Will create a conceptual sewer network structure for the region being modelled if checked. The generation is random, but is meant to provide a more realistic conceptual assessment of the region.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">If the model is part of a full DAnCE4Water Simulation, then leave these boxes unchecked.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.conceptnet_lbl.setText(QtGui.QApplication.translate("DelinBlocksDialog", "Conceptual Networks:", None, QtGui.QApplication.UnicodeUTF8))
        self.conceptsupply_check.setText(QtGui.QApplication.translate("DelinBlocksDialog", "Create conceptual supply network", None, QtGui.QApplication.UnicodeUTF8))
        self.demsmooth_check.setWhatsThis(QtGui.QApplication.translate("DelinBlocksDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Applies a weighted average smoothing filter over the DEM layer. </span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.demsmooth_check.setText(QtGui.QApplication.translate("DelinBlocksDialog", "DEM Smoothing (no. passes)", None, QtGui.QApplication.UnicodeUTF8))
        self.delinbasin_lbl.setWhatsThis(QtGui.QApplication.translate("DelinBlocksDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Will create a conceptual sewer network structure for the region being modelled if checked. The generation is random, but is meant to provide a more realistic conceptual assessment of the region.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">If the model is part of a full DAnCE4Water Simulation, then leave these boxes unchecked.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.delinbasin_lbl.setText(QtGui.QApplication.translate("DelinBlocksDialog", "Delineate Basins:", None, QtGui.QApplication.UnicodeUTF8))
        self.delinbasin_check.setWhatsThis(QtGui.QApplication.translate("DelinBlocksDialog", "Check if you want to avoid localised ponds forming in the region. If this is of particular interest because the DEM\'s accuracy has been assured and the purpose of the simulation is to assess these problem spots, then leave this box unchecked.\n"
"\n"
"Correction proceeds as follows:\n"
"- If cell cannot transfer water downhill, but there is an adjacent cell with identical elevation within tolerance limit, it will transfer the water into this.\n"
"- If tolerance limit is not met, cell\'s water is routed directly to catchment outlet.", None, QtGui.QApplication.UnicodeUTF8))
        self.delinbasin_check.setText(QtGui.QApplication.translate("DelinBlocksDialog", "Limit search to maximum basin size of:", None, QtGui.QApplication.UnicodeUTF8))
        self.neighb_vnfp_check.setWhatsThis(QtGui.QApplication.translate("DelinBlocksDialog", "Check if you want to avoid localised ponds forming in the region. If this is of particular interest because the DEM\'s accuracy has been assured and the purpose of the simulation is to assess these problem spots, then leave this box unchecked.\n"
"\n"
"Correction proceeds as follows:\n"
"- If cell cannot transfer water downhill, but there is an adjacent cell with identical elevation within tolerance limit, it will transfer the water into this.\n"
"- If tolerance limit is not met, cell\'s water is routed directly to catchment outlet.", None, QtGui.QApplication.UnicodeUTF8))
        self.neighb_vnfp_check.setText(QtGui.QApplication.translate("DelinBlocksDialog", "Flow Path Delineation", None, QtGui.QApplication.UnicodeUTF8))
        self.neighb_vnpd_check.setWhatsThis(QtGui.QApplication.translate("DelinBlocksDialog", "Check if you want to avoid localised ponds forming in the region. If this is of particular interest because the DEM\'s accuracy has been assured and the purpose of the simulation is to assess these problem spots, then leave this box unchecked.\n"
"\n"
"Correction proceeds as follows:\n"
"- If cell cannot transfer water downhill, but there is an adjacent cell with identical elevation within tolerance limit, it will transfer the water into this.\n"
"- If tolerance limit is not met, cell\'s water is routed directly to catchment outlet.", None, QtGui.QApplication.UnicodeUTF8))
        self.neighb_vnpd_check.setText(QtGui.QApplication.translate("DelinBlocksDialog", "Patch Delineation", None, QtGui.QApplication.UnicodeUTF8))
        self.neighb_lbl2.setWhatsThis(QtGui.QApplication.translate("DelinBlocksDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Method of finding flow direction in the digital elevation model or in this case the grid of blocks. Refer to publications for further information.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">D-infinity - Tarboton, 1997. A new method for the determination of flow directions and upslope areas in grid digital elevation models. Water Resources Research v33.2, 309-319</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">D8 - O\'Callaghan &amp; Mark, 1984. The Extraction of Drainage Networks from Digital Elevation Data. Computer Vision, Graphics and Image Processing v28, 323-344</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Divergent Flows - Freeman, 1991</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.neighb_lbl2.setText(QtGui.QApplication.translate("DelinBlocksDialog", "Apply Von Neumann Neighbourhood to: ", None, QtGui.QApplication.UnicodeUTF8))
        self.delinbasin_lbl2.setWhatsThis(QtGui.QApplication.translate("DelinBlocksDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Method of finding flow direction in the digital elevation model or in this case the grid of blocks. Refer to publications for further information.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">D-infinity - Tarboton, 1997. A new method for the determination of flow directions and upslope areas in grid digital elevation models. Water Resources Research v33.2, 309-319</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">D8 - O\'Callaghan &amp; Mark, 1984. The Extraction of Drainage Networks from Digital Elevation Data. Computer Vision, Graphics and Image Processing v28, 323-344</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Divergent Flows - Freeman, 1991</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.delinbasin_lbl2.setText(QtGui.QApplication.translate("DelinBlocksDialog", "hectares", None, QtGui.QApplication.UnicodeUTF8))
        self.descr_blocks.setHtml(QtGui.QApplication.translate("DelinBlocksDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Set basic simulation parameters for creating the block map of input region. Define additional inputs and specify neighbourhood and DEM analysis rules.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.remarks.setText(QtGui.QApplication.translate("DelinBlocksDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-style:italic;\">UrbanBEATS.delinblocks</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.remarks2.setText(QtGui.QApplication.translate("DelinBlocksDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-style:italic;\">v0.80 - (C) 2012 Peter M. Bach</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.helpButton.setWhatsThis(QtGui.QApplication.translate("DelinBlocksDialog", "You do not need help right now! :)", None, QtGui.QApplication.UnicodeUTF8))
        self.helpButton.setText(QtGui.QApplication.translate("DelinBlocksDialog", "Help", None, QtGui.QApplication.UnicodeUTF8))

