# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1368, 1060)
        MainWindow.setStyleSheet("background-color: rgb(33, 37, 43);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background: transparent;\n"
"color: rgb(210, 210, 210);")
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.leftButtonsFrame = QtWidgets.QFrame(self.centralwidget)
        self.leftButtonsFrame.setMinimumSize(QtCore.QSize(60, 0))
        self.leftButtonsFrame.setMaximumSize(QtCore.QSize(60, 16777215))
        self.leftButtonsFrame.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.leftButtonsFrame.setStyleSheet("background-color: rgb(27, 29, 35);")
        self.leftButtonsFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.leftButtonsFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.leftButtonsFrame.setLineWidth(0)
        self.leftButtonsFrame.setObjectName("leftButtonsFrame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.leftButtonsFrame)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.userLogo = QtWidgets.QFrame(self.leftButtonsFrame)
        self.userLogo.setMinimumSize(QtCore.QSize(60, 50))
        self.userLogo.setMaximumSize(QtCore.QSize(60, 50))
        self.userLogo.setStyleSheet("image: url(:/icons/24x24/cil-user.png);\n"
"background-color: rgb(22, 25, 31);")
        self.userLogo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.userLogo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.userLogo.setObjectName("userLogo")
        self.verticalLayout_4.addWidget(self.userLogo)
        self.uploadDefaultDatasetButton = QtWidgets.QPushButton(self.leftButtonsFrame)
        self.uploadDefaultDatasetButton.setMinimumSize(QtCore.QSize(60, 60))
        self.uploadDefaultDatasetButton.setMaximumSize(QtCore.QSize(60, 60))
        self.uploadDefaultDatasetButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.uploadDefaultDatasetButton.setStyleSheet("QPushButton {\n"
"    background-position: center;\n"
"    background-repeat: no-reperat;\n"
"    border: none;\n"
"    background-color: rgb(27, 29, 35);\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.uploadDefaultDatasetButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/24x24/cil-arrow-circle-bottom.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.uploadDefaultDatasetButton.setIcon(icon)
        self.uploadDefaultDatasetButton.setIconSize(QtCore.QSize(24, 24))
        self.uploadDefaultDatasetButton.setObjectName("uploadDefaultDatasetButton")
        self.verticalLayout_4.addWidget(self.uploadDefaultDatasetButton)
        self.uploadDatasetButton = QtWidgets.QPushButton(self.leftButtonsFrame)
        self.uploadDatasetButton.setMinimumSize(QtCore.QSize(60, 60))
        self.uploadDatasetButton.setMaximumSize(QtCore.QSize(60, 60))
        self.uploadDatasetButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.uploadDatasetButton.setStyleSheet("QPushButton {\n"
"    background-position: center;\n"
"    background-repeat: no-reperat;\n"
"    border: none;\n"
"    background-color: rgb(27, 29, 35);\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.uploadDatasetButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/24x24/cil-folder-open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.uploadDatasetButton.setIcon(icon1)
        self.uploadDatasetButton.setIconSize(QtCore.QSize(24, 24))
        self.uploadDatasetButton.setObjectName("uploadDatasetButton")
        self.verticalLayout_4.addWidget(self.uploadDatasetButton)
        self.videoButton = QtWidgets.QPushButton(self.leftButtonsFrame)
        self.videoButton.setMinimumSize(QtCore.QSize(60, 60))
        self.videoButton.setMaximumSize(QtCore.QSize(60, 60))
        self.videoButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.videoButton.setStyleSheet("QPushButton {\n"
"    background-position: center;\n"
"    background-repeat: no-reperat;\n"
"    border: none;\n"
"    background-color: rgb(27, 29, 35);\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.videoButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/24x24/cil-video.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.videoButton.setIcon(icon2)
        self.videoButton.setIconSize(QtCore.QSize(24, 24))
        self.videoButton.setObjectName("videoButton")
        self.verticalLayout_4.addWidget(self.videoButton)
        self.pointCloudButton = QtWidgets.QPushButton(self.leftButtonsFrame)
        self.pointCloudButton.setMinimumSize(QtCore.QSize(60, 60))
        self.pointCloudButton.setMaximumSize(QtCore.QSize(60, 60))
        self.pointCloudButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.pointCloudButton.setStyleSheet("QPushButton {\n"
"    background-position: center;\n"
"    background-repeat: no-reperat;\n"
"    border: none;\n"
"    background-color: rgb(27, 29, 35);\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.pointCloudButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/24x24/cil-3d.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pointCloudButton.setIcon(icon3)
        self.pointCloudButton.setIconSize(QtCore.QSize(24, 24))
        self.pointCloudButton.setObjectName("pointCloudButton")
        self.verticalLayout_4.addWidget(self.pointCloudButton)
        self.camera3dButton = QtWidgets.QPushButton(self.leftButtonsFrame)
        self.camera3dButton.setMinimumSize(QtCore.QSize(60, 60))
        self.camera3dButton.setMaximumSize(QtCore.QSize(60, 60))
        self.camera3dButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.camera3dButton.setStyleSheet("QPushButton {\n"
"    background-position: center;\n"
"    background-repeat: no-reperat;\n"
"    border: none;\n"
"    background-color: rgb(27, 29, 35);\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.camera3dButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/24x24/cil-camera.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.camera3dButton.setIcon(icon4)
        self.camera3dButton.setIconSize(QtCore.QSize(24, 24))
        self.camera3dButton.setObjectName("camera3dButton")
        self.verticalLayout_4.addWidget(self.camera3dButton)
        self.chartButton = QtWidgets.QPushButton(self.leftButtonsFrame)
        self.chartButton.setMinimumSize(QtCore.QSize(60, 60))
        self.chartButton.setMaximumSize(QtCore.QSize(60, 60))
        self.chartButton.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.chartButton.setStyleSheet("QPushButton {\n"
"    background-position: center;\n"
"    background-repeat: no-reperat;\n"
"    border: none;\n"
"    background-color: rgb(27, 29, 35);\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(33, 37, 43);\n"
"}\n"
"QPushButton:pressed {    \n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.chartButton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/24x24/cil-chart-line.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.chartButton.setIcon(icon5)
        self.chartButton.setIconSize(QtCore.QSize(24, 24))
        self.chartButton.setObjectName("chartButton")
        self.verticalLayout_4.addWidget(self.chartButton)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)
        self.nameLogoFrame = QtWidgets.QFrame(self.leftButtonsFrame)
        self.nameLogoFrame.setMinimumSize(QtCore.QSize(60, 60))
        self.nameLogoFrame.setMaximumSize(QtCore.QSize(60, 60))
        self.nameLogoFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.nameLogoFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.nameLogoFrame.setObjectName("nameLogoFrame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.nameLogoFrame)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.nameLabel = QtWidgets.QLabel(self.nameLogoFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nameLabel.sizePolicy().hasHeightForWidth())
        self.nameLabel.setSizePolicy(sizePolicy)
        self.nameLabel.setMinimumSize(QtCore.QSize(40, 40))
        self.nameLabel.setMaximumSize(QtCore.QSize(40, 40))
        self.nameLabel.setStyleSheet("QLabel {\n"
"    border-radius: 20px;\n"
"    background-color: rgb(44, 49, 60);\n"
"    border: 5px solid rgb(39, 44, 54);\n"
"    background-position: center;\n"
"    background-repeat: no-repeat;\n"
"}")
        self.nameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.nameLabel.setObjectName("nameLabel")
        self.horizontalLayout_4.addWidget(self.nameLabel)
        self.verticalLayout_4.addWidget(self.nameLogoFrame)
        self.horizontalLayout.addWidget(self.leftButtonsFrame)
        self.rightFrame = QtWidgets.QFrame(self.centralwidget)
        self.rightFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.rightFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.rightFrame.setLineWidth(0)
        self.rightFrame.setObjectName("rightFrame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.rightFrame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.topBar = QtWidgets.QFrame(self.rightFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.topBar.sizePolicy().hasHeightForWidth())
        self.topBar.setSizePolicy(sizePolicy)
        self.topBar.setMinimumSize(QtCore.QSize(0, 50))
        self.topBar.setMaximumSize(QtCore.QSize(16777215, 60))
        self.topBar.setStyleSheet("background: transparent;")
        self.topBar.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.topBar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.topBar.setLineWidth(0)
        self.topBar.setObjectName("topBar")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.topBar)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.headBar = QtWidgets.QFrame(self.topBar)
        self.headBar.setMinimumSize(QtCore.QSize(0, 30))
        self.headBar.setMaximumSize(QtCore.QSize(16777215, 30))
        self.headBar.setStyleSheet("background-color: rgba(27, 29, 35,200);\n"
"")
        self.headBar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.headBar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.headBar.setObjectName("headBar")
        self.verticalLayout_2.addWidget(self.headBar)
        self.notificationBar = QtWidgets.QFrame(self.topBar)
        self.notificationBar.setMinimumSize(QtCore.QSize(0, 20))
        self.notificationBar.setMaximumSize(QtCore.QSize(16777215, 20))
        self.notificationBar.setStyleSheet("background-color: rgb(39, 44, 54);")
        self.notificationBar.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.notificationBar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.notificationBar.setObjectName("notificationBar")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.notificationBar)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.terminalImage = QtWidgets.QFrame(self.notificationBar)
        self.terminalImage.setMinimumSize(QtCore.QSize(16, 16))
        self.terminalImage.setMaximumSize(QtCore.QSize(16, 16))
        self.terminalImage.setStyleSheet("image: url(:/icons/16x16/cil-terminal.png);")
        self.terminalImage.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.terminalImage.setFrameShadow(QtWidgets.QFrame.Raised)
        self.terminalImage.setObjectName("terminalImage")
        self.horizontalLayout_3.addWidget(self.terminalImage)
        self.notificationLabel = QtWidgets.QLabel(self.notificationBar)
        self.notificationLabel.setStyleSheet("color: rgb(98, 103, 111);")
        self.notificationLabel.setObjectName("notificationLabel")
        self.horizontalLayout_3.addWidget(self.notificationLabel)
        self.verticalLayout_2.addWidget(self.notificationBar)
        self.verticalLayout.addWidget(self.topBar)
        self.centerFrame = QtWidgets.QFrame(self.rightFrame)
        self.centerFrame.setStyleSheet("background-color: rgb(44, 49, 60);")
        self.centerFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.centerFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.centerFrame.setObjectName("centerFrame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.centerFrame)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.mainStackedWidget = QtWidgets.QStackedWidget(self.centerFrame)
        self.mainStackedWidget.setObjectName("mainStackedWidget")
        self.homePage = QtWidgets.QWidget()
        self.homePage.setObjectName("homePage")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.homePage)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.frame = QtWidgets.QFrame(self.homePage)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(33)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label)
        self.horizontalLayout_6.addWidget(self.frame)
        self.mainStackedWidget.addWidget(self.homePage)
        self.videoPage = QtWidgets.QWidget()
        self.videoPage.setObjectName("videoPage")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.videoPage)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(2)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.frame_2 = QtWidgets.QFrame(self.videoPage)
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(10)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.rgbImage = QtWidgets.QLabel(self.frame_2)
        self.rgbImage.setMinimumSize(QtCore.QSize(640, 480))
        self.rgbImage.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(33)
        self.rgbImage.setFont(font)
        self.rgbImage.setScaledContents(True)
        self.rgbImage.setAlignment(QtCore.Qt.AlignCenter)
        self.rgbImage.setObjectName("rgbImage")
        self.verticalLayout_6.addWidget(self.rgbImage)
        self.depthImage = QtWidgets.QLabel(self.frame_2)
        self.depthImage.setMinimumSize(QtCore.QSize(640, 480))
        self.depthImage.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setPointSize(33)
        self.depthImage.setFont(font)
        self.depthImage.setScaledContents(True)
        self.depthImage.setAlignment(QtCore.Qt.AlignCenter)
        self.depthImage.setObjectName("depthImage")
        self.verticalLayout_6.addWidget(self.depthImage)
        self.horizontalLayout_7.addWidget(self.frame_2)
        self.mainStackedWidget.addWidget(self.videoPage)
        self.pointCloudPage = QtWidgets.QWidget()
        self.pointCloudPage.setObjectName("pointCloudPage")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.pointCloudPage)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.mainStackedWidget.addWidget(self.pointCloudPage)
        self.camera3dPage = QtWidgets.QWidget()
        self.camera3dPage.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.camera3dPage.setObjectName("camera3dPage")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.camera3dPage)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.frame_3 = QtWidgets.QFrame(self.camera3dPage)
        self.frame_3.setMaximumSize(QtCore.QSize(200, 16777215))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.renderModeledCheckBox = QtWidgets.QCheckBox(self.frame_3)
        self.renderModeledCheckBox.setObjectName("renderModeledCheckBox")
        self.verticalLayout_5.addWidget(self.renderModeledCheckBox)
        self.renderGroundTruthCheckBox = QtWidgets.QCheckBox(self.frame_3)
        self.renderGroundTruthCheckBox.setObjectName("renderGroundTruthCheckBox")
        self.verticalLayout_5.addWidget(self.renderGroundTruthCheckBox)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem2)
        self.horizontalLayout_9.addWidget(self.frame_3)
        self.cameraRenderPlace = QtWidgets.QFrame(self.camera3dPage)
        self.cameraRenderPlace.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.cameraRenderPlace.setFrameShadow(QtWidgets.QFrame.Raised)
        self.cameraRenderPlace.setObjectName("cameraRenderPlace")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.cameraRenderPlace)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_9.addWidget(self.cameraRenderPlace)
        self.mainStackedWidget.addWidget(self.camera3dPage)
        self.chartPage = QtWidgets.QWidget()
        self.chartPage.setObjectName("chartPage")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.chartPage)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.frame_4 = QtWidgets.QFrame(self.chartPage)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.chart1Frame = QtWidgets.QFrame(self.frame_4)
        self.chart1Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.chart1Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.chart1Frame.setObjectName("chart1Frame")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.chart1Frame)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_2 = QtWidgets.QLabel(self.chart1Frame)
        font = QtGui.QFont()
        font.setPointSize(33)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_9.addWidget(self.label_2)
        self.horizontalLayout_10.addWidget(self.chart1Frame)
        self.chart2Frame = QtWidgets.QFrame(self.frame_4)
        self.chart2Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.chart2Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.chart2Frame.setObjectName("chart2Frame")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.chart2Frame)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_3 = QtWidgets.QLabel(self.chart2Frame)
        font = QtGui.QFont()
        font.setPointSize(33)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_10.addWidget(self.label_3)
        self.horizontalLayout_10.addWidget(self.chart2Frame)
        self.verticalLayout_8.addWidget(self.frame_4)
        self.frame_5 = QtWidgets.QFrame(self.chartPage)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.chart3Frame = QtWidgets.QFrame(self.frame_5)
        self.chart3Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.chart3Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.chart3Frame.setObjectName("chart3Frame")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.chart3Frame)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_4 = QtWidgets.QLabel(self.chart3Frame)
        font = QtGui.QFont()
        font.setPointSize(33)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_11.addWidget(self.label_4)
        self.horizontalLayout_11.addWidget(self.chart3Frame)
        self.chart4Frame = QtWidgets.QFrame(self.frame_5)
        self.chart4Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.chart4Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.chart4Frame.setObjectName("chart4Frame")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.chart4Frame)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.label_5 = QtWidgets.QLabel(self.chart4Frame)
        font = QtGui.QFont()
        font.setPointSize(33)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_12.addWidget(self.label_5)
        self.horizontalLayout_11.addWidget(self.chart4Frame)
        self.verticalLayout_8.addWidget(self.frame_5)
        self.mainStackedWidget.addWidget(self.chartPage)
        self.verticalLayout_3.addWidget(self.mainStackedWidget)
        self.informationBar = QtWidgets.QFrame(self.centerFrame)
        self.informationBar.setMinimumSize(QtCore.QSize(0, 20))
        self.informationBar.setMaximumSize(QtCore.QSize(16777215, 20))
        self.informationBar.setStyleSheet("background-color: rgba(27, 29, 35,200);\n"
"")
        self.informationBar.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.informationBar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.informationBar.setObjectName("informationBar")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.informationBar)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.informationLabel = QtWidgets.QLabel(self.informationBar)
        self.informationLabel.setStyleSheet("color: rgb(98, 103, 111);")
        self.informationLabel.setObjectName("informationLabel")
        self.horizontalLayout_2.addWidget(self.informationLabel)
        self.versionLabel = QtWidgets.QLabel(self.informationBar)
        self.versionLabel.setMinimumSize(QtCore.QSize(40, 0))
        self.versionLabel.setMaximumSize(QtCore.QSize(40, 16777215))
        self.versionLabel.setStyleSheet("color: rgb(98, 103, 111);")
        self.versionLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.versionLabel.setObjectName("versionLabel")
        self.horizontalLayout_2.addWidget(self.versionLabel)
        self.frame_6 = QtWidgets.QFrame(self.informationBar)
        self.frame_6.setMinimumSize(QtCore.QSize(20, 0))
        self.frame_6.setMaximumSize(QtCore.QSize(20, 16777215))
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_2.addWidget(self.frame_6)
        self.verticalLayout_3.addWidget(self.informationBar)
        self.verticalLayout.addWidget(self.centerFrame)
        self.horizontalLayout.addWidget(self.rightFrame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.nameLabel.setText(_translate("MainWindow", "SH"))
        self.notificationLabel.setText(_translate("MainWindow", "No dataset loaded in yet."))
        self.label.setText(_translate("MainWindow", "Home Page"))
        self.rgbImage.setText(_translate("MainWindow", "RGB Image (disabled in constants.py)"))
        self.depthImage.setText(_translate("MainWindow", "Depth Image (disabled in constants.py)"))
        self.renderModeledCheckBox.setText(_translate("MainWindow", "Render Modeled"))
        self.renderGroundTruthCheckBox.setText(_translate("MainWindow", "Render Ground Truth"))
        self.label_2.setText(_translate("MainWindow", "Chart 1"))
        self.label_3.setText(_translate("MainWindow", "Chart 2"))
        self.label_4.setText(_translate("MainWindow", "Chart 3"))
        self.label_5.setText(_translate("MainWindow", "Chart 4"))
        self.informationLabel.setText(_translate("MainWindow", "  SLAM - Simen van Herpt"))
        self.versionLabel.setText(_translate("MainWindow", "v1.0.0"))
import qtresources_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
