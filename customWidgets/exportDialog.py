from PySide6.QtWidgets import QDialog,  QDialogButtonBox, QVBoxLayout, QLineEdit, QLabel

import json

class exportDialog(QDialog):
    def __init__(self, title, file_loc, write_dic, overwrite_confirm=True):
        super().__init__()
        self.setWindowTitle(title)

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        buttonBox = QDialogButtonBox(QBtn)

        self.overwrite_popup = overwrite_confirm
        self.file_loc = file_loc
        self.write_dic = write_dic
        buttonBox.accepted.connect(self.save_verify)
        buttonBox.rejected.connect(self.close)
        layout = QVBoxLayout()
        self.write_key = QLineEdit()
        layout.addWidget(self.write_key)
        layout.addWidget(buttonBox)
        self.setLayout(layout)

    def save_verify(self):
        item_label = self.write_key.text()
        is_error = False
        error_msg = "theme name can not be empty"
        if item_label is None or item_label == "":
            is_error = True
        elif len(item_label) > 12:
            is_error = True
            error_msg = "theme name must be less than 12 characters"

        if is_error:
            dlg = QDialog(self)
            dlg.setWindowTitle("Error")
            label = QLabel(text=error_msg)
            QBtn = QDialogButtonBox.Ok
            buttonBox = QDialogButtonBox(QBtn)
            buttonBox.accepted.connect(dlg.close)
            layout = QVBoxLayout()
            layout.addWidget(label)
            layout.addWidget(buttonBox)
            dlg.setLayout(layout)
            dlg.exec_()
        else:
            with open(self.file_loc, "r") as jsonFile:
                current_file = json.load(jsonFile)
            self.write_dic['Name'] = item_label
            self.overwrite_dlg = QDialog(self)
            if item_label in current_file:

                self.overwrite_dlg.setWindowTitle("Theme Exist")
                QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
                buttonBox = QDialogButtonBox(QBtn)
                buttonBox.rejected.connect(self.overwrite_dlg.close)
                buttonBox.accepted.connect(self.save)
                label = QLabel(text=f"Existing {item_label} will be overwritten!")
                layout = QVBoxLayout()
                layout.addWidget(label)
                layout.addWidget(buttonBox)
                self.overwrite_dlg.setLayout(layout)
                if self.overwrite_dlg.exec():
                    self.overwrite_dlg.close()
            else:
                self.save()

            self.close()

    def save(self):
        with open(self.file_loc, mode="r+") as jsonFile:
            current_file = json.load(jsonFile)
            jsonFile.seek(0)
            current_file[self.write_dic['Name']] = self.write_dic
            json.dump(current_file, jsonFile, indent=4)

        if self.overwrite_dlg.isVisible():
            self.overwrite_dlg.close()

        self.close()