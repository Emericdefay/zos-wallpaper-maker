from functools import partial
import json
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QFileDialog,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QRubberBand,
    QLineEdit,
)
from PyQt5.QtGui import (
    QPixmap,
    QColor,
    QPalette,
)
from PyQt5.QtCore import (
    Qt,
    QRect,
    pyqtSignal,
)

from Presets.default_settings import load_settings, original_message


class TextFieldWidget(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.settings = load_settings()
        self.msgs = self.settings.get('MESSAGES')

        layout = QVBoxLayout(self)

        # Créez un QLineEdit et un QPushButton pour chaque message
        self.list_msg = []
        for index, msg in enumerate(self.msgs):
            h_layout = QHBoxLayout()
            line_edit = QLineEdit(self)
            line_edit.setText(msg)
            reset_button = QPushButton("Défaut", self)
            reset_button.clicked.connect(partial(self.reset_line, index))
            line_edit.textChanged.connect(partial(self.check_text, line_edit))
            h_layout.addWidget(line_edit)
            h_layout.addWidget(reset_button)
            layout.addLayout(h_layout)
            self.list_msg.append(line_edit)

        # Ajoutez un bouton "Enregistrer" pour enregistrer les modifications dans le fichier JSON
        save_button = QPushButton("Enregistrer", self)
        save_button.clicked.connect(self.save_changes)
        layout.addWidget(save_button)

    def save_changes(self):
        # Récupérez les nouvelles valeurs de chaque QLineEdit et enregistrez-les dans le fichier JSON
        for i, msg in enumerate(self.list_msg):
            self.msgs[i] = msg.text()
            self.settings.get('MESSAGES')[i] = msg.text()
        # Écrivez les modifications dans le fichier JSON
        with open("settings.json", "w") as f:
            json.dump(self.settings, f)

    def reset_line(self, index):
        print(index, self.msgs[index], original_message(index))
        self.msgs[index] = original_message(index)
        self.list_msg[index].setText(original_message(index))

    def check_text(self, line_edit):
        text = line_edit.text()
        if len(text) > 49 or '"' in text:
            line_edit.setStyleSheet("background-color: #f22c3d")
        else:
            line_edit.setStyleSheet("")