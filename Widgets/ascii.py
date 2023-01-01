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
)
from PyQt5.QtGui import (
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

from Configuration.settings import VARIATIONS_ASCII, DISPLAYED_COLORS


class ASCIIWidget(QWidget):
    """
        ASCIIWidget est une classe qui hérite de la classe QWidget de Qt, 
        qui représente un widget de base dans une interface graphique. 
        ASCIIWidget peut être utilisé pour afficher une image sous forme de 
        caractères ASCII dans une interface graphique. 
    """
    def __init__(self, ascii_height=22, ascii_width=80, parent=None, *args, **kwargs):
        """
            Méthode de création de l'objet. Elle initialise les attributs 
            de la classe et crée les widgets de l'interface.
        """
        super().__init__(parent)
        size_policy = QSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.Expanding
        )
        self.setSizePolicy(size_policy)

        # Créer l'image à afficher en utilisant un QLabel et une QPixmap
        self.image_label = QLabel(self)
        self.image_pixmap = QPixmap()
        self.image_label.setPixmap(self.image_pixmap)
       
        # initialisez la hauteur et la largeur de l'image en ASCII en nombre 
        # de caractères
        self.ascii_height = ascii_height
        self.ascii_width = ascii_width
        self.ascii_chars = VARIATIONS_ASCII
        self.ascii_text = []
        self.image = None
        self.ascii_colors = None

        # définissez la taille de la police de caractères en points
        self.font = QFont()
        self.font.setPointSizeF(12.5)
        self.font.setFamily("Courier")
        self.font.setWeight(QFont.Bold)

        # créez un objet QLabel pour afficher les caractères ASCII
        self.ascii_label = QTextEdit(self)
        self.ascii_label.setFont(self.font)
        self.ascii_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # initialize fond zone de texte
        palette = QPalette()
        palette.setColor(QPalette.Base, QColor(0, 0, 0))
        # appliquez l'objet QPalette à la zone de texte
        self.ascii_label.setPalette(palette)

        # Curseurs
        self.red_def = 33
        self.grn_def = 33
        self.blu_def = 34

        # ajoutez un bouton pour changer la couleur de fond de la zone de texte
        self.color_button = QPushButton("Changer la couleur de fond")
        self.color_button.clicked.connect(self.change_color)

        # créez un bouton "Simplifier" pour ouvrir une image
        self.simplified = False
        self.simplify_button_sfe = QPushButton("Conversion 3270 (SFE)", self)
        self.simplify_button_sfe.clicked.connect(
            lambda: self.simplify_colors("sfe")
        )

        self.simplify_button_sfsa = QPushButton("Conversion 327+ (SF/SA)", self)
        self.simplify_button_sfsa.clicked.connect(
            lambda: self.simplify_colors("sfsa")
        )

        self.save_img = QPushButton("Sauvegarder en .png", self)
        self.save_img.clicked.connect(self.save_as_image)

        # utilisez un layout pour organiser les widgets
        layout = QVBoxLayout(self) 
        self.setLayout(layout)
        layout.addWidget(self.image_label)
        layout.addWidget(self.ascii_label)
        layout.addWidget(self.color_button)

        sublayout_1 = QHBoxLayout()
        sublayout_1.addWidget(self.simplify_button_sfe)
        sublayout_1.addWidget(self.simplify_button_sfsa)
        layout.addLayout(sublayout_1)

        layout.addWidget(self.save_img)

        # calculez la nouvelle taille des caractères en fonction de la largeur
        # du widget d'ASCII
        font_size = self.width() / (self.ascii_width+100)
        self.font.setPointSizeF(font_size)
        # mettez à jour la taille des caractères de la zone de texte
        self.ascii_label.setFont(self.font)

    def generate_image(self):
        """
            generate_image est une méthode qui s'utilise pour générer une image 
            ASCII à partir d'une image donnée.

            Elle commence par réinitialiser certaines variables de l'instance, 
            comme la zone de texte, la simplification de l'image, les couleurs 
            ASCII et le texte ASCII.

            Elle convertit ensuite l'image donnée en un objet de la 
            bibliothèque d'images Python (PIL) et la redimensionne en fonction 
            de la taille de la zone de texte. Elle crée ensuite un tableau 
            NumPy à partir de l'image et met à jour l'image de l'instance.

            Elle appelle ensuite les méthodes generate_ascii_text et 
            generate_ascii_colors, qui génèrent respectivement le texte ASCII 
            et les couleurs ASCII à partir de l'image. Enfin, elle met à jour 
            la zone de texte avec les caractères ASCII et les couleurs générés 
            en appelant la méthode update_ascii.
        """
        # réinitialisez la zone de texte
        self.ascii_label.setText('')
        self.simplified = False
        self.ascii_colors = []
        self.ascii_text = []
        # Convertir QImage en un objet PIL.Image
        image = Image.fromqimage(self.image)

        if image:
            # redimensionnez l'image en fonction de la taille de la zone de 
            # texte
            image = image.resize(
                (self.ascii_width, self.ascii_height), resample=Image.BICUBIC
            )
            # créez un tableau NumPy à partir de l'image
            image = np.array(image)
            # update l'image de l'instance
            self.image_array = image
            # générez les caractères ASCII à partir de l'image
            self.generate_ascii_text(self.image_array)
            # générez les couleurs pour chaque caractère ASCII à partir de 
            # l'image
            self.generate_ascii_colors(self.image_array)
            # mettez à jour la zone de texte avec les caractères ASCII et les 
            # couleurs générés
            self.update_ascii()

    def generate_ascii_text(self, image):
        """
            generate_ascii_text est une méthode qui prend en entrée une image
             sous forme de tableau NumPy et qui génère des caractères ASCII 
             à partir de cette image.

            Elle fonctionne en parcourant chaque pixel de l'image et en le 
            convertissant en un caractère ASCII en fonction de sa luminosité. 
            Plus précisément, la luminosité d'un pixel est calculée en 
            faisant la moyenne de ses valeurs de rouge, de vert et de bleu, 
            et en la comparant à un échantillon de valeurs de luminosité 
            prédéfinies, chacune correspondant à un caractère ASCII.
        """
        self.ascii_text = []
        # itérez sur chaque pixel de l'image
        for r in range(self.ascii_height):
            ascii_row = ""
            for c in range(self.ascii_width):
                # calculez l'index du caractère ASCII correspondant au pixel
                try:
                    # récupérez les valeurs RVB et alpha du pixel
                    red, green, blue, _ = image[r][c]
                except ValueError:
                    # récupérez les valeurs de rouge, vert et bleu du pixel
                    red, green, blue = image[r][c]

                gray = self.red_def * red + \
                       self.grn_def * green + \
                       self.blu_def * blue 
                gray /= 100
                if gray > 256:
                    gray = 255

                ascii_index = int(gray / 256.0 * len(self.ascii_chars))
                
                ascii_char = self.ascii_chars[ascii_index]
                ascii_row += ascii_char
            self.ascii_text.append(ascii_row)

    def generate_ascii_colors(self, image):
        """
            generate_ascii_colors est une méthode qui prend en entrée une 
            image sous forme de tableau NumPy et génère des couleurs pour 
            chaque caractère ASCII de la zone de texte de l'application. 
            Elle fonctionne en parcourant chaque pixel de l'image et en 
            utilisant la méthode get_ascii_color pour obtenir la couleur 
            du caractère ASCII qui correspond au pixel. Ces couleurs sont 
            ensuite stockées dans une liste self.ascii_colors.
        """
        # itérez sur chaque ligne et colonne de l'image
        ascii_colors = []
        for r in range(self.ascii_height):
            row = []
            for c in range(self.ascii_width):
                try:
                    # récupérez les valeurs RVB et alpha du pixel
                    red, green, blue, alpha = image[r][c]
                    # créez un objet QColor à partir des valeurs RVB et alpha
                    # du pixel
                    color = QColor(red, green, blue, alpha)
                except ValueError:
                    # récupérez les valeurs de rouge, vert et bleu du pixel
                    red, green, blue = image[r][c]
                    # créez un objet QColor à partir des valeurs RVB du pixel
                    color = QColor(red, green, blue)
                row.append(color)
            ascii_colors.append(row)
        # mettez à jour self.ascii_colors avec les couleurs générées
        self.ascii_colors = ascii_colors

    def change_color(self):
        # affichez une palette pour sélectionner une couleur
        color = QColorDialog.getColor()
        # vérifiez si une couleur a été sélectionnée
        if color.isValid():
            # créez un objet QPalette avec la couleur de fond sélectionnée
            palette = QPalette()
            palette.setColor(QPalette.Base, color)
            # appliquez l'objet QPalette à la zone de texte
            self.ascii_label.setPalette(palette)

    def update_ascii(self):
        # réinitialisez la zone de texte
        self.ascii_label.setText('')
        # créez un objet QTextCursor à partir de la zone de texte
        cursor = QTextCursor(self.ascii_label.textCursor())
        # placez le curseur au début de la zone de texte
        cursor.movePosition(QTextCursor.Start)
        # itérez sur chaque ligne de self.ascii_chars
        for i, row in enumerate(self.ascii_text):
            # itérez sur chaque caractère de la ligne
            for j, char in enumerate(row):
                # récupérez la couleur du caractère à partir de 
                # self.ascii_colors
                color = self.ascii_colors[i][j]
                # créez un objet QTextCharFormat avec la couleur du caractère
                char_format = QTextCharFormat()
                char_format.setForeground(color)
                # insérez le caractère ASCII dans la zone de texte avec le 
                # format de texte défini
                cursor.insertText(char, char_format)
            # insérez un retour à la ligne à la fin de chaque ligne
            cursor.insertText("\n")
        if self.parent():
            self.parent().update_ascii(self.ascii_text, self.ascii_colors)

    def resizeEvent(self, event):
        # calculez la nouvelle taille des caractères en fonction de la largeur
        # du widget d'ASCII
        font_size = self.width() / (self.ascii_width-5)
        self.font.setPointSizeF(font_size)
        # mettez à jour la taille des caractères de la zone de texte
        self.ascii_label.setFont(self.font)
        # redimensionnez le widget d'ASCII en fonction de la taille de la 
        # fenêtre principale
        self.resize(event.size().width(), event.size().height())

    def simplify_colors(self, method=""):
        """
            La fonction simplify_colors s'utilise pour remplacer chaque 
            couleur de l'image ASCII par la couleur la plus proche parmi une 
            liste prédéfinie de couleurs. La distance entre les couleurs est 
            calculée en utilisant la formule de distance CIE76.

            La fonction prend en argument un paramètre optionnel method qui 
            peut être défini comme "sfe" pour activer un traitement 
            spécifique des couleurs. Si method est défini comme "sfe", la 
            couleur de chaque caractère est comparée à celle du caractère 
            précédent dans la ligne. Si les deux couleurs sont différentes 
            et que la couleur précédente n'est pas noire, la couleur actuelle 
            est remplacée par noir.

            Ensuite, la fonction itère sur chaque ligne de self.ascii_text 
            et sur chaque caractère de la ligne. Elle récupère la couleur 
            du caractère en utilisant self.ascii_colors[i][j], où i est 
            l'indice de la ligne et j l'indice du caractère. La fonction 
            calcule alors la distance euclidienne entre la couleur actuelle 
            et chaque couleur de la liste colors en utilisant la fonction 
            self.cie76. Si la distance est inférieure à la distance minimale 
            trouvée jusqu'à présent, la distance minimale et la couleur 
            la plus proche sont mises à jour.
        """
        self.simplified = True
        ascii_colors = []
        # définis les couleurs à utiliser
        colors = DISPLAYED_COLORS

        # itère sur chaque caractère ASCII de self.ascii_chars
        for i, row in enumerate(self.ascii_text):
            text = []
            # itérez sur chaque caractère de la ligne
            for j, char in enumerate(row):
                # récupère la couleur du caractère ASCII
                color = self.ascii_colors[i][j]
                # trouve la couleur la plus proche parmi celles définies
                min_distance = float("inf")
                nearest_color = None
                for c in colors:
                    # calculer la distance euclidienne entre les deux couleurs
                    distance = self.cie76(c, color.name())
                    # si la distance est inférieure à la distance minimale 
                    # trouvée jusqu'à présent, mettre à jour la distance 
                    # minimale et la couleur la plus proche
                    if distance < min_distance:
                        min_distance = distance
                        nearest_color = c

                # remplace la couleur par la couleur la plus proche
                red, green, blue = self.hex_to_rgb(nearest_color)
                if method == "sfe":
                    if j >= 1:
                        current_pixel = nearest_color[2:]
                        last_pixel = text[j-1].name()[1:]
                        black_pixel = '000000'
                        if (current_pixel != last_pixel) and \
                           (last_pixel != black_pixel):
                            new_color = QColor(0, 0, 0)
                        else:
                            new_color = QColor(red, green, blue)
                    else :
                        new_color = QColor(red, green, blue)
                else:
                    new_color = QColor(red, green, blue)
                text.append(new_color)
            ascii_colors.append(text)
        self.ascii_colors = ascii_colors
        self.update_ascii()

    def hex_to_rgb(self, hex_color: str) -> tuple:
        """
            La fonction hex_to_rgb prend en entrée une chaîne de caractères 
            hexadécimale qui représente une couleur, par exemple '#ff0000' 
            pour du rouge. Elle retire le préfixe '0x' ou '#' de la chaîne 
            si nécessaire, puis la convertit en entier en utilisant la 
            fonction int avec comme base de conversion le système de 
            numération hexadécimal.

            Ensuite, la fonction utilise la fonction divmod pour diviser 
            l'entier obtenu par les puissances de 256 correspondant aux 
            valeurs RGB. Par exemple, si l'entier est 0xff0000, cela 
            signifie que la valeur de rouge est 0xff, soit 255 en décimal. 
            La fonction retourne finalement un tuple contenant les valeurs 
            RGB sous forme de nombres entiers.
        """
        # retirez le caractère de début '0x' de la chaîne hexadécimale
        if hex_color[0] == '#':
            hex_color = hex_color[1:]
        else:
            hex_color = hex_color[2:]
        # convertissez la chaîne en entier
        hex_color = int(hex_color, 16)
        # décomposez l'entier en valeurs RGB en utilisant la fonction divmod()
        red = hex_color // (256 * 256)
        green = hex_color // 256 % 256
        blue = hex_color % 256
        # retournez le tuple RGB
        return red, green, blue

    def cie76(self, color1, color2):
        """
            La fonction cie76 calcule la distance de couleur entre deux 
            couleurs en utilisant le modèle de couleur CIELab.

            Le modèle CIELab est un modèle de couleur perceptuellement 
            uniforme, ce qui signifie que la distance entre les couleurs 
            dans l'espace CIELab reflète de manière fiable la distance perçue 
            par l'œil humain entre les couleurs. La distance entre deux 
            couleurs dans l'espace CIELab est donc un bon indicateur de la 
            similitude perçue des couleurs.

            La fonction cie76 calcule d'abord les composantes de 
            couleur L, a et b pour chaque couleur en utilisant des formules 
            qui convertissent les valeurs de couleur RVB (rouge, vert, bleu) 
            en composantes de couleur L, a et b. La composante L représente 
            la luminance (lumière) de la couleur, tandis que les 
            composantes a et b représentent les teintes (couleurs).

            Ensuite, la fonction calcule la distance entre les deux couleurs 
            en utilisant la formule suivante:

            distance = (L1 - L2) ** 2 + (a1 - a2) ** 2 + (b1 - b2) ** 2

            Cette formule calcule la distance entre les composantes L, a et b 
            de chaque couleur, puis calcule la racine carrée de la somme 
            de ces distances au carré. La distance ainsi calculée est une 
            mesure de la différence perçue entre les deux couleurs.

            Enfin, la fonction cie76 retourne la distance ainsi calculée.
        """
        r1, g1, b1 = self.hex_to_rgb(color1)
        r2, g2, b2 = self.hex_to_rgb(color2)
        l1 = 0.2126 * r1 + 0.7152 * g1 + 0.0722 * b1
        l2 = 0.2126 * r2 + 0.7152 * g2 + 0.0722 * b2
        a1 = 0.5 * (2 * r1 - g1 - b1)
        a2 = 0.5 * (2 * r2 - g2 - b2)
        b1 = 0.5 * (2 * b1 - r1 - g1)
        b2 = 0.5 * (2 * b2 - r2 - g2)
        distance = (l1 - l2) ** 2 + (a1 - a2) ** 2 + (b1 - b2) ** 2
        return distance

    def update_image(self, image):
        self.image = image
        self.generate_image()
        
    def save_as_image(self):
        # Capture de l'image du widget dans un objet QPixmap
        pixmap = QPixmap(self.ascii_label.width(), self.ascii_label.height())
        self.ascii_label.render(pixmap)
        scaled_pixmap = pixmap.scaled(
            self.ascii_width*10, self.ascii_height*10
        )

        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        # Sauvegarde de l'image dans un fichier
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Enregistrer l'image",
            "",
            "Images PNG (*.png);;Tous les fichiers (*)",
            options=options
        )
        if file_name:
            # Enregistrez l'image PIL dans le format souhaité
            scaled_pixmap.save(file_name, "png", quality=100)
