import unittest
import numpy as np
from PIL import (
                            Image,
)
from PyQt5.QtWidgets import (
                            QWidget,
                            QLabel,
                            QFileDialog,
                            QPushButton,
                            QTextEdit,
                            QVBoxLayout,
                            QHBoxLayout,
                            QColorDialog,
                            QSizePolicy,
                            QApplication, 
                            QMainWindow,
)
from PyQt5.QtGui import (
                            QImage,
                            QTextCursor,
                            QTextCharFormat,
                            QColor,
                            QFont,
                            QPalette,
                            QPixmap,
)
from PyQt5.QtCore import (
                            Qt,
)
import os.path, sys
sys.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
)
from Widgets.ascii import ASCIIWidget


class TestASCIIWidget(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Créer une instance de QApplication avant de créer les widgets
        cls.app = QApplication([])

    def setUp(self):
        self.ascii_widget = ASCIIWidget()

    def test_generate_image(self):
        # Créer une image de test avec PIL
        image = QImage(10, 10, QImage.Format_RGB32)

        # Remplissez l'image avec la couleur rouge en utilisant fill()
        image.fill(Qt.red)
        # Charger l'image dans l'ASCIIWidget
        self.ascii_widget.update_image(image)

        # Vérifier que l'ASCIIWidget génère correctement les caractères ASCII 
        # et les couleurs
        self.ascii_widget.generate_image()
        self.assertEqual(
            self.ascii_widget.ascii_text,
            [
                '8' * self.ascii_widget.ascii_width 
                for _ in range(self.ascii_widget.ascii_height)
            ]
        )
        self.assertEqual(
            self.ascii_widget.ascii_colors[0][0].name(),
            '#ff0000'
        )

    def test_simplify_colors(self):
        # Créer une image de test avec PIL
        image = QImage(10, 10, QImage.Format_RGB32)
        # Remplissez l'image avec la couleur rouge en utilisant fill()
        image.fill(QColor('#FF0505'))
        # Charger l'image dans l'ASCIIWidget
        self.ascii_widget.update_image(image)
        # Générez les caractères ASCII et les couleurs de l'image
        self.ascii_widget.generate_image()
        # Vérifiez que tous les caractères ASCII ont la couleur rouge avant 
        # la simplification des couleurs
        self.assertEqual(
            self.ascii_widget.ascii_colors[0][0].name(),
            '#ff0505'
        )
        # Simplifiez les couleurs de l'ASCIIWidget
        self.ascii_widget.simplify_colors()
        # Vérifiez que tous les caractères ASCII ont maintenant la couleur 
        # la plus proche parmi les couleurs définies
        self.assertEqual(
            self.ascii_widget.ascii_colors[0][0].name(),
            '#cc0000'
        )


if __name__ == '__main__':
    unittest.main()
