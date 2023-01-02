def get_help_text(index):
    if index == 0:
        # Mettre à jour le texte pour la QTab self.image_widget
        return """
Ouvrez une image avant 
d'appuyer sur Selectionner.

Vous pouvez selectionner 
une partie de votre image
en glissant-déposant 
votre souris sur celle-ci.

Vous pouvez également 
déplacer la zone 
selectionnée en la 
glissant-déposant.

Cliquer sur Selectionner
vous transferera 
automatiquement à l'étape
d'après, sauf si vous
n'avez pas ajouté
d'image.
        """
    elif index == 1:
        # Mettre à jour le texte pour la QTab self.ascii_widget
        return """
Sélectionnez une image 
avant de générer l'ASCII.

Vous pouvez changer
le fond si cela vous permet
d'avoir un meilleur rendu.

Vous pouvez convertir l'ASCII
de deux façons:
- en SFE :
Cette manière est la seule 
compatible pour ZOS R1.10

- en SF/SA :
Il existe des mainframes
qui utilisent un protocole
permettant de gérer les 
couleurs adjacentes.

Veuillez à bien vous renseigner
avant toute manipulation. Cela
pourrait causer la perte de 
votre système.

Prevoyez un Back-up.

Vous pouvez également 
partager votre rendu 
en la sauvegardant
en .png
        """
    elif index == 2:
        # Mettre à jour le texte pour la QTab self.prompt
        return """
Vous pouvez modifier les
HELPERS qui sont affichés
à l'écran d'accueil de ZOS.

Si toutefois vous voulez 
revenir en arrière, vous
pourrez réinitialiser
les textes aux valeurs
d'origine.

Cliquez sur Enregistrer pour
enregistrer toutes vos 
modifications.

Attention :
- Le texte ne doit pas
dépasser 49 caractères
- Ne doit pas contenir
de double quotes

Pour des raisons de 
liberté, ce n'est pas 
bloquant pour la 
génération du JCL.

Toutefois, les lignes 
apparaitrons en rouge
à la modification 
pour vous le faire savoir.

        """
