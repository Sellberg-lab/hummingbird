"""Window to display 2D plots"""
from interface.ui import Ui_plotWindow
import pyqtgraph
import numpy
from interface.ui import DataWindow

class PlotWindow(DataWindow, Ui_plotWindow):
    """Window to display 2D plots"""
    def __init__(self, parent=None):
        DataWindow.__init__(self, parent)
        self.plot = pyqtgraph.PlotWidget(self.plotFrame, antialiasing=True)
        self.plot.hideAxis('bottom')
        self.legend = self.plot.addLegend()
        self.legend.hide()
        self.finish_layout()
        self.actionLegend_Box.triggered.connect(self.on_view_legend_box)
        self.actionX_axis.triggered.connect(self.on_view_x_axis)
        self.actionY_axis.triggered.connect(self.on_view_y_axis)
        self.acceptable_data_types = ['scalar', 'vector']
        self.exclusive_source = False
        self.line_colors = [(252, 175, 62), (114, 159, 207), (255, 255, 255),
                            (239, 41, 41), (138, 226, 52), (173, 127, 168)]

    def on_view_legend_box(self):
        """Show/hide legend box"""
        action = self.sender()
        if(action.isChecked()):
            self.legend.show()
        else:
            self.legend.hide()

    def on_view_x_axis(self):
        """Show/hide X axis"""
        action = self.sender()
        if(action.isChecked()):
            self.plot.showAxis('bottom')
        else:
            self.plot.hideAxis('bottom')

    def on_view_y_axis(self):
        """Show/hide Y axis"""
        action = self.sender()
        if(action.isChecked()):
            self.plot.showAxis('left')
        else:
            self.plot.hideAxis('left')

    def replot(self):
        """Replot data"""
        self.plot.clear()
        color_index = 0
        titlebar = []
        self.plot.plotItem.legend.items = []
        for source, title in self.source_and_titles():
            if(title not in source.plotdata or source.plotdata[title].y is None):
                continue
            pd = source.plotdata[title]
            titlebar.append(pd.title)

            color = self.line_colors[color_index % len(self.line_colors)]
            pen = None
            symbol = None
            symbol_pen = None
            symbol_brush = None
            if(self.actionLines.isChecked()):
                pen = color
            if(self.actionPoints.isChecked()):
                symbol = 'o'
                symbol_pen = color
                symbol_brush = color

            conf = source.conf[title]
            if(self.actionX_axis.isChecked()):
                if 'xlabel' in conf:
                    self.plot.setLabel('bottom', conf['xlabel'])
            if(self.actionY_axis.isChecked()):
                if 'ylabel' in conf:
                    self.plot.setLabel('left', conf['ylabel'])

            if(source.data_type[title] == 'scalar'):
                y = numpy.array(pd.y, copy=False)
            elif(source.data_type[title] == 'vector'):
                y = numpy.array(pd.y[-1, :], copy=False)

            x = None
            if(source.data_type[title] == 'scalar'):
                x = numpy.array(pd.x, copy=False)

            plt = self.plot.plot(x=x, y=y, clear=False, pen=pen, symbol=symbol,
                                 symbolPen=symbol_pen, symbolBrush=symbol_brush, symbolSize=3)

            self.legend.addItem(plt, pd.title)
            color_index += 1
        self.setWindowTitle(", ".join(titlebar))
        dt = self.get_time()
        # Round to miliseconds
        self.timeLabel.setText('%02d:%02d:%02d.%03d' % (dt.hour, dt.minute, dt.second, dt.microsecond/1000))
        self.dateLabel.setText(str(dt.date()))
