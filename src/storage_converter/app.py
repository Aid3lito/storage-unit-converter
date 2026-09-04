import sys
import tkinter as tk
from tkinter import ttk
from . import converter


# ==============================
# CONSTANTES
# ==============================

LARGEUR_FENETRE = 800
HAUTEUR_MIN_FENETRE = 800

PLACEHOLDER = "e.g. 100"

MAX_HISTORIQUE = 10

SEUIL_NOTATION_SCIENTIFIQUE = 0.0001

OPERATION_CONVERSION = "Conversion"
OPERATION_ADDITION = "Addition"
OPERATION_SOUSTRACTION = "Subtraction"

OPERATIONS = (
    OPERATION_CONVERSION,
    OPERATION_ADDITION,
    OPERATION_SOUSTRACTION
)

OPERATION_DEFAUT = OPERATION_CONVERSION

UNITE_ENTREE_DEFAUT = "GB - GigaByte"
UNITE_RESULTAT_DEFAUT = "GiB - GibiByte"

EXPOSANTS_UNICODE = str.maketrans(
    "0123456789-",
    "⁰¹²³⁴⁵⁶⁷⁸⁹⁻"
)

TEXTE_RESULTAT_DEFAUT = "Result:"

COULEUR_TEXTE = "#000000"
COULEUR_CHAMP = "#FFFFFF"

lignes_valeurs = []
historique = []

class ValeurNegativeError(Exception):
    pass

class ResultatNegatifError(Exception):
    pass





# ==============================
# FENÊTRE
# ==============================

fenetre = tk.Tk()
fenetre.title("Storage Unit Converter")
fenetre.geometry(
    f"{LARGEUR_FENETRE}x{HAUTEUR_MIN_FENETRE}"
)


style = ttk.Style()

style.configure(
    "Custom.TMenubutton",
    foreground="black"
)

style.configure(
    "Custom.TButton",
    foreground="black"
)





# ==============================
# FONCTIONS
# ==============================


# GESTION DES PLACEHOLDERS

def effacer_placeholder(event):
    entree = event.widget

    if entree.get() == PLACEHOLDER:
        entree.delete(0, tk.END)
        entree.config(fg="black")

def remettre_placeholder(event):
    entree = event.widget

    if entree.get() == "":
        entree.insert(0, PLACEHOLDER)
        entree.config(fg="grey")

def retirer_focus_entree(event):
    if isinstance(event.widget, (tk.Tk, tk.Frame, tk.Label)):
        fenetre.focus_set()





# RÉCUPERATION DES VALEURS

def recuperer_valeurs():
    valeurs = []

    for ligne in lignes_valeurs:
        valeur = float(
            ligne["entree"].get().strip().replace(",", ".")
        )

        if valeur < 0:
            raise ValeurNegativeError

        unite = ligne["unite"].get().split(" - ")[1]

        valeurs.append({
            "valeur": valeur,
            "unite": unite
        })

    return valeurs





# CALCULS

def effectuer_calcul(valeurs, choix_operation, unite_arrivee):
    if choix_operation == OPERATION_CONVERSION:
        premiere_ligne = valeurs[0]

        return converter.convertir(
            premiere_ligne["valeur"],
            premiere_ligne["unite"],
            unite_arrivee
        )

    if choix_operation == OPERATION_ADDITION:
        resultat = 0

        for element in valeurs:
            resultat += converter.convertir(
                element["valeur"],
                element["unite"],
                unite_arrivee
            )

        return resultat

    if choix_operation == OPERATION_SOUSTRACTION:
        premier_element = valeurs[0]

        resultat = converter.convertir(
            premier_element["valeur"],
            premier_element["unite"],
            unite_arrivee
        )

        for element in valeurs[1:]:
            resultat -= converter.convertir(
                element["valeur"],
                element["unite"],
                unite_arrivee
            )

        if resultat < 0:
            raise ResultatNegatifError

        return resultat





