from src.metrics.metrics import Metrics
from PyQt5.QtChart import QChart, QChartView, QLineSeries
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

    def setPosErrorChart(self, selectedTimestamps):
        allDistances = Metrics.getPosErrorPerStep(
            self.data, selectedTimestamps)

        self.posErrorline.set_data(allDistances)
        self.posErrorChart.vb.camera.set_range(
            (0, len(selectedTimestamps), (0, 1)))

    def setVelocityChart(self, selectedTimestamps):
        modelVel, trueVel = Metrics.getVelocityPerStep(
            self.data, selectedTimestamps)

        self.modelVelline.set_data(modelVel)
        self.trueVelline.set_data(trueVel)
        self.velocityChart.vb.camera.set_range(
            (0, len(selectedTimestamps), (0, 1)))

    def setKeyMatchAmountChart(self, selectedTimestamps):
        keypointAmounts = Metrics.getKeyMatchAmountPerStep(
            self.data, selectedTimestamps)

        self.keyAmountline.set_data(keypointAmounts)
        self.keyAmountChart.vb.camera.set_range(
            (0, len(selectedTimestamps), (0, 1)))

    def setRotErrorChart(self, selectedTimestamps):
        allRotErrors = Metrics.getRotationErrorPerStep(
            self.data, selectedTimestamps)
        self.rotErrorline.set_data(allRotErrors)
        self.rotErrorChart.vb.camera.set_range(
            (0, len(selectedTimestamps), (0, 1)))

    def getMetrics(self):
        selectedTimestamps = self.data.timestamps[self.ui.start: self.ui.end]
        self.setPosErrorChart(selectedTimestamps)
        self.setVelocityChart(selectedTimestamps)
        self.setKeyMatchAmountChart(selectedTimestamps)
        self.setRotErrorChart(selectedTimestamps)

    def setSceneVisualsData(self, newSelect=False):
        amount = self.ui.end - self.ui.start
        if amount <= 1:
            return

        self.getMetrics()


class CustomPlot(scene.SceneCanvas):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.unfreeze()
        self.grid = self.central_widget.add_grid(spacing=0)
        self.vb = self.grid.add_view(row=0, col=1, camera='panzoom')

        self.x_axis = scene.AxisWidget(
            orientation='bottom', axis_color=(98/255, 103/255, 111/255))
        self.x_axis.stretch = (1, 0.1)
        self.grid.add_widget(self.x_axis, row=1, col=1)
        self.x_axis.link_view(self.vb)

        self.y_axis = scene.AxisWidget(
            orientation='left', axis_color=(98/255, 103/255, 111/255))
        self.y_axis.stretch = (0.1, 1)
        self.grid.add_widget(self.y_axis, row=0, col=0)
        self.y_axis.link_view(self.vb)
