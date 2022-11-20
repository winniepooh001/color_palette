from PySide6.QtWidgets import QWidget, QFrame, QGridLayout, QLabel

from PySide6.QtCore import Qt, Signal

from customWidgets.colorPicker import ColorButton
import colorsys
from resource.themeApply import rgb_to_hex

class gradientWidget(QWidget):
    def __init__(self, *args, color=None, num_gradient=3, gradient_index=2, **kwargs):
        super().__init__()
        self.setLayout(QGridLayout())
        label = kwargs['text'] if 'text' in kwargs else 'color'
        self.cur_frame_label = QLabel(text=label)
        self.layout().addWidget(self.cur_frame_label, 0, 0, 1, 4, alignment=Qt.AlignCenter)
        self.base_btn = ColorButton(*args, color=color, **kwargs)
        self.layout().addWidget(self.base_btn, 1, 0, 1, 1)

        self.btn_list = []
        self.gradient_index = gradient_index
        self.all_color = [color, color, color, color]
        for i in range(num_gradient):
            btn = QLabel()
            self.btn_list.append(btn)
            self.layout().addWidget(btn, 1, i + 1, 1, 1)
        self.base_hsv = colorsys.rgb_to_hsv(*[i / 255 for i in self.base_btn.color_rgb])
        self.set_gradient_color()
        self.base_btn.pressed.connect(self.update_gradient_color)

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:
            self.set_gradient_color()

        return super(gradientWidget, self).mousePressEvent(e)

    def update_gradient_color(self):

        self.base_hsv = colorsys.rgb_to_hsv(*self.base_btn.color_rgb)
        self.all_color[0] = self.base_btn.color()
        self.set_gradient_color()

    def get_new_color(self, hsv, index, level):
        if index == 0:
            base_ = 20/360 if hsv[index] < 0.5 else -20/360
        elif index == 1:
            base_ = 20/255 if hsv[index] < 0.5 else -20/255
        else:
            base_ = 20 if hsv[index] < 125 else -20

        new_hsv = [i for i in hsv]
        new_hsv[index] = new_hsv[index] + level * base_
        rgb = colorsys.hsv_to_rgb(*new_hsv)
        return [int(i) for i in rgb]

    def setColor(self, color):
        self.base_btn.setColor(color)
        self.update_gradient_color()

    def color(self):
        return self.all_color

    def set_gradient_color(self):

        for i, cur_btn in enumerate(self.btn_list):
            rgb = self.get_new_color(self.base_hsv, self.gradient_index, i + 1)
            self.all_color[i+1] = rgb_to_hex(*rgb)
            cur_btn.setText(self.all_color[i+1])
            cur_btn.setStyleSheet("background-color: {0}".format(self.all_color[i+1]))




