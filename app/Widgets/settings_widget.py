import json
from functools import partial
from PyQt5.QtWidgets import (
    QWidget,
    QPushButton, 
    QLabel,
    QVBoxLayout, 
    QGroupBox, 
    QHBoxLayout,
    QColorDialog,
    QGraphicsDropShadowEffect,
)
from PyQt5.QtGui import (
    QColor,
    QFont,
    QPalette,
)
from PyQt5.QtCore import (
    pyqtSignal,
    Qt,
)
from Presets.default_settings import load_settings, write_default_json


class SettingsWidget(QWidget):
    """Widget permettant de changer les paramètres de l'application.

    Attributes:
        parent (QWidget): Widget parent.
        settings (dict): Dictionnaire contenant les paramètres de 
                         l'application.
    """
    # Définition du signal personnalisé settingsSaved
    settingsSaved = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Charge les paramètres
        self.settings = load_settings()

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(129, 129, 129))
        self.setPalette(palette)

        # Mise en place de l'interface utilisateur
        self.setLayout(QVBoxLayout())
        self.color_groupbox = QGroupBox("Couleurs affichées")
        self.color_layout = QVBoxLayout()
        self.color_groupbox.setLayout(self.color_layout)

        # Création des widgets de modification de couleur
        self.color_widgets = []
        for index, color in enumerate(self.settings["DISPLAYED_COLORS"]):
            color_widget = QWidget()
            color_widget.setLayout(QHBoxLayout())
            # Label
            text = self.settings["ASSOCIATED_NAME"][index]
            color_label = QLabel(text)
            color_label.setAlignment(Qt.AlignCenter)
            color_label.setFont(QFont("Arial", 12, QFont.Bold))
            # Ajoute une ombre 
            shadow_effect = QGraphicsDropShadowEffect()
            shadow_effect.setColor(QColor(0, 0, 0))
            shadow_effect.setOffset(5, 6)
            shadow_effect.setBlurRadius(2)
            color_label.setGraphicsEffect(shadow_effect)
            # initialize fond zone de texte
            color_label.setStyleSheet(f"background-color: #{color[2:]};")

            color_button = QPushButton("Modifier")
            color_widget.layout().addWidget(color_label)
            color_widget.layout().addWidget(color_button)
            self.color_layout.addWidget(color_widget)
            self.color_widgets.append((color_label, color_button))

        self.prev_colors_groupbox = QGroupBox("Couleurs du terminal")
        self.prev_color_layout = QVBoxLayout()
        self.prev_colors_groupbox.setLayout(self.prev_color_layout)

        # Création des widgets de modification de couleur
        self.prev_color_widgets = []
        for index, color in enumerate(self.settings["PREVIEWED_COLORS"]):
            color_widget = QWidget()
            color_widget.setLayout(QHBoxLayout())
            # Label
            text = self.settings["ASSOCIATED_NAME"][index]
            color_label = QLabel(text)
            color_label.setAlignment(Qt.AlignCenter)
            color_label.setFont(QFont("Arial", 12, QFont.Bold))
            # Ajoute une ombre 
            shadow_effect = QGraphicsDropShadowEffect()
            shadow_effect.setColor(QColor(0, 0, 0))
            shadow_effect.setOffset(5, 6)
            shadow_effect.setBlurRadius(2)
            color_label.setGraphicsEffect(shadow_effect)
            # initialize fond zone de texte
            color_label.setStyleSheet(f"background-color: #{color[2:]};")

            prev_color_button = QPushButton("Modifier")
            color_widget.layout().addWidget(color_label)
            color_widget.layout().addWidget(prev_color_button)
            self.prev_color_layout.addWidget(color_widget)
            self.prev_color_widgets.append((color_label, prev_color_button))

        # Bouton Enregistrer
        self.save_button = QPushButton("Enregistrer")
        # Bouton Par Défaut
        self.default_button = QPushButton("Défaut")

        # sublayout
        sublayout_1 = QHBoxLayout()
        sublayout_1.addWidget(self.color_groupbox)
        sublayout_1.addWidget(self.prev_colors_groupbox)
        self.layout().addLayout(sublayout_1)
        
        # save / default
        self.layout().addWidget(self.save_button)
        self.layout().addWidget(self.default_button)

        # Connexion des signaux color
        for index in range(len(self.color_widgets)):
            color_label  = self.color_widgets[index][0]
            color_button = self.color_widgets[index][1]
            color_button.clicked.connect(
                partial(self.change_color, index, color_label)
                )
        # Connexion des signaux prev_color
        for index in range(len(self.prev_color_widgets)):
            color_label  = self.prev_color_widgets[index][0]
            prev_color_button = self.prev_color_widgets[index][1]
            prev_color_button.clicked.connect(
                partial(self.change_prev_color, index, color_label)
                )
        self.save_button.clicked.connect(self.save_settings)
        self.default_button.clicked.connect(self.default_settings)

    def change_color(self, index, color_label):
        """
            Modifie la couleur à l'index spécifié dans 
            la liste DISPLAYED_COLORS.

        Args:
            index (int): Index de la couleur à modifier.
            color_label (QLabel): Widget de couleur à mettre à jour.

        Returns:
            bool: True si la couleur a été modifiée avec succès, False sinon.
        """
        # Récupérer la couleur actuelle à partir du widget de couleur
        current_color = color_label.palette().color(QPalette.Window)

        # Afficher une boîte de dialogue de sélection de couleur avec 
        # la couleur actuelle en valeur initiale
        color = QColorDialog.getColor(current_color)
        # vérifiez si une couleur a été sélectionnée
        if color.isValid():
            try:
                self.settings['DISPLAYED_COLORS'][index] = '0x' + \
                                                            color.name()[1:]
                self.color_widgets[index][0].setStyleSheet(
                    f"background-color: {color.name()};"
                )
            except Exception as e:
                print(e)
                pass

    def change_prev_color(self, index, color_label):
        """
            Modifie la couleur à l'index spécifié dans 
            la liste DISPLAYED_COLORS.

        Args:
            index (int): Index de la couleur à modifier.
            color_label (QLabel): Widget de couleur à mettre à jour.

        Returns:
            bool: True si la couleur a été modifiée avec succès, False sinon.
        """
        # Récupérer la couleur actuelle à partir du widget de couleur
        current_color = color_label.palette().color(QPalette.Window)

        # Afficher une boîte de dialogue de sélection de couleur avec la 
        # couleur actuelle en valeur initiale
        color = QColorDialog.getColor(current_color)
        # vérifiez si une couleur a été sélectionnée
        if color.isValid():
            try:
                self.settings['PREVIEWED_COLORS'][index] = '0x' + \
                                                            color.name()[1:]
                self.prev_color_widgets[index][0].setStyleSheet(
                    f"background-color: {color.name()};"
                )
            except Exception as e:
                print(e)
                pass

    def save_settings(self):
        """Sauvegarde les paramètres de l'application dans un fichier JSON.

        Returns:
            bool: True si les paramètres ont été sauvegardés avec succès, 
            False sinon.
        """
        try:
            with open('settings.json', 'w') as f:
                json.dump(self.settings, f)
        except Exception as e:
            print(e)
            return False
        # Emettre le signal settingsSaved
        self.settingsSaved.emit()
        # Fermer la fenêtre
        self.close()
        return True

    def default_settings(self):
        with open("settings.json", "w") as f:
            json.dump(write_default_json(), f, indent=4)
        with open("settings.json", "r") as f:
            self.settings = json.load(f)
        # Emettre le signal settingsSaved
        self.settingsSaved.emit()
        # Fermer la fenêtre
        self.close()
