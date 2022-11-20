### this is testing and learning

import sys
from functools import partial

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit, QDialog, QDialogButtonBox,
                               QMainWindow, QFrame, QGridLayout, QMenu, QPushButton, QVBoxLayout, QSpinBox,
                               QWidget, QPlainTextEdit, QCheckBox, QComboBox,
                               QScrollArea, QStatusBar, QSizePolicy)
import json
from resource import resources, themeApply
from customWidgets.colorPicker import ColorButton
from customWidgets.titleBar import title_bar
from testWindow import testWindow
from customWidgets.labeledCombo import labelleedCombo
from customWidgets.collapsibleWidget import CollapsibleBox
from customWidgets.exportDialog import exportDialog
from customWidgets.divider import sectionDivider
from customWidgets.stylsheetWindow import styleEditor
from customWidgets.informationDialogue import informationDialogue

class MainWindow(QMainWindow):
    def __init__(self, window_title):
        super().__init__()
        self.resource_files = resources.LayoutSettings
        self.cur_theme = 'default'

        with open(self.resource_files['theme_file'], mode="r") as fh:
            allthemes = json.load(fh)
        self.theme_list = list(allthemes.keys())
        self.themes = self.default_theme = allthemes[self.cur_theme]

        with open(self.resource_files['setting_file'], mode="r") as fh:
            self.settings = json.load(fh)

        with open(self.resource_files["style_sheet"], mode="r") as fh:
            self.default_style = fh.read()

        with open(self.resource_files['style_sheet_variables'], mode='r') as fh:
            self.style_parameter = json.load(fh)['default']

        # remove default title bar
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.oldPos = None

        self.status_bar = QStatusBar(objectName='StatusBar')
        self.status_bar.showMessage("this is the status", 5000)


        # setup
        self.container = QWidget()
        self.setCentralWidget(self.container)

        self.frameLayout = QVBoxLayout()
        self.container.setLayout(self.frameLayout)

        self.title_bar = title_bar(self, title="THEME BUILDER")
        self.frameLayout.addWidget(self.title_bar)

        option_box = QFrame()
        option_box.setLayout(QHBoxLayout())
        self.themeSelector = labelleedCombo(objectName='themeSelector', title="Base Theme")
        self.themeSelector.setPlaceholderText("Chose an Existing Theme")
        option_box.layout().addWidget(self.themeSelector, stretch=5)
        option_box.layout().setContentsMargins(0,0,0,0)
        option_box.layout().addStretch(3)
        divider = sectionDivider()
        option_box.layout().addWidget(divider)
        self.auto_style_from_color = QPushButton(text="Autofill Pallette from Colors")
        option_box.layout().addWidget(self.auto_style_from_color, stretch=2)
        option_box.layout().addStretch(1)
        self.base_color = []
        self.base_color_defn = {'Window': 'Active_Window', 'Text': 'Active_Text', 'Alternate':'Active_HighlightedText'}
        for objname, colorname in self.base_color_defn.items():
            cur_color = ColorButton(objectName=objname, color=self.default_theme['Palette'][colorname])

            option_box.layout().addWidget(cur_color)
            self.base_color.append(cur_color)
        option_box.layout().addStretch(3)
        self.frameLayout.addWidget(option_box)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.mainView = QWidget()
        self.scroll.setWidget(self.mainView)
        self.mainViewLayout = QHBoxLayout()
        self.mainView.setLayout(self.mainViewLayout)
        self.frameLayout.addWidget(self.scroll, stretch=5)

        self.popMenu = QMenu(self)
        self.popMenuAction = [QAction('copy across', self), QAction('copy up', self), QAction('copy down', self)]


        # Palette
        self.theme_box = CollapsibleBox('Palette')
        self.mainViewLayout.addWidget(self.theme_box)
        self.themeLayout = QGridLayout()
        for idx, state in enumerate(['Active','Disabled', 'Inactive']):
            label = QLabel(f"Group {state}")
            label.setAlignment(Qt.AlignCenter)
            self.themeLayout.addWidget(label, 0, idx + 1, 1, 1)

            for row_idx, role_name in enumerate(themeApply.color_role):
                role_text = str(role_name).split(".")[1]
                object_name = f'{state}_{role_text}'
                label = QLabel(text=role_text, objectName=role_text)
                self.themeLayout.addWidget(label, row_idx + 1, 0, 1, 1)
                color = ColorButton(color=self.default_theme['Palette'][object_name], objectName=object_name)
                self.themeLayout.addWidget(color, row_idx + 1, 1 + idx, 1, 1)
                color.setContextMenuPolicy(Qt.CustomContextMenu)
                color.customContextMenuRequested.connect(self.on_context_menu)

        self.theme_box.setContentLayout(self.themeLayout)


        # layout with label and text edit
        action_btns = QFrame()
        action_btns.setLayout(QHBoxLayout())
        self.action_buttons = {}
        for btn in ["reset", "apply", "style edit", "export", "delete"]:
            cur_btn = QPushButton(text=btn)
            self.action_buttons[btn] = cur_btn
            action_btns.layout().addWidget(cur_btn)

        self.frameLayout.addWidget(action_btns)

        self.show_sample_btn = QPushButton(text='Sample Window')
        self.show_sample_btn.clicked.connect(self.show_sample)
        self.show_sample_btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        divider = sectionDivider(direction='vertical')
        self.frameLayout.addWidget(divider)
        self.frameLayout.addWidget(self.show_sample_btn)
        # for grip and resize
        self.frameLayout.stretch(2)
        self.frameLayout.addWidget(self.status_bar)

        # custom widgets
        self.w = styleEditor()
        self.sample_display = testWindow()


        # other actions

        self.themeSelector.combo.currentIndexChanged.connect(self.pull_style)


        # set size
        self.setMinimumSize(QSize(200, 20))

        self.resize(800,500)
        self.load_data()
        self.init_btn()
        self.init_style()
        self.show()

    def show_sample(self):
        if not self.sample_display.isVisible():
            self.sample_display.show()

    def on_context_menu(self, point):
        # show context menu
        cur_widget = self.childAt(self.sender().mapTo(self, point))

        self.popMenu.exec_(cur_widget.mapToGlobal(point))

    def copy_over(self, direction=0):
        cur_widget = self.sender()
        widget_index = self.themeLayout.indexOf(cur_widget)
        row_idx, col_idx, _, _ = self.themeLayout.getItemPosition(widget_index)
        color = cur_widget.color()
        max_row = self.themeLayout.rowCount()
        if direction == 0:
            print('copy across')
            for pos in range(col_idx + 1, 4):
                self.themeLayout.itemAtPosition(row_idx, pos).widget().setColor(color)
        elif direction == 1:
            print('copy up')
            for pos in range(1, row_idx):
                self.themeLayout.itemAtPosition(pos, col_idx).widget().setColor(color)
        elif direction == 2:
            print('copy down')
            for pos in range(row_idx + 1, max_row):
                self.themeLayout.itemAtPosition(pos, col_idx).widget().setColor(color)


    def open_editor(self):
        if self.w.isVisible():
            self.w.hide()
        else:
            colorList = list(set(self.themes['Palette'].values()))
            self.w.setColor(colorList)
            self.w.init_default_style(self.resource_files['style_sheet'])
            self.w.show()
            self.show_sample()

    def extract_theme(self):
        for child in self.theme_box.findChildren(ColorButton):
            self.themes['Palette'][child.objectName()] = child.color()

    def save_theme(self):
        self.extract_theme()
        self.save_dlg = exportDialog(title="Name the Theme", file_loc=self.resource_files['theme_file'], write_dic=self.themes)
        self.save_dlg.exec()
        with open(self.resource_files['theme_file'], mode='r') as fh:
            self.theme_list = list(json.load(fh).keys())

        self.load_data()

    def load_data(self):
        self.themeSelector.combo.blockSignals(True)
        self.themeSelector.clear()
        self.themeSelector.addItems(self.theme_list)
        self.themeSelector.combo.blockSignals(False)

    def pull_style(self):
        with open(self.resource_files['theme_file'], mode="r") as fh:
            self.themes = json.load(fh)[self.themeSelector.combo.currentText()]

        self.cur_theme = self.themeSelector.combo.currentText()
        self._button_update()

    def delete_theme(self):
        if self.cur_theme == 'default':
            dlg = QDialog(self)
            dlg.setWindowTitle("Error")
            QBtn = QDialogButtonBox.Ok
            buttonBox = QDialogButtonBox(QBtn)
            buttonBox.accepted.connect(dlg.close)
            msg = QLabel(text="default cannot be deleted")
            dlg.setLayout(QVBoxLayout())
            dlg.layout().addWidget(msg)
            dlg.layout().addWidget(buttonBox)
            dlg.exec()
        else:
            with open(self.resource_files['theme_file'], mode='r') as fh:
                all_themes = json.load(fh)
                del all_themes[self.cur_theme]
                self.theme_list.remove(self.cur_theme)

            with open(self.resource_files['theme_file'], mode='w') as fh:
                json.dump(all_themes, fh, indent=4)

            self.load_data()

    def _button_update(self):
        for child in self.theme_box.findChildren(ColorButton):
            child.setColor(self.themes['Palette'][child.objectName()])
        for i, v in enumerate(['Active_Window', 'Active_Text', 'Active_HighlightedText']):
            self.base_color[i].setColor(self.themes['Palette'][v])

    def generate_palette(self):
        newTheme = themeApply.create_palette(self.base_color[0].color(), self.base_color[1].color(), self.base_color[2].color())
        self.themes['Palette'] = newTheme
        self._button_update()

    def update_palette(self):
        self.extract_theme()
        palette = themeApply.chosen_palette(self.themes['Palette'])
        # self.setPalette(palette)
        self.sample_display.setPalette(palette)
        self.sample_display.setStyleSheet("")

    def update_styles(self):
        # page 219 in Martin Fitzpack - Create Gui Applications with Python & Qt5 (2020)
        qss = self.w.editor.toPlainText()
        named_tuple = self.w.get_table_value()
        if qss != "":
            if len(named_tuple) > 0:
                self.sample_display.setStyleSheet(qss.format(**named_tuple))
            else:
                self.sample_display.setStyleSheet(qss)

    def save_style(self):
        qss = self.w.editor.toPlainText()
        named_tuple = self.w.get_table_value()
        with open(self.resource_files['custom_style_sheet'], mode='w') as fh:
            fh.write(qss)

        with open(self.resource_files['custom_style_json'], mode='w') as fh:
            json.dump(named_tuple, fh, indent=4)

        msg = "stylesheet save at\n{0}\nnamed tuple saved at\n{1}".format(self.resource_files['custom_style_sheet'],
                                                                                                   self.resource_files['custom_style_json'])
        dlg = informationDialogue(title="File overwritten", msg=msg)
        dlg.exec()

    def init_style(self):
        palette = themeApply.chosen_palette(self.default_theme['Palette'])
        self.setPalette(palette)
        self.setStyleSheet(self.default_style.format(**self.style_parameter))
        self._button_update()



        # self.title_label.setStyleSheet('font: {0}pt;'.format(self.settings["font"]["title_size"]))


    def init_btn(self):

        self.action_buttons['style edit'].clicked.connect(self.open_editor)
        self.action_buttons['reset'].clicked.connect(self.init_style)
        self.action_buttons['apply'].clicked.connect(self.update_palette)
        self.action_buttons['export'].clicked.connect(self.save_theme)
        self.action_buttons['delete'].clicked.connect(self.delete_theme)
        for i, cur_act in enumerate(self.popMenuAction):
            self.popMenu.addAction(cur_act)
            cur_act.triggered.connect(partial(self.copy_over, i))

        self.auto_style_from_color.clicked.connect(self.generate_palette)
        self.w.apply_btn.clicked.connect(self.update_styles)
        self.w.save_btn.clicked.connect(self.save_style)

    def closeEvent(self, event):
        for window in QApplication.topLevelWidgets():
            window.close()



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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    win = MainWindow("testing")
    sys.exit(app.exec())