# CONSTRUCTION DU TEXTE DE L'HISTORIQUE

def construire_texte_historique(
    valeurs,
    choix_operation,
    resultat_formate,
    acronyme_resultat
):
    elements_historique = []

    for element in valeurs:
        valeur_formatee = formater_nombre(element["valeur"])
        acronyme = converter.toutes_les_units[
            element["unite"]
        ]["acronyme"]

        elements_historique.append(
            f"{valeur_formatee} {acronyme}"
        )

    if choix_operation == OPERATION_CONVERSION:
        return (
            f"{elements_historique[0]} → "
            f"{resultat_formate} {acronyme_resultat}"
        )

    if choix_operation == OPERATION_ADDITION:
        return (
            " + ".join(elements_historique)
            + f" = {resultat_formate} {acronyme_resultat}"
        )

    if choix_operation == OPERATION_SOUSTRACTION:
        return (
            " - ".join(elements_historique)
            + f" = {resultat_formate} {acronyme_resultat}"
        )





# AFFICHAGE DU RÉSULTAT
def afficher_resultat(resultat, unite_arrivee):
    acronyme_resultat = converter.toutes_les_units[
        unite_arrivee
    ]["acronyme"]

    resultat_formate = formater_nombre(resultat)

    label_resultat.config(
        text=f"{TEXTE_RESULTAT_DEFAUT} {resultat_formate} {acronyme_resultat}"
    )

    return resultat_formate, acronyme_resultat

def afficher_erreur(message):
    label_resultat.config(
        text=message
    )





# LANCEMENT DU CALCUL

def lancer_calcul(event=None):
    try:
        choix_operation = operation.get()
        unite_arrivee = unite_resultat.get().split(" - ")[1]

        valeurs = recuperer_valeurs()

        resultat = effectuer_calcul(
            valeurs,
            choix_operation,
            unite_arrivee
        )

        # Affichage
        resultat_formate, acronyme_resultat = afficher_resultat(
            resultat,
            unite_arrivee
        )

        # Ajout à l'historique
        texte_operation = construire_texte_historique(
            valeurs,
            choix_operation,
            resultat_formate,
            acronyme_resultat
        )

        ajouter_historique(texte_operation)

    except ResultatNegatifError:
        afficher_erreur(
            "Operation impossible: the result cannot be negative."
        )

    except ValeurNegativeError:
        afficher_erreur(
            "Invalid value: please enter a positive number."
        )

    except ValueError:
        afficher_erreur(
            "Invalid value: please enter a number."
        )





# COPIER

def copier_resultat():
    texte = label_resultat.cget("text")

    if not texte.startswith(f"{TEXTE_RESULTAT_DEFAUT} "):
        return

    fenetre.clipboard_clear()
    fenetre.clipboard_append(texte)
    fenetre.update()

    bouton_copier.config(text="Copied ✓")

    fenetre.after(
        1500,
        lambda: bouton_copier.config(text="Copy")
    )





# MISE À JOUR DYNAMIQUE DE L'INTERFACE

def mettre_a_jour_interface():
    choix_operation = operation.get()
    minimum = nombre_minimum_lignes()

    if choix_operation == OPERATION_CONVERSION:
        while len(lignes_valeurs) > minimum:
            ligne = lignes_valeurs.pop()
            ligne["frame"].destroy()

        bouton_ajouter_valeur.pack_forget()

    else:
        while len(lignes_valeurs) < minimum:
            ajouter_ligne_valeur()

        bouton_ajouter_valeur.pack(pady=10)

    ajuster_hauteur_fenetre()





# CRÉATION DES MENUS D'UNITÉS

def ajouter_groupe_unites(menu, titre, unites, variable):
    menu.add_command(
        label=f"--- {titre} ---",
        state="disabled"
    )

    for nom, donnees in unites.items():
        texte = f'{donnees["acronyme"]} - {nom}'

        menu.add_command(
            label=texte,
            command=lambda valeur=texte: variable.set(valeur)
        )

