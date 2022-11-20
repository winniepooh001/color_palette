from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame, QHBoxLayout, QPushButton
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
import os
from customWidgets.divider import sectionDivider


resource_directory = os.path.dirname(os.path.abspath(__file__))
class title_bar(QWidget):
    def __init__(self, mainframe, logo_path="", title="TITLE", btn_size=20):
        super().__init__()
        self._mainframe = mainframe
        self.title_bar_layout = QHBoxLayout()
        self.title_bar_layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.title_bar_layout)

        # logo
        self.logo = QLabel(objectName="topLogo")
        logo_layout = QVBoxLayout()
        self.logo.setLayout(logo_layout)

        if os.path.exists(logo_path):
            self.setIcon(logo_path)
        else:
            self.logo.setText("LOGO")

        self.title_bar_layout.addWidget(self.logo)
        div = sectionDivider(direction="horizontal")
        self.title_bar_layout.addWidget(div)
        # title
        self.title = QLabel(objectName="windowTitle", text=title)
        alignments = Qt.AlignVCenter | Qt.AlignHCenter
        self.title.setAlignment(alignments)
        self.title_bar_layout.addWidget(self.title, stretch=5)
        self.title_bar_layout.addWidget(div)

        # buttons
        self.button_group = QFrame()
        self.button_layout = QHBoxLayout()
        self.button_layout.setContentsMargins(0,0,0,0)
        self.button_layout.setSpacing(3)
        buttons = { "minimize": "-", "maximize": '+', 'close': 'x',}
        self.title_buttons = {}
        for btn_name, btn_label in buttons.items():
            self.title_buttons[btn_name] = QPushButton(objectName=btn_name, text=btn_label)
            self.title_buttons[btn_name].setMinimumSize(QSize(20,20))
            self.title_buttons[btn_name].setMaximumSize(QSize(25,25))
            self.title_buttons[btn_name].setToolTip(btn_name)
            self.title_buttons[btn_name].setToolTipDuration(5000)
            self.button_layout.addWidget(self.title_buttons[btn_name])
        self.button_group.setLayout(self.button_layout)
        self.title_bar_layout.addWidget(self.button_group, stretch=1)

        self.setMinimumHeight(20)
        self.setMaximumHeight(50)
        # initialize action
        self.title_buttons['minimize'].clicked.connect(self.showMinimized)
        self.title_buttons['maximize'].clicked.connect(self.maximize_restore)
        self.title_buttons['close'].clicked.connect(self.close)

    def setIcon(self, logo_path):
        self.logo_svg = QSvgWidget()
        self.logo_svg.load(logo_path)
        self.logo.layout().addWidget(self.logo_svg, Qt.AlignCenter, Qt.AlignCenter)
        self.logo.setText(None)

    def close(self) -> bool:
        self._mainframe.close()

    def showMinimized(self) -> None:
        self._mainframe.showMinimized()

    def maximize_restore(self):
        if self._mainframe.isMaximized():
            self._mainframe.resize(700, 600)
        else:
            self._mainframe.showMaximized()