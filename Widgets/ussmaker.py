from PyQt5.QtWidgets import (
                            QWidget,
                            QFileDialog,
                            QPushButton,
                            QVBoxLayout,
)

from Configuration.settings import COLORS, HEX_TO_COLORS, forbidden
from Presets.ussskeleton import PART1, PART2


class USSMaker(QWidget):
    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.text_list = None
        self.color_list = None

        self.ascii_width = 80
        self.pixels = list()
        self.sep_pixels = list()

        self.make_uss = QPushButton("Créer JCL", self)
        self.make_uss.clicked.connect(self.make_jcl)

        # utilisez un layout pour organiser les widgets
        layout = QVBoxLayout(self) 
        layout.addWidget(self.make_uss)


    def convert_hex(self, row, col):
        """
            Methode qui retourne l'addresse HEX de chaque bloc de texte
            Spécifique à USS.
        """
        return hex(0x110000 + (row)*self.ascii_width - 1 + col)

    def regroup_pixels(self, pixels):
        """
            Methode qui prend une liste d'objets représentant des pixels et 
            retourne une liste d'objets regroupés selon leur couleur
        """
        result = []
        current_object = None
        for pixel in pixels:
            if current_object is None:
                # On commence un nouvel objet si on en a pas encore créé un
                current_object = pixel
            elif pixel['c'] == current_object['c']:
                # Si la couleur de l'objet courant est la même que celle de l'objet en cours,
                # on concatène les symboles des deux objets
                current_object['s'] += pixel['s']
            else:
                # Si la couleur de l'objet courant est différente de celle de l'objet en cours,
                # on ajoute l'objet en cours à la liste résultat et on crée un nouvel objet à partir de l'objet courant
                if current_object['c'] != "#000000":  # On ignore les objets noirs
                    result.append(current_object)
                current_object = pixel

        # On ajoute l'objet en cours s'il n'est pas noir
        if current_object is not None and current_object['c'] != "#000000":
            result.append(current_object)
        return result

    def command(self, pixel: dict):
        """
            Methode qui s'occupe de générer les instructions unitairement pour
            les textes à afficher sur le WALLPAPER.
        """
        row = pixel.get('y')
        col = pixel.get('x')
        index_x = self.convert_hex(row, col)
        index = (row)*self.ascii_width - 1 + col
        text = pixel.get('s', ' ')
        colore = HEX_TO_COLORS.get(pixel.get('c'), 'WHITE')
        if len(text) > 40:
            return f"""
         DC    X'{index_x.upper().replace('0X', '')}'               SBA, {index:04}     ROW {(pixel.get('y')):02} COL {pixel.get('x'):02}
         DC    X'290242{COLORS.get(colore).get('ibm')}C0E0'         SFE, PROTECTED/NORMAL/{colore}
         DC    C'{text[:40]}'
         DC    C'{text[40:]}'"""
        else:
            return f"""
         DC    X'{index_x.upper().replace('0X', '')}'               SBA, {index:04}     ROW {(pixel.get('y')):02} COL {pixel.get('x'):02}
         DC    X'290242{COLORS.get(colore).get('ibm')}C0E0'         SFE, PROTECTED/NORMAL/{colore}
         DC    C'{text}'"""

    def truc(self):
        """ 
            Methode qui prend une liste d'objets représentant des pixels et 
            retourne une liste concaténée de ces objets, en divisant la liste
            originale en plusieurs sous-listes de longueur ascii_width
        """
        pixels_lbl = []
        for k in range(len(self.pixels)//self.ascii_width):
            a= k*self.ascii_width
            b= (k+1)*self.ascii_width
            pixels_lbl.append(self.regroup_pixels(self.pixels[a:b]))
        pixels_full = []
        for pixs in pixels_lbl:
            pixels_full += pixs
        return pixels_full

    def make_jcl(self):
        """
            Methode qui génère le JCL
        """
        if not self.text_list and not self.color_list:
            return
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(self, "Enregistrer le script", "", "Scripts JCL (*.jcl);;Tous les fichiers (*)", options=options)
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as f:
                print(f"Write on file : {file_name}.", end='')
                # Part 1
                f.write(PART1)
                print(".", end="-")

                #!SECTION
                pixels = self.truc()
                # LOGO Part                                                 
                counter = 1
                for pixel in pixels:       
                    f.write(self.command(pixel))  # white
                # Part 2
                f.write(PART2)
                print(".", end=" ")
                # 
                print("Done")

    def update_ascii(self, text_list, color_list):
        """
            Methode qui met à jour les pixels qui sont dans la zone d'édition
            QTextEditor (module ascii)
        """
        self.text_list = text_list
        self.color_list = color_list
        self.pixels = list()
        if self.text_list and self.color_list:
            for i, line in enumerate(self.text_list):
                for j, char in enumerate(line):
                    char = char if char not in forbidden['ascii_chars'] else '8'
                    col = j % 80
                    row = i
                    this_pixel = {
                        'x': col,
                        'y': row,
                        's': char,
                        'c': self.color_list[i][j].name(),
                    }
                    self.pixels.append(this_pixel)
