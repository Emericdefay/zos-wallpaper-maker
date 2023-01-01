import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout
from PyQt5.QtGui import QPalette, QColor, QIcon

from PyQt5.QtCore import (
                            Qt,
)

import resources

# importez les modules et les widgets nécessaires
from Widgets.ascii import    ASCIIWidget
from Widgets.image import    ImageWidget
from Widgets.ussmaker import USSMaker

from Configuration.settings import (
    scales,
)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)
        self.initUI()

    def initUI(self):
        # définissez la largeur et la hauteur de la fenêtre
        self.setGeometry(0, 0, 1200, 610)
        self.max_height = 580

        # Charger l'icône à partir d'un fichier
        self.setWindowIcon(QIcon(':/icons/favicon'))

        # définissez le titre de la fenêtre
        self.setWindowTitle("Zos Wallpaper Maker")

        # définissez la couleur de fond de la fenêtre
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(200, 200, 150))
        self.setPalette(palette)
        # créez des layouts et ajoutez des widgets à partir de vos modules
        layout = QGridLayout(self)
        self.ascii_widget = ASCIIWidget(**scales)
        self.image_widget = ImageWidget(brother=self.ascii_widget, **scales)
        self.ussmaker_widget = USSMaker(**scales)
        
        layout.addWidget(self.image_widget, 0, 0)
        layout.addWidget(self.ascii_widget, 0, 1)
        layout.addWidget(self.ussmaker_widget, 0, 2)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
