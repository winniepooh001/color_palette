from PySide6.QtWidgets import QDialog,  QDialogButtonBox, QVBoxLayout, QLabel


class informationDialogue(QDialog):
    def __init__(self, title, msg):
        super().__init__()
        self.setWindowTitle(title)

        QBtn = QDialogButtonBox.Ok
        buttonBox = QDialogButtonBox(QBtn)

        buttonBox.accepted.connect(self.close)
        layout = QVBoxLayout()
        self.write_key = QLabel(text=msg)
        layout.addWidget(self.write_key)
        layout.addWidget(buttonBox)
        self.setLayout(layout)
