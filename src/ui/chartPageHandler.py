from src.metrics.metrics import Metrics
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from vispy import scene
import numpy as np


class ChartPageHandler():
    def __init__(self, ui, dataObject):
        self.ui = ui
        self.data = dataObject
        self.createCharts()

    # Create all the charts, not really worth simplifying this function
    def createCharts(self):
        bgColor = (28 / 255, 31 / 255, 36 / 255)

        self.posErrorChart = CustomPlot(bgcolor=bgColor)
        self.rotErrorChart = CustomPlot(bgcolor=bgColor)
        self.keyAmountChart = CustomPlot(bgcolor=bgColor)
        self.velocityChart = CustomPlot(bgcolor=bgColor)

        lineColor1 = (171 / 255, 0 / 255, 46 / 255)
        lineColor2 = (46 / 255, 0 / 255, 171 / 255)
        lineWidth = 3
        self.posErrorline = scene.Line(
            None, lineColor1, width=lineWidth, parent=self.posErrorChart.vb.scene)
        self.rotErrorline = scene.Line(
            None, lineColor1, width=lineWidth, parent=self.rotErrorChart.vb.scene)
        self.keyAmountline = scene.Line(
            None, lineColor1, width=lineWidth, parent=self.keyAmountChart.vb.scene)
        self.trueVelline = scene.Line(
            None, lineColor1, width=lineWidth, parent=self.velocityChart.vb.scene)
        self.modelVelline = scene.Line(
            None, lineColor2, width=lineWidth, parent=self.velocityChart.vb.scene)

        self.ui.chart1Frame.layout().addWidget(self.posErrorChart.native)
        self.ui.chart2Frame.layout().addWidget(self.rotErrorChart.native)
        self.ui.chart3Frame.layout().addWidget(self.velocityChart.native)
        self.ui.chart4Frame.layout().addWidget(self.keyAmountChart.native)

        # Get the metrics data
        self.getMetrics()

    # Position error
    def updatePosErrorChart(self):
        selDistances = self.posError[self.ui.start: self.ui.end]

        self.posErrorline.set_data(selDistances)
        self.posErrorChart.vb.camera.set_range(
            (0, len(selDistances), (0, 1)))

    # Velocities per stamps
    def updateVelocityChart(self):
        selModelVel = self.modelVel[self.ui.start: self.ui.end]
        selTrueVel = self.trueVel[self.ui.start: self.ui.end]

        self.modelVelline.set_data(selModelVel)
        self.trueVelline.set_data(selTrueVel)
        self.velocityChart.vb.camera.set_range(
            (0, len(selTrueVel), (0, 1)))

    # Number of keypoints
    def updateKeyPointAmountChart(self):
        selKPAmount = self.keypointAmounts[self.ui.start: self.ui.end]

        self.keyAmountline.set_data(selKPAmount)
        self.keyAmountChart.vb.camera.set_range(
            (0, len(selKPAmount), (0, 1)))

    # Rotation error
    def updateRotErrorChart(self):
        selRotErrors = self.rotErrors[self.ui.start: self.ui.end]
        self.rotErrorline.set_data(selRotErrors)
        self.rotErrorChart.vb.camera.set_range(
            (0, len(selRotErrors), (0, 1)))

    # Get all the metrics
    def getMetrics(self):
        self.posError = Metrics.getPosErrorPerStep(
            self.data)
        self.modelVel, self.trueVel = Metrics.getVelocityPerStep(
            self.data)
        self.keypointAmounts = Metrics.getKeyPointAmountPerStep(
            self.data)
        self.rotErrors = Metrics.getRotationErrorPerStep(
            self.data)

    def updateCharts(self):
        self.updatePosErrorChart()
        self.updateVelocityChart()
        self.updateKeyPointAmountChart()
        self.updateRotErrorChart()

    # Connection point from the main screen
    def setSceneVisualsData(self, newSelect=False):
        amount = self.ui.end - self.ui.start
        if amount <= 1:
            return

        self.updateCharts()


class CustomPlot(scene.SceneCanvas):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.unfreeze()
        self.grid = self.central_widget.add_grid(spacing=0)
        self.vb = self.grid.add_view(row=0, col=1, camera='panzoom')

        axisColor = (98 / 255, 103 / 255, 111 / 255)
        self.x_axis = scene.AxisWidget(
            orientation='bottom', axis_color=axisColor)
        self.x_axis.stretch = (1, 0.1)
        self.grid.add_widget(self.x_axis, row=1, col=1)
        self.x_axis.link_view(self.vb)

        self.y_axis = scene.AxisWidget(
            orientation='left', axis_color=axisColor)
        self.y_axis.stretch = (0.1, 1)
        self.grid.add_widget(self.y_axis, row=0, col=0)
        self.y_axis.link_view(self.vb)
