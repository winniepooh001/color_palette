from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import  Signal
from colour import Color


class ColorButton(QtWidgets.QPushButton):
    '''
    Custom Qt Widget to show a chosen color.

    Left-clicking the button shows the color-chooser, while
    right-clicking resets the color to None (no-color).
    '''

    colorChanged = Signal(object)

    def __init__(self, *args, color=None, **kwargs):
        super(ColorButton, self).__init__(*args, **kwargs)

        self._color = None
        self._default = color if color is not None else "#1b1e23"
        self.pressed.connect(self.onColorPicker)
        # Set the initial/default state.
        self.setColor(self._default)

    def setColor(self, color):
        if color != self._color:
            self._color = color
            self.colorChanged.emit(color)

        if self._color:
            color_num = Color(self._color).rgb
            text_color = "white" if (sum(color_num) / 3) < 0.5 else "black"
            self.setText(self._color)
            self.setStyleSheet("background-color: {0}; color: {1}".format(self._color, text_color))

        else:
            color_num = Color(self._default).rgb
            text_color = "white" if (sum(color_num) / 3) < 0.5 else "black"
            self.setText(self._color)
            self.setStyleSheet("background-color: {0}; color: {1}".format(self._color, text_color))



    def color(self):
        return self._color

    def onColorPicker(self):
        '''
        Show color-picker dialog to select color.

        Qt will use the native dialog by default.

        '''
        dlg = QtWidgets.QColorDialog(self)
        if self._color:
            dlg.setCurrentColor(QtGui.QColor(self._color))

        if dlg.exec_():
            self.setColor(dlg.currentColor().name())