def creer_menu_unites(parent, variable):
    if sys.platform == "win32":
        bouton = tk.Menubutton(
            parent,
            textvariable=variable,
            width=20,
            relief="raised",
            borderwidth=1,
            padx=6,
            pady=3,
            fg="black",
            indicatoron=True
        )
    else:
        bouton = ttk.Menubutton(
            parent,
            textvariable=variable,
            width=20,
            style="Custom.TMenubutton"
        )

    menu = tk.Menu(
        bouton,
        tearoff=0
    )

    bouton["menu"] = menu

    ajouter_groupe_unites(
        menu,
        "Decimal",
        converter.units_decimal,
        variable
    )

    menu.add_separator()

    ajouter_groupe_unites(
        menu,
        "Binary",
        converter.units_binary,
        variable
    )

    return bouton





# CRÉATION DU MENU DES OPÉRATIONS

def basculer_menu(bouton, menu):
    if getattr(bouton, "_menu_ouvert", False):
        menu.unpost()
        bouton._menu_ouvert = False
        return

    x = bouton.winfo_rootx()
    y = bouton.winfo_rooty() + bouton.winfo_height()

    bouton._menu_ouvert = True
    menu.post(x, y)



def creer_menu_operations(parent, variable):
    if sys.platform == "win32":
        bouton = tk.Menubutton(
            parent,
            textvariable=variable,
            width=20,
            relief="raised",
            borderwidth=1,
            padx=6,
            pady=3,
            fg="black",
            indicatoron=True
        )
    else:
        bouton = ttk.Menubutton(
            parent,
            textvariable=variable,
            width=20,
            style="Custom.TMenubutton"
        )

    menu = tk.Menu(
        bouton,
        tearoff=0
    )

    bouton["menu"] = menu

    if sys.platform == "win32":
        bouton.config(
            command=lambda: basculer_menu(bouton, menu)
        )

    menu.bind(
        "<Unmap>",
        lambda event: setattr(bouton, "_menu_ouvert", False)
    )

    def choisir_operation(valeur):
        variable.set(valeur)
        mettre_a_jour_interface()

    for choix in OPERATIONS:
        menu.add_command(
            label=choix,
            command=lambda valeur=choix: choisir_operation(valeur)
        )

    return bouton





# REDIMENSIONNEMENT AUTOMATIQUE

def ajuster_hauteur_fenetre():
    fenetre.update_idletasks()

    hauteur_necessaire = fenetre.winfo_reqheight()
    largeur_actuelle = fenetre.winfo_width()

    hauteur = max(
        HAUTEUR_MIN_FENETRE,
        hauteur_necessaire
)

    fenetre.geometry(
        f"{largeur_actuelle}x{hauteur}"
    )





# RÉINITIALISATION

def reinitialiser_interface():

    # Supprime toutes les lignes existantes
    for ligne in lignes_valeurs:
        ligne["frame"].destroy()

    lignes_valeurs.clear()

    # Recrée une seule ligne par défaut
    ajouter_ligne_valeur()

    # Réinitialise l'unité de résultat
    unite_resultat.set(UNITE_RESULTAT_DEFAUT)

    # Retour en mode Conversion
    operation.set(OPERATION_DEFAUT)

    mettre_a_jour_interface()

    # Réinitialise le résultat
    label_resultat.config(
        text=TEXTE_RESULTAT_DEFAUT
    )





# GESTION DES MULTIVALEURS

def nombre_minimum_lignes():
    if operation.get() == OPERATION_CONVERSION:
        return 1

    return 2

def positionner_ligne_valeur(ligne, index):
    ligne["frame"].grid(
        row=index,
        column=0,
        columnspan=3,
        pady=5
    )

# Suppression d'une ligne de valeurs
def supprimer_ligne_valeur(ligne):
    minimum = nombre_minimum_lignes()

    if len(lignes_valeurs) <= minimum:
        return

    ligne["frame"].destroy()
    lignes_valeurs.remove(ligne)

    # Repositionnement des lignes restantes
    for index, ligne_restante in enumerate(lignes_valeurs):
        positionner_ligne_valeur(
            ligne_restante,
            index
        )

    ajuster_hauteur_fenetre()



