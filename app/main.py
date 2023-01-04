import sys
from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, 
    QGridLayout, 
    QMainWindow, 
    QPushButton, 
    QVBoxLayout,
    QTabWidget,
    QHBoxLayout,
    QDialog,
    QLabel,
    QTextEdit,
    
)
from PyQt5.QtGui import (
    QPalette, 
    QColor, 
    QFont,
    QIcon,
)

from PyQt5.QtCore import (
    Qt,
    pyqtSlot,
    pyqtSignal,
)

import resources

from Widgets.ascii           import ASCIIWidget
from Widgets.image           import ImageWidget
from Widgets.ussmaker        import USSMaker
from Widgets.prompt          import TextFieldWidget
from Widgets.area_uss        import USSMessages
from Widgets.settings_widget import SettingsWidget

from Presets.texthelper      import get_help_text

from Configuration.settings import (
    scales,
)


class MainWindow(QWidget):

    signal_update_image = pyqtSignal(str)  # définition du signal

    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.initUI()

    def initUI(self):
        # définissez la largeur et la hauteur de la fenêtre

        self.setGeometry(100, 100, 1200, 610)
        self.max_height = 580

        # Charger l'icône à partir d'un fichier
        self.setWindowIcon(QIcon(':/icons/favicon'))

        # définissez le titre de la fenêtre
        self.setWindowTitle("Zos Wallpaper Maker")

        # définissez la couleur de fond de la fenêtre
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(76, 112, 140))
        self.setPalette(palette)

        # créez des layouts et ajoutez des widgets à partir de vos modules
        layout = QGridLayout(self)
        self.setLayout(layout)

        self.ussmaker_widget = USSMaker(**scales)
        self.prompt_widget = TextFieldWidget()
        self.ascii_widget = ASCIIWidget(**scales, brother=self.ussmaker_widget)
        self.image_widget = ImageWidget(brother=self.ascii_widget, parent=self, **scales)

        self.ascii_widget.simply_done.connect(self.conversion_done)
        self.image_widget.selected_image_sended.connect(self.go_to_asciitab)

        # Créez une instance de QTabWidget et ajoutez-la au layout principal de votre fenêtre
        self.tab_widget = QTabWidget(self)
        # self.tab_widget.setGeometry(0, 0, self.width(), self.height())

        self.left_layout = QVBoxLayout()
        self.left_layout.addWidget(self.tab_widget)

        # Ajoutez vos widgets ImageWidget et ASCIIWidget aux onglets de QTabWidget
        self.tab_widget.addTab(self.image_widget, "Image en entrée")
        self.tab_widget.addTab(self.ascii_widget, "ASCII Art")
        self.tab_widget.addTab(self.prompt_widget, "Textes")
        

        self.parameters = QPushButton("Paramètres")
        self.parameters.clicked.connect(self.show_settings_widget)

        # définissez la taille de la police de caractères en points
        self.font = QFont()
        self.font.setPointSizeF(10)
        self.font.setFamily("Arial")
        self.help_text = QLabel(self)
        self.help_text.setFont(self.font)

        self.help_text.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.help_text.setMinimumWidth(180)
        self.help_text.setMaximumWidth(180)
        self.help_text.setMinimumHeight(500)
        self.help_text.setMaximumHeight(500)
        self.help_text.setStyleSheet("margin-top:24px;background-color: #cccccc; color: #555555; font-size: 12px; border: 1px solid grey; width: 100%; text-align: left; vertical-align: top;")
        self.tab_widget.currentChanged.connect(self.update_help_text)
        self.update_help_text(0)

        # Copyright
        self.copyright = QLabel("Copyright © 2022 · DEFAY Emeric")
        self.copyright.setAlignment(Qt.AlignCenter)
        
        # créez un layout vertical pour les widgets du coin droit
        right_layout = QGridLayout()
        right_layout.addWidget(self.help_text, 0, 0)

        right_layout_bottom = QVBoxLayout()
        right_layout_bottom.addStretch()
        right_layout_bottom.addWidget(self.ussmaker_widget)
        right_layout_bottom.addWidget(self.parameters)
        right_layout_bottom.addWidget(self.copyright)

        right_layout.addLayout(right_layout_bottom, 1, 0)

        # Application sur le layout
        layout.addLayout(self.left_layout, 0, 0)
        layout.addLayout(right_layout, 0, 1)

        self.signal_update_image.connect(self.update_ascii)

    def update_help_text(self, index):
        self.help_text.setText(get_help_text(index))

    def update_image(self, image):
        """
            update_image est une méthode de la classe MainWindow qui prend 
            un paramètre image de type QImage. Cette méthode appelle la 
            méthode update_image de l'objet ascii_widget, qui doit être 
            une instance de la classe ASCIIWidget, en lui passant le paramètre 
            image. La méthode update_image de ASCIIWidget devrait être 
            utilisée pour mettre à jour l'image affichée dans l'interface 
            utilisateur en utilisant le paramètre image.
        """
        self.ascii_widget.update_image(image)

    def update_ascii(self, text, color):
        """
            update_ascii est une méthode de la classe MainWindow qui prend 
            en argument du texte et des couleurs et les passe à la méthode 
            update_ascii de l'instance de la classe USSMakerWidget appelée 
            self.ussmaker_widget. Cette méthode permet de mettre à jour le 
            texte et les couleurs affichés dans l'interface.
        """
        self.ussmaker_widget.update_ascii(text, color)

    def show_settings_widget(self):

        # Création de la fenêtre modale
        self.settings_dialog = QDialog(self)
        # Création de l'instance de SettingsWidget
        self.settings_widget = SettingsWidget()
        # Ajout de SettingsWidget à la fenêtre modale en utilisant un layout
        self.settings_dialog.setLayout(QVBoxLayout())
        self.settings_dialog.layout().addWidget(self.settings_widget)
        # Connexion du signal settingsSaved à la slot close_settings_widget
        self.settings_widget.settingsSaved.connect(self.close_settings_widget)
        # Affichage de la fenêtre modale
        self.settings_dialog.exec_()

    @pyqtSlot()
    def close_settings_widget(self):
        """Ferme la fenêtre modale des paramètres."""
        self.settings_dialog.hide()

    @pyqtSlot()
    def go_to_asciitab(self):
        """Va à l'onglet ASCII après avoir Selectionné l'image ou une partie"""
        self.tab_widget.setCurrentIndex(1)

    @pyqtSlot()
    def conversion_done(self):
        self.ussmessages = USSMessages(
            ascii_colors=self.ascii_widget.ascii_colors,
            ascii_text=self.ascii_widget.ascii_text,
            parent=self
        )
        self.tab_widget.removeTab(3)
        self.tab_widget.addTab(self.ussmessages, "Curseurs")

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        return 


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
