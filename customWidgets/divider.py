# Inspiration from PyDarkOne PyDiv

from PySide6.QtWidgets import QWidget, QHBoxLayout, QFrame

class sectionDivider(QWidget):
    def __init__(self, direction="horizontal", objectName=""):
        super().__init__(objectName=objectName)

        self.layout = QHBoxLayout(self)
        self.frame_line = QFrame()
        self.layout.addWidget(self.frame_line)

        if direction == "horizontal":
            self.layout.setContentsMargins(0,5,0,5)
            self.frame_line.setMaximumWidth(1)
            self.frame_line.setMinimumWidth(1)
        else:
            self.layout.setContentsMargins(5,0,5,0)
            self.frame_line.setMaximumHeight(1)
            self.frame_line.setMinimumHeight(1)


        # self.frame_line.setStyleSheet(f"background: {color};")