def creer_entree_valeur(parent):
    entree = tk.Entry(
        parent,
        width=20,
        bg=COULEUR_CHAMP,
        fg=COULEUR_TEXTE,
        insertbackground=COULEUR_TEXTE
    )

    entree.insert(0, PLACEHOLDER)
    entree.config(fg="grey")

    entree.bind("<FocusIn>", effacer_placeholder)
    entree.bind("<FocusOut>", remettre_placeholder)

    return entree

def creer_bouton_suppression(parent):
    return ttk.Button(
        parent,
        text="×",
        width=1,
        style="Custom.TButton"
    )

def creer_ligne_valeur():

    frame_ligne = tk.Frame(frame_valeurs)

    entree = creer_entree_valeur(frame_ligne)

    unite = tk.StringVar(
        value=UNITE_ENTREE_DEFAUT
    )

    menu_unite = creer_menu_unites(
        frame_ligne,
        unite
    )

    bouton_supprimer = creer_bouton_suppression(
        frame_ligne
    )

    entree.grid(
        row=0,
        column=0,
        padx=5
    )

    menu_unite.grid(
        row=0,
        column=1,
        padx=5
    )

    bouton_supprimer.grid(
        row=0,
        column=2,
        padx=(2, 5)
    )

    ligne = {
        "frame": frame_ligne,
        "entree": entree,
        "unite": unite,
        "bouton_supprimer": bouton_supprimer
    }

    bouton_supprimer.config(
        command=lambda: supprimer_ligne_valeur(ligne)
    )

    return ligne

# Ajout d'une ligne de valeurs
def ajouter_ligne_valeur():
    ligne = creer_ligne_valeur()

    lignes_valeurs.append(ligne)

    positionner_ligne_valeur(
        ligne,
        len(lignes_valeurs) - 1
    )

    ajuster_hauteur_fenetre()


# Formatage intelligent des nombres

def formater_nombre(nombre):
    if nombre == 0:
        return "0"

    valeur_absolue = abs(nombre)

    # Très petites valeurs : notation scientifique
    if valeur_absolue < SEUIL_NOTATION_SCIENTIFIQUE:
        coefficient, exposant = f"{nombre:.2e}".split("e")

        coefficient = float(coefficient)

        if coefficient.is_integer():
            coefficient = int(coefficient)
            coefficient_texte = str(coefficient)
        else:
            coefficient_texte = str(coefficient)

        exposant = int(exposant)

        exposant_texte = str(exposant).translate(EXPOSANTS_UNICODE)

        return f"{coefficient_texte} × 10{exposant_texte}"

    # Valeurs comprises entre 0,0001 et 0,01 :
    # conservation de plusieurs décimales
    if valeur_absolue < 0.01:
        texte = f"{nombre:,.8f}"

    # Valeurs entières
    elif nombre.is_integer():
        texte = f"{int(nombre):,}"

    # Valeurs décimales classiques
    else:
        texte = f"{nombre:,.3f}"

    if "." in texte:
        texte = texte.rstrip("0").rstrip(".")

    return texte






# GESTION DE L'HISTORIQUE

# Ajouter une valeur à l'historique
def ajouter_historique(texte):
    historique.insert(0, texte)

    if len(historique) > MAX_HISTORIQUE:
        historique.pop()

    mettre_a_jour_historique()

# Mettre à jour l'historique
def mettre_a_jour_historique():
    liste_historique.delete(0, tk.END)

    for entree in historique:
        liste_historique.insert(tk.END, entree)

    liste_historique.yview_moveto(0)

# Supprimer l'historique
def effacer_historique():
    historique.clear()
    mettre_a_jour_historique()





# ==============================
# CONSTRUCTION DE L'INTERFACE
# ==============================


