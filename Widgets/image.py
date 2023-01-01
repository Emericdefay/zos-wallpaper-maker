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
    def __init__(self, Y_CONST, X_CONST, brother, parent=None, *args, **kwargs):
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
        # Affichez une boîte de dialogue d'ouverture de fichier pour sélectionner l'image à ouvrir
        file_name, _ = QFileDialog.getOpenFileName(self, "Ouvrir l'image", "", "Images (*.png *.xpm *.jpg *.bmp);;Tous les fichiers (*)")

        # Si un fichier est sélectionné, chargez-le dans le QLabel
        if file_name:
            pixmap = QPixmap(file_name)
            if pixmap.height() > self.max_height or pixmap.width() > self.max_width:
                pixmap = pixmap.scaled(self.max_width, self.max_height, Qt.KeepAspectRatio)
            # affichez le pixmap dans un widget QLabel ou autre
            self.pixmap = pixmap
            self.image_label.setPixmap(pixmap)
            self.image_opened = True
            # self.rubber_band = QRect(0, 0, self.image_width, self.image_height)
        else: 
            self.image_opened = False
            print('ERROR 102')

    def mousePressEvent(self, event):
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
            # Définit le rectangle de sélection à l'aide des coordonnées de départ et de la hauteur calculée
            self.rubber_band.setGeometry(QRect(event.x(), event.y(), self.X_CONST, self.Y_CONST))
            # self.rubber_band.show()            

    def mouseMoveEvent(self, event):
        if not self.image_opened:
            return

        if self.clicked_rubber_band:
            # déplacez le rubber_band en fonction de la position du curseur
            delta_x = event.pos().x() - self.last_mouse_position.x()
            delta_y = event.pos().y() - self.last_mouse_position.y()
            self.rubber_band.move(self.rubber_band.x() + delta_x, self.rubber_band.y() + delta_y)
            self.last_mouse_position = event.pos()
            #self.rubber_band.move(event.pos())
        else:
            try:
                self.rubber_band.setGeometry(QRect(self.origin, event.pos()).normalized())
                x, y, w, h = self.rubber_band.geometry().getRect()
                # Modifiez la hauteur en fonction de la largeur et des constantes x_const et y_const
                h = int(w * self.Y_CONST / self.X_CONST)
                self.rubber_band.setGeometry(x, y, w, h)
                self.initial_rubber_band = self.rubber_band
                self.rubber_band.show()            
            except AttributeError:
                print('ERROR 101')

    def mouseReleaseEvent(self, event):
        # récupérez la zone sélectionnée
        self.selected_region = self.rubber_band.geometry()
        self.clicked_rubber_band = False


    def send_area(self):
        try:
            selected_pixmap = self.pixmap.copy(self.selected_region)
            selected_image = selected_pixmap.toImage()
            # Recherche l'instance du widget ASCII en utilisant son type
            self.parent().update_image(selected_image)
        except AttributeError:
            selected_pixmap = self.pixmap
            selected_image = selected_pixmap.toImage()
            # Recherche l'instance du widget ASCII en utilisant son type
            self.parent().update_image(selected_image)
