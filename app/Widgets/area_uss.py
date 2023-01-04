from functools import partial
import json
import numpy as np
from PIL import (
    Image,
)
from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QFileDialog,
    QGridLayout,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QColorDialog,
    QSizePolicy,
    QLineEdit,
)
from PyQt5.QtGui import (
    QTextCursor,
    QTextCharFormat,
    QColor,
    QFont,
    QCursor,
    QPalette,
    QPixmap,
)
from PyQt5.QtCore import (
    Qt,
    QCoreApplication,
)

from Presets.default_settings import load_settings, original_instruction


class USSMessages(QWidget):
    def __init__(self, ascii_text, ascii_colors, parent=None):
        super().__init__(parent)

        # Enregistrement de la référence à l'objet QLabel contenant l'image ASCII
        self.ascii_text = ascii_text
        self.ascii_colors = ascii_colors
        self.settings = load_settings()

        # Mise en place de l'interface utilisateur
        self.setLayout(QVBoxLayout())
        # Boutons permettant de sélectionner une zone de la grille
        self.zone_demande_instruction_button = QPushButton("Zone Demande Instruction")
        self.position_curseur_button = QPushButton("Position curseur")
        self.zone_uss_message_button = QPushButton("Zone USS Message")
        self.zone_demande_instruction_button_undo = QPushButton("Annuler")
        self.position_curseur_button_undo = QPushButton("Annuler")
        self.zone_uss_message_button_undo = QPushButton("Annuler")
        top_layout = QHBoxLayout()
        group_1 = QVBoxLayout()
        group_2 = QVBoxLayout()
        group_3 = QVBoxLayout()
        group_1.addWidget(self.zone_demande_instruction_button)
        group_1.addWidget(self.zone_demande_instruction_button_undo)
        group_2.addWidget(self.position_curseur_button)
        group_2.addWidget(self.position_curseur_button_undo)
        group_3.addWidget(self.zone_uss_message_button)
        group_3.addWidget(self.zone_uss_message_button_undo)

        top_layout.addLayout(group_1)
        top_layout.addLayout(group_2)
        top_layout.addLayout(group_3)
        # Grille contenant les caractères de l'image ASCII
        self.grid_layout = QGridLayout()
        self.layout().setAlignment(Qt.AlignTop)
        self.layout().addLayout(top_layout)
        self.list_buttons = []
        
        # Remplissage de la grille avec les caractères de l'image ASCII
        self.fill_grid()

        # Connexion des signaux "clicked" des boutons à leurs méthodes respectives
        self.zone_demande_instruction_button.clicked.connect(self.select_zone_demande_instruction)
        self.position_curseur_button.clicked.connect(self.select_position_curseur)
        self.zone_uss_message_button.clicked.connect(self.select_zone_uss_message)
        self.zone_demande_instruction_button_undo.clicked.connect(self.reset_zone_demande_instruction)
        self.position_curseur_button_undo.clicked.connect(self.reset_position_curseur)
        self.zone_uss_message_button_undo.clicked.connect(self.reset_zone_uss_message)

        # selected buttons
        self.first = True
        self.one_click = False
        self.selection = False
        self.selection_1 = False
        self.selection_1_area = (0, 0, 0, 0)
        self.selection_2 = False
        self.selection_2_area = (0, 0, 0, 0)
        self.selection_3 = False
        self.selection_3_area = (0, 0, 0, 0)
        self.waiting_clicks = False
        self.start_col = 0
        self.start_row = 0
        self.end_col = 0
        self.end_row = 0

        self.alert_message_sent = False
        self.alarm = None

        h_layout = QHBoxLayout()
        self.instr_edit = QLineEdit(self)
        self.instr = self.settings.get('INSTRUCTION')[0]
        self.instr_edit.setText(self.instr)
        reset_button = QPushButton("Défaut", self)
        reset_button.clicked.connect(self.reset_line)
        self.instr_edit.textChanged.connect(partial(self.check_text, self.instr_edit))
        h_layout.addWidget(self.instr_edit)
        h_layout.addWidget(reset_button)
        self.layout().addLayout(h_layout)

        save_button = QPushButton("Enregistrer le texte", self)
        save_button.clicked.connect(self.save_changes)
        self.layout().addWidget(save_button)


    def fill_grid(self):
        """Remplit la grille avec les caractères de l'image ASCII."""
        # Découpage du texte en lignes
        lines = self.ascii_text
        # Ajout des lignes dans la grille
        for row, line in enumerate(lines):
            self.list_buttons.append([])
            for col, char in enumerate(line):
                button = QPushButton(char)
                button.setFixedSize(13, 18)
                button.setStyleSheet(
                    f"background-color: {self.ascii_colors[row][col].name()};"
                )
                button.clicked.connect(partial(self.get_pos_button, col, row))
                self.grid_layout.addWidget(button, row, col)
                self.list_buttons[row].append(button)
        self.grid_layout.setSpacing(0)
        self.layout().addLayout(self.grid_layout)

    def get_pos_button(self, col, row):
        if self.waiting_clicks:
            if self.one_click:
                    self.selection = True
                    self.first = True
                    self.start_col = col
                    self.start_row = row
                    self.end_col = col + 1
                    self.end_row = row + 1
            else:
                if not self.first:
                    self.selection = True
                    self.first = True
                    self.end_col = col + 1
                    self.end_row = row + 1
                else:
                    self.first = False
                    self.start_col = col
                    self.start_row = row

    def select_zone_demande_instruction(self):
        """Sélectionne une zone de la grille de couleur rouge."""
        if self.alert_message_sent:
            item = self.layout().takeAt(4)
            widget = item.widget()
            self.layout().removeWidget(widget)
            if widget is not None:
                widget.deleteLater()
            self.alert_message_sent = False
        self.one_click = True
        if not self.selection_1:
            while not self.selection:
                self.waiting_clicks = True
                QCoreApplication.processEvents()
            starting_x = self.start_col
            starting_y = self.start_row
            # num_cols = self.end_col - self.start_col
            num_cols = len(self.settings.get('INSTRUCTION')[0])
            num_rows = self.end_row - self.start_row

            if starting_x + num_cols > len(self.ascii_colors[0]):
                print('ERROR 0')
                self.alert_message(0)
                self.selection = False
                self.waiting_clicks = False
                return

            for i in range(num_rows):
                for j in range(num_cols):
                    try:
                        row = starting_y + i
                        col = starting_x + j
                        self.list_buttons[row][col]
                    except IndexError:
                        print('ERROR 0')
                        self.alert_message(0)
                        self.selection = False
                        self.waiting_clicks = False
                        return
                    button = self.list_buttons[row][col]
                    button.setStyleSheet(
                        f"background-color: red;"
                    )
            self.selection_1 = True
            self.selection = False
            self.waiting_clicks = False
            self.selection_1_area = (starting_x, starting_y, num_cols, num_rows)

    def select_position_curseur(self):
        """Sélectionne une zone de la grille de couleur bleu."""
        if self.alert_message_sent:
            item = self.layout().takeAt(4)
            widget = item.widget()
            self.layout().removeWidget(widget)
            if widget is not None:
                widget.deleteLater()
            self.alert_message_sent = False
        self.one_click = True
        if not self.selection_2:
            while not self.selection:
                self.waiting_clicks = True
                QCoreApplication.processEvents()
            starting_x = self.start_col
            starting_y = self.start_row
            num_cols = self.end_col - self.start_col
            num_rows = self.end_row - self.start_row

            for i in range(num_rows):
                for j in range(num_cols):
                    row = starting_y + i
                    col = starting_x + j
                    button = self.list_buttons[row][col]
                    button.setStyleSheet(
                        f"background-color: blue;"
                    )
            self.selection_2 = True
            self.selection = False
            self.waiting_clicks = False
            self.selection_2_area = (starting_x, starting_y, num_cols, num_rows)
            self.one_click = False

    def select_zone_uss_message(self):
        """Sélectionne une zone de la grille de couleur jaune."""
        if self.alert_message_sent:
            item = self.layout().takeAt(4)
            widget = item.widget()
            self.layout().removeWidget(widget)
            if widget is not None:
                widget.deleteLater()
            self.alert_message_sent = False
        self.one_click = True
        if not self.selection_3:
            while not self.selection:
                self.waiting_clicks = True
                QCoreApplication.processEvents()
            starting_x = self.start_col
            starting_y = self.start_row
            # num_cols = self.end_col - self.start_col
            num_cols = max( len(msg) for msg in self.settings.get('MESSAGES'))
            num_rows = self.end_row - self.start_row

            if starting_x + num_cols > len(self.ascii_colors[0]):
                print('ERROR 0')
                self.alert_message(0)
                self.selection = False
                self.waiting_clicks = False
                return

            for i in range(num_rows):
                for j in range(num_cols):
                    try:
                        row = starting_y + i
                        col = starting_x + j
                        self.list_buttons[row][col]
                    except IndexError:
                        print('ERROR 0')
                        self.alert_message(0)
                        self.selection = False
                        self.waiting_clicks = False
                        return
                    button = self.list_buttons[row][col]
                    button.setStyleSheet(
                        f"background-color: yellow;"
                    )
            self.selection_3 = True
            self.selection = False
            self.waiting_clicks = False
            self.selection_3_area = (starting_x, starting_y, num_cols, num_rows)
            self.one_click = False

    def reset_zone_demande_instruction(self):
        self.selection_1 = False
        self.reset_zone(self.selection_1_area)

    def reset_position_curseur(self):
        self.selection_2 = False
        self.reset_zone(self.selection_2_area)

    def reset_zone_uss_message(self):
        self.selection_3 = False
        self.reset_zone(self.selection_3_area)

    def reset_zone(self, selection_area):
        #self.selection_1 = False
        #self.selection_1_area = (0, 0, 0, 0)
        starting_x = selection_area[0]
        starting_y = selection_area[1]
        num_cols = selection_area[2]
        num_rows = selection_area[3]

        for i in range(num_rows):
            for j in range(num_cols):
                row = starting_y + i
                col = starting_x + j
                button = self.list_buttons[row][col]
                button.setStyleSheet(
                    f"background-color: {self.ascii_colors[row][col].name()};"
                )
    def reset_line(self, index):
        instr = original_instruction()
        self.instr_edit.setText(instr)

    def check_text(self, line_edit):
        text = line_edit.text()
        if len(text) > 49 or '"' in text:
            line_edit.setStyleSheet("background-color: #f22c3d")
        else:
            line_edit.setStyleSheet("")

    def save_changes(self):
        # Récupérez les nouvelles valeurs de chaque QLineEdit et enregistrez-les dans le fichier JSON
        self.settings.get('INSTRUCTION')[0] = self.instr_edit.text()
        # Écrivez les modifications dans le fichier JSON
        with open("settings.json", "w") as f:
            json.dump(self.settings, f)


    def alert_message(self, alert):
        if alert == 0:
            text = QLabel(
                """Votre selection est trop à droite.

                """
            )
            text.setStyleSheet("color: #f22c3d")
            text.setAlignment(Qt.AlignCenter)
            self.layout().addWidget(text)
        self.alert_message_sent = True
        self.alarm = text