# TITRE

titre = tk.Label(
    fenetre,
    text="Storage Unit Converter",
    font=("Arial", 20, "bold"),
    fg=COULEUR_TEXTE
)
titre.pack(pady=20)





# SÉLECTION DE L'OPÉRATION

label_operation = tk.Label(
    fenetre,
    text="Operation",
    fg=COULEUR_TEXTE
)
label_operation.pack(pady=10)

operation = tk.StringVar()

menu_operation = creer_menu_operations(
    fenetre,
    operation
)

operation.set(OPERATION_DEFAUT)
menu_operation.pack()





# CONTENEUR DES VALEURS

frame_valeurs = tk.Frame(fenetre)
frame_valeurs.pack(pady=20)

frame_ajout = tk.Frame(fenetre)

frame_ajout.pack()

ajouter_ligne_valeur()

bouton_ajouter_valeur = ttk.Button(
    frame_ajout,
    text="+ Add value",
    command=ajouter_ligne_valeur,
    style="Custom.TButton"
)





# UNITÉ DE RÉSULTAT

label_unite_resultat = tk.Label(
    fenetre,
    text="Result unit",
    fg=COULEUR_TEXTE
)
label_unite_resultat.pack(pady=(20, 5))

unite_resultat = tk.StringVar(
    value=UNITE_RESULTAT_DEFAUT
)

menu_unite_resultat = creer_menu_unites(
    fenetre,
    unite_resultat
)

menu_unite_resultat.pack()





# BOUTON DE CALCUL ET RÉSULTAT

frame_boutons = tk.Frame(fenetre)
frame_boutons.pack(pady=20)

# Bouton calcul
bouton_calculer = ttk.Button(
    frame_boutons,
    text="Calculate",
    command=lancer_calcul,
    style="Custom.TButton"
)
bouton_calculer.pack(side="left", padx=10)

# Bouton réinitialiser
bouton_reinitialiser = ttk.Button(
    frame_boutons,
    text="Reset",
    command=reinitialiser_interface,
    style="Custom.TButton"
)
bouton_reinitialiser.pack(side="left", padx=10)

# Bouton copier
bouton_copier = ttk.Button(
    frame_boutons,
    text="Copy",
    command=copier_resultat,
    style="Custom.TButton"
)
bouton_copier.pack(side="left", padx=10)

# Résultat
label_resultat = tk.Label(
    fenetre,
    text=TEXTE_RESULTAT_DEFAUT,
    font=("Arial", 14, "bold"),
    fg=COULEUR_TEXTE
)
label_resultat.pack(pady=20)

# Historique
titre_historique = tk.Label(
    fenetre,
    text="History",
    font=("Arial", 12, "bold"),
    fg=COULEUR_TEXTE
)
titre_historique.pack(pady=(10, 5))

frame_historique = tk.Frame(fenetre)
frame_historique.pack(pady=5)

liste_historique = tk.Listbox(
    frame_historique,
    width=60,
    height=6,
    bg=COULEUR_CHAMP,
    fg=COULEUR_TEXTE,
    selectbackground="#0078D7",
    selectforeground="white"
)

scrollbar_historique = tk.Scrollbar(
    frame_historique,
    orient="vertical",
    command=liste_historique.yview
)

liste_historique.config(
    yscrollcommand=scrollbar_historique.set
)

liste_historique.pack(
    side="left",
    fill="both"
)

scrollbar_historique.pack(
    side="right",
    fill="y"
)

# Bouton effacer
bouton_effacer_historique = ttk.Button(
    fenetre,
    text="Clear History",
    command=effacer_historique,
    style="Custom.TButton"
)
bouton_effacer_historique.pack(pady=10)





# <ENTER> lance le calcul
fenetre.bind("<Return>", lancer_calcul)

# Cliquer en dehors des zones de texte pour désélectionner
fenetre.bind("<Button-1>", retirer_focus_entree, add="+")



fenetre.mainloop()