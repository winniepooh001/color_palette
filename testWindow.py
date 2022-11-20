from PySide6.QtWidgets import (QGridLayout, QWidget, QLabel, QTableWidget, QTableWidgetItem,
                               QPushButton, QSpinBox, QLineEdit, QMenu, QHeaderView, QStatusBar, QSizePolicy,
                               QVBoxLayout, QFrame)
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt
from pathlib import Path
import os
from customWidgets.titleBar import title_bar
from customWidgets.divider import sectionDivider
from customWidgets.labeledCombo import labelleedCombo

file_directory = os.getcwd()

class testWindow(QWidget):
    def __init__(self):
        super().__init__()
        # testing color scheme and font
        self.oldPos = None
        self.setLayout(QVBoxLayout())
        self.setWindowTitle("SAMPLE VIEW")
        
        self.title = title_bar(self, title="title bar")
        self.setWindowFlag(Qt.FramelessWindowHint)


        self.layout().addWidget(self.title)
        
        mainView = QFrame()
        mainView.setLayout(QGridLayout())
        self.layout().addWidget(mainView)
        self.layout().setContentsMargins(1,0,1,0)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenuEvent)

        self.widgets = {
            'QLabel: label': QLabel(),
            'QLabel: hyperlink': QLabel(),
            'QButton: flat': QPushButton(flat=True),
            'QButton: not_flat': QPushButton(),
            'QButton: icon': QPushButton(icon=QIcon(f'{file_directory}\\images\\icons\\clear.png')),
            'QButton: disabled': QPushButton(),
            'QLineEdit: lineEdit': QLineEdit(),
            'QTableView: table': QTableWidget(),
            'labelledCombo: combo': labelleedCombo(title="combo with label", items=['empty','list'])
        }

        separater = sectionDivider('vertical', objectName="divider")
        separater.setMinimumHeight(2)
        col_idx = 0
        num_col = 4
        row_idx = 0
        table_rows = 4
        num_item = 0
        for label, item in self.widgets.items():
            num_item += 1
            item.setToolTip(label)
            item.setToolTipDuration(50000)
            objName = label.split(":")[1].strip()
            item.setObjectName(objName)
            if 'QLabel' in label:
                item.setText(objName)
                if 'hyperlink' in label:
                    item.setOpenExternalLinks(True)
                    linkTemplate = '<a href={0}>{1}</a>'.format('www.google.com', label)
                    item.setText(linkTemplate)
                else:
                    item.setText(objName)
                mainView.layout().addWidget(item, row_idx, col_idx, 1, 2)
                col_idx += 2
            elif 'QButton' in label:
                if row_idx == 0:
                    col_idx = 0
                    row_idx += 1
                item.setText(objName)
                if 'disabled' in label:
                    item.setDisabled(True)

                item.clicked.connect(self.update_status)
                mainView.layout().addWidget(item, row_idx, col_idx, 1, 1)
                col_idx += 1
            elif 'QLine' in label or 'Combo' in label:
                pos = mainView.layout().getItemPosition(num_item-2)
                item.setPlaceholderText(objName)
                row_idx = pos[0] + 2 + pos[3]
                print(row_idx)
                mainView.layout().addWidget(item, row_idx, 0, 1, num_col)
            elif 'Table' in label:
                row_idx += table_rows + 1
                item.setRowCount(table_rows)
                item.rowSpan(4,4)
                item.setColumnCount(num_col)
                item.horizontalHeader().setVisible(True)
                item.verticalHeader().setVisible(True)
                for i in range(4):
                    for j in range(num_col):
                        base_text = f"({i+1}, {j+1})"
                        item.setItem(i, j, QTableWidgetItem(base_text))
                        if j == 0:
                            item.item(i,j).setText(f"{base_text} not selectable")
                            item.item(i, j).setFlags(~Qt.ItemFlag.ItemIsSelectable)
                        elif j == 1:
                            item.item(i, j).setText(f"{base_text} not editable")
                            item.item(i, j).setFlags(~Qt.ItemFlag.ItemIsEditable)
                        elif j == 2:
                            item.item(i, j).setText(f"{base_text} word wrap" + "="*10)
                            item.item(i,j).setStatusTip(f"{label} at {base_text}")

                item.resizeRowsToContents()
                item.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                item.setAlternatingRowColors(True)
                mainView.layout().addWidget(item, row_idx, 0, 4, num_col)




        self.layout().addWidget(separater)
        self.status_bar = QStatusBar(objectName='StatusBar')
        self.status_bar.showMessage("this is the status", 5000)
        self.layout().addWidget(self.status_bar)

    def update_status(self):

        self.status_bar.showMessage(self.sender().objectName() + " is clicked", 2000)

    def contextMenuEvent(self, event) -> None:
        # right-click on the window
        context = QMenu(self)
        self.contextActions = [QAction(f"context menu {i}", self) for i in range(3)]
        for cur_act in self.contextActions:
            cur_act.setObjectName(cur_act.text())
            cur_act.triggered.connect(self.update_status)
            context.addAction(cur_act)

        context.exec_(self.mapToGlobal(event))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.oldPos is not None:
            delta = event.globalPos() - self.oldPos
            self.move(self.pos() + delta)
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.oldPos = None
