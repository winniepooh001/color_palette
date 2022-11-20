from PySide6.QtWidgets import QLabel, QComboBox, QWidget, QStyle, QVBoxLayout, QHBoxLayout, QStyleOption
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt
class labelleedCombo(QWidget):
    def __init__(self, direction="horizontal", ratio=4, title="Combo Label", objectName=None, items=None):
        super().__init__(objectName=objectName)

        self.label = QLabel(text=title)
        self.combo = QComboBox()

        if direction == "vertical":
            layout = QVBoxLayout()
            layout.addWidget(self.label,  alignment=Qt.AlignCenter)
            layout.addWidget(self.combo, )
        else:
            layout = QHBoxLayout()
            layout.addWidget(self.label, stretch=1, alignment=Qt.AlignCenter)
            layout.addWidget(self.combo, stretch=ratio)

        self.setLayout(layout)
        if items is not None:
            self.addItems(items)


    def setPlaceholderText(self, text):
        self.combo.setPlaceholderText(text)

    def setLabel(self, label):
        self.label.setText(label)

    def clear(self):
        self.combo.clear()

    def addItems(self, item):
        if type(item) == list:
            self.combo.addItems(item)
        else:
            self.combo.addItem(text=item)

    def paintEvent(self, event):
        opt = QStyleOption()
        opt.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, p, self)