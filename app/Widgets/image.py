from PyQt5.QtWidgets import (
                            QWidget,
                            QLabel,
                            QFileDialog,
                            QPushButton,
                            QVBoxLayout,
                            QRubberBand,
)
from PyQt5.QtGui import (
                            QPixmap,
)
from PyQt5.QtCore import (
                            Qt,
                            QRect,
)


class ImageWidget(QWidget):
    """
        ImageWidget est une classe qui hérite de QWidget et qui est utilisée 
        pour afficher une image à l'écran. Elle peut être utilisée de manière 
        autonome ou intégrée à une fenêtre plus large (par exemple en utilisant
        un layout).
    """
    def __init__(
        self,
        Y_CONST,
        X_CONST,
        brother,
        parent=None,
            *args, **kwargs):
        super().__init__(parent)
        # Créez un QLabel pour afficher l'image
        self.image_label = QLabel(self)
        self.Y_CONST = Y_CONST
        self.X_CONST = X_CONST
        self.clicked_rubber_band = False
        self.ascii_widget = brother

        # Proportions maximales
        max_width = kwargs.get('max_width', 2000)
        max_height = kwargs.get('max_height', 610)
        self.max_width = max_width
        self.max_height = max_height

        self.pixmap = None

        self.image_opened = False

        # ajustez la taille de l'image en fonction de sa hauteur maximale
        self.image_label.setScaledContents(True)
        self.image_label.setMaximumHeight(self.max_height)

        # créez un QRubberBand pour sélectionner une zone dans l'image
        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)

        # Créez un QPushButton pour ouvrir l'image
        self.open_button = QPushButton("Ouvrir", self)
        self.open_button.clicked.connect(self.open_image)

        # Créez un QPushButton pour sélectionner une zone de l'image
        self.select_button = QPushButton("Sélectionner", self)
        self.select_button.clicked.connect(self.send_area)

        # Créez un QVBoxLayout pour organiser les widgets verticalement
        layout = QVBoxLayout(self)
        layout.addWidget(self.image_label)
        layout.addWidget(self.open_button)
        layout.addWidget(self.select_button)

    def open_image(self):
        """
            Cette méthode ouvre une image à partir de son emplacement sur le 
            disque dur. Elle peut être utilisée pour afficher l'image dans 
            l'interface utilisateur ou pour la traiter de quelque manière que 
            ce soit.
        """
        # Affichez une boîte de dialogue d'ouverture de fichier pour 
        # sélectionner l'image à ouvrir
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Ouvrir l'image",
            "",
            "Images (*.png *.xpm *.jpg *.bmp);;Tous les fichiers (*)"
        )

        # Si un fichier est sélectionné, chargez-le dans le QLabel
        if file_name:
            pixmap = QPixmap(file_name)
            if pixmap.height() > self.max_height or \
               pixmap.width()  > self.max_width:
                pixmap = pixmap.scaled(
                    self.max_width,
                    self.max_height,
                    Qt.KeepAspectRatio
                )
            # affichez le pixmap dans un widget QLabel ou autre
            self.pixmap = pixmap
            self.image_label.setPixmap(pixmap)
            self.image_opened = True
        else: 
            self.image_opened = False
            print('ERROR 102')

    def mousePressEvent(self, event):
        """
            Cette méthode est appelée lorsque l'utilisateur appuie sur un 
            bouton de la souris. Elle peut être utilisée pour détecter le 
            début d'un clic de souris ou le déplacement de la souris avec 
            un bouton maintenu enfoncé.
        """
        # commencez la sélection lorsque l'utilisateur clique dans l'image
        self.origin = event.pos()
        if not self.image_opened:
            return
        if self.clicked_rubber_band:
            return
        if self.rubber_band.geometry().contains(event.pos()):
            self.clicked_rubber_band = True
            self.last_mouse_position = event.pos()
        else:
            self.rubber_band.hide()
            self.origin = event.pos()
            # Définit le rectangle de sélection à l'aide des coordonnées de 
            # départ et de la hauteur calculée
            self.rubber_band.setGeometry(
                QRect(event.x(), event.y(), self.X_CONST, self.Y_CONST)
            )

    def mouseMoveEvent(self, event):
        """
            Cette méthode est appelée lorsque l'utilisateur déplace la souris.
            Elle peut être utilisée pour suivre le mouvement de la souris et
            mettre à jour l'interface utilisateur en conséquence.
        """
        if not self.image_opened:
            return

        if self.clicked_rubber_band:
            # déplacez le rubber_band en fonction de la position du curseur
            delta_x = event.pos().x() - self.last_mouse_position.x()
            delta_y = event.pos().y() - self.last_mouse_position.y()
            self.rubber_band.move(
                self.rubber_band.x() + delta_x, self.rubber_band.y() + delta_y
            )
            self.last_mouse_position = event.pos()
        else:
            try:
                self.rubber_band.setGeometry(
                    QRect(self.origin, event.pos()).normalized()
                )
                x, y, w, h = self.rubber_band.geometry().getRect()
                # Modifiez la hauteur en fonction de la largeur et des 
                # constantes x_const et y_const
                h = int(w * self.Y_CONST / self.X_CONST)
                self.rubber_band.setGeometry(x, y, w, h)
                self.initial_rubber_band = self.rubber_band
                self.rubber_band.show()            
            except AttributeError:
                print('ERROR 101')

    def mouseReleaseEvent(self, event):
        """
            Cette méthode est appelée lorsque l'utilisateur relâche un bouton
            de la souris. Elle peut être utilisée pour détecter la fin d'un 
            clic de souris ou le déplacement de la souris avec un bouton 
            maintenu enfoncé.
        """
        # récupérez la zone sélectionnée
        self.selected_region = self.rubber_band.geometry()
        self.clicked_rubber_band = False

    def send_area(self):
        try:
            try:
                selected_pixmap = self.pixmap.copy(self.selected_region)
                selected_image = selected_pixmap.toImage()
                # Recherche l'instance du widget ASCII en utilisant son type
                self.parent().update_image(selected_image)
            except AttributeError as e:
                selected_pixmap = self.pixmap
                selected_image = selected_pixmap.toImage()
                # Recherche l'instance du widget ASCII en utilisant son type
                self.parent().update_image(selected_image)
        except AttributeError as e: 
            if "object has no attribute 'toImage'" in str(e):
                pass
            else:
                print(e) 
                pass