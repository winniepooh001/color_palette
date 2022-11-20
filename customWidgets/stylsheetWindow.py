from PySide6.QtWidgets import (QWidget, QPlainTextEdit, QVBoxLayout,
							    QFrame, QSpinBox,QLabel,  QPushButton, QGridLayout,
							QFontComboBox, QHBoxLayout, QScrollArea, QStatusBar,
                            QTableWidget, QHeaderView
							   )
from PySide6.QtCore import QSize
from colour import Color
from customWidgets.divider import sectionDivider
from customWidgets.flowLayout import FlowLayout

class styleEditor(QWidget):
    def __init__(self, placeholder=None, color_list=None):
        super().__init__()
        self.setMinimumSize(QSize(600,300))

        self.editor = QPlainTextEdit()
        self.editor.setPlaceholderText(placeholder)
        self.default = QPlainTextEdit()
        self.default.setStyleSheet("background-color: gray; color: white;")
        self.default.setReadOnly(True)
        style_editor = QFrame()
        style_editor.setLayout(QGridLayout())
        style_editor.layout().addWidget(QLabel(text="default stylesheet"), 0, 0, 1, 1)
        style_editor.layout().addWidget(QLabel(text="custom stylesheet"), 0, 1, 1, 1)
        style_editor.layout().addWidget(self.default, 1, 0, 3, 1)
        style_editor.layout().addWidget(self.editor,1, 1, 3, 1)
        self.editor.setToolTip("Use '{{' and '}}' when there is named tuple otherwise '{' '}'")
        self.editor.setToolTipDuration(50000)
        action_btns = QFrame()
        action_btns.setLayout(QHBoxLayout())
        self.apply_btn = QPushButton(text="Apply Style")
        self.save_btn = QPushButton(text="Save Style")
        action_btns.layout().addWidget(self.apply_btn)
        action_btns.layout().addWidget(self.save_btn)

        layout = QVBoxLayout()
        warn_label = QLabel("!Style will Overwrite Palette")
        warn_label.setStyleSheet("font: 800 15px; color: red;")
        layout.addWidget(warn_label, stretch=2)
        layout.addWidget(style_editor)
        layout.addWidget(action_btns)
        # font area
        layout.addWidget(sectionDivider("vertical"))
        font_area = QFrame()
        font_area.setLayout(QHBoxLayout())
        self.font_display = QLabel(text="font display")
        self.font_selector = QFontComboBox(objectName="font_combo")
        self.font_size = QSpinBox()
        self.font_size.setRange(1, 50)
        self.font_size.setValue(10)
        font_area.layout().addWidget(self.font_display, stretch=2)
        font_area.layout().addWidget(self.font_selector, stretch=3)
        font_area.layout().addWidget(self.font_size, stretch=1)
        layout.addWidget(font_area, stretch=2)

        self.font_selector.currentFontChanged.connect(self.update_font)
        self.font_size.valueChanged.connect(self.update_font)

        # color area
        layout.addWidget(QLabel(text="Palette Colors"))
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.colorView = QWidget()
        self.scroll.setWidget(self.colorView)
        self.colorViewLayout = FlowLayout(self.colorView)
        layout.addWidget(self.scroll)
        if color_list is not None:
            self.setColor(color_list)

        # named variable
        layout.addWidget(QLabel(text="Named Tuple for StyleSheet"))
        self.cur_table = QTableWidget()
        self.cur_table.setColumnCount(2)
        self.cur_table.horizontalHeader().setVisible(True)
        header = self.cur_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        self.cur_table.setHorizontalHeaderLabels(["name", "definition"])
        self.cur_table.verticalHeader().setVisible(True)
        self.cur_table.setRowCount(1)

        addButton = QPushButton(text="+")
        removeButton = QPushButton(text="-")
        button_layout = QFrame()
        button_layout.setLayout(QHBoxLayout())
        button_layout.layout().addWidget(addButton)
        button_layout.layout().addWidget(removeButton)
        addButton.clicked.connect(self.table_add)
        removeButton.clicked.connect(self.table_delete)

        layout.addWidget(self.cur_table)
        layout.addWidget(button_layout)

        cur_status = QStatusBar(objectName='StatusBar')
        cur_status.showMessage("real time change to screen")
        layout.addWidget(cur_status)
        self.setLayout(layout)
        # self.setWindowFlag(Qt.FramelessWindowHint)
        # need to add title bar if go to frameless

    def table_add(self):
        rowCount = self.cur_table.rowCount()
        self.cur_table.insertRow(rowCount)

    def table_delete(self):
        if self.cur_table.rowCount() > 1:
            self.cur_table.removeRow(self.cur_table.rowCount()-1)

    def get_table_value(self):
        row_count = self.cur_table.rowCount()
        named_tuples = {}
        for i in range(row_count):
            key_ = self.cur_table.item(i, 0)
            if key_ is None or key_.text() == "":
                return named_tuples
            elif self.cur_table.item(i, 1) is None:
                return named_tuples
            else:
                named_tuples[key_.text()] = self.cur_table.item(i,1).text()
        return named_tuples


    def update_font(self):
        self.font_display.setStyleSheet('font: {0}px "{1}"'.format(self.font_size.value(), self.font_selector.currentText()))

    def init_default_style(self, file):
        with open(file, 'r') as fh:
            self.default.setPlainText(fh.read())

    def setColor(self, color_list):
        num_colors = self.colorViewLayout.count()
        min_count = min(num_colors, len(color_list))
        for i in range(min_count):
            cur_lbl = self.colorViewLayout.itemAt(i).widget()
            cur_lbl.setText(color_list[i])
            cur_col = Color(color_list[i])
            text_color = "white" if (sum(cur_col.rgb) / 3) < 0.5 else "black"
            cur_lbl.setStyleSheet(f"border: 1px solid black; background-color: {color_list[i]}; color: {text_color}")

        # delete
        if num_colors > len(color_list):
            for i in range(min_count, num_colors):
                self.colorViewLayout.itemAt(i).deleteLater()

        elif num_colors < len(color_list):
            for i in range(min_count, len(color_list)):
                cur_lbl = QLabel(text=color_list[i])
                cur_col = Color(color_list[i])
                text_color = "white" if (sum(cur_col.rgb) / 3) < 0.5 else "black"
                cur_lbl.setStyleSheet(f"border: 1px solid black; background-color: {color_list[i]}; color: {text_color};")
                self.colorViewLayout.addWidget(cur_lbl)