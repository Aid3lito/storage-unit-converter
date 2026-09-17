import sys
import tkinter as tk

from pathlib import Path
from tkinter import ttk
from .localization.manager import LocalizationManager
from .ui.settings_window import ouvrir_fenetre_parametres

from . import converter
from . import history_store
from . import preferences

from .ui.theme import (
    THEMES,
    THEME_DEFAUT,
    configurer_styles_ttk,
    obtenir_theme,
)



# ==============================
# CONSTANTES
# ==============================

LARGEUR_FENETRE = 800
HAUTEUR_MIN_FENETRE = 800

PLACEHOLDER = "e.g. 100"

MAX_HISTORIQUE = 10

SEUIL_NOTATION_SCIENTIFIQUE = 0.0001

OPERATION_CONVERSION = "conversion"
OPERATION_ADDITION = "addition"
OPERATION_SOUSTRACTION = "subtraction"

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

def texte_resultat_defaut():
    return tr("label.result")

theme_actuel = THEME_DEFAUT

PADDING_RESULT_LABEL = (3, 3)
PADDING_RESULT_MENU = (0, 5)
PADDING_SWAP = (8, 18)

lignes_valeurs = []
historique = []

LANGUES_DISPONIBLES = (
    "en",
    "fr",
)

fenetre_parametres = None

DOSSIER_LOCALISATION = (
    Path(__file__).resolve().parent
    / "localization"
)

localization = LocalizationManager(
    DOSSIER_LOCALISATION,
    language="en",
)


def tr(key):
    return localization.translate(key)


def obtenir_libelle_operation(operation_id):
    return tr(f"operation.{operation_id}")

def appliquer_langue():
    fenetre.title(
        tr("app.title")
    )

    label_operation.config(
        text=tr("label.operation")
    )

    label_unite_resultat.config(
        text=tr("label.result_unit")
    )

    bouton_ajouter_valeur.config(
        text=tr("button.add_value")
    )

    bouton_inverser_unites.config(
        text=tr("button.swap_units")
    )

    bouton_calculer.config(
        text=tr("button.calculate")
    )

    bouton_reinitialiser.config(
        text=tr("button.reset")
    )

    bouton_copier.config(
        text=tr("button.copy")
    )

    titre_historique.config(
        text=tr("section.history")
    )

    bouton_effacer_historique.config(
        text=tr("button.clear_history")
    )

    operation_affichage.set(
        obtenir_libelle_operation(
            operation.get()
        )
    )

    mettre_a_jour_menu_operations()

    for ligne in lignes_valeurs:
        mettre_a_jour_menu_unites(
            ligne["menu_unite"]
        )

    mettre_a_jour_menu_unites(
        menu_unite_resultat
    )

    label_resultat.config(
        text=texte_resultat_defaut()
    )

    appliquer_theme()

def changer_langue(langue):
    if langue not in LANGUES_DISPONIBLES:
        return

    if localization.language == langue:
        return

    localization.set_language(langue)

    appliquer_langue()
    sauvegarder_preferences()

class ValeurNegativeError(Exception):
    pass


class ResultatNegatifError(Exception):
    pass


def appliquer_theme():
    theme = obtenir_theme(theme_actuel)

    if theme_actuel == "dark":
        bouton_theme.config(
            text="☀"
        )
    else:
        bouton_theme.config(
            text="☾"
        )

    fenetre.configure(
        bg=theme["background"]
    )

    for widget in (
        label_operation,
        label_unite_resultat,
        label_resultat,
        titre_historique
    ):
        widget.configure(
            bg=theme["background"],
            fg=theme["text"]
        )

    for frame in (
        frame_valeurs,
        frame_ajout,
        frame_boutons,
        frame_historique
    ):
        frame.configure(
            bg=theme["background"]
        )

    for ligne in lignes_valeurs:
        ligne["frame"].configure(
            bg=theme["background"]
        )

        entree = ligne["entree"]

        if entree.get() == PLACEHOLDER:
            couleur_texte = theme["placeholder"]
        else:
            couleur_texte = theme["text"]

        entree.configure(
            bg=theme["field"],
            fg=couleur_texte,
            insertbackground=theme["text"]
        )

    liste_historique.configure(
        bg=theme["field"],
        fg=theme["text"],
        selectbackground=theme["selection"],
        selectforeground=theme["selection_text"]
    )

    configurer_styles_ttk(style, theme)

def basculer_theme():
    nouveau_theme = (
        "dark"
        if theme_actuel == "light"
        else "light"
    )

    changer_theme(nouveau_theme)

def changer_theme(nouveau_theme):
    global theme_actuel

    if nouveau_theme not in THEMES:
        return

    if theme_actuel == nouveau_theme:
        return

    theme_actuel = nouveau_theme

    appliquer_theme()
    sauvegarder_preferences()

def ouvrir_parametres():
    global fenetre_parametres

    fenetre_parametres = ouvrir_fenetre_parametres(
        fenetre,
        tr,
        localization.language,
        changer_langue,
        theme_actuel,
        changer_theme,
        obtenir_langue_actuelle,
        obtenir_theme_actuel,
        fenetre_parametres,
    )

def obtenir_langue_actuelle():
    return localization.language


def obtenir_theme_actuel():
    return theme_actuel

# ==============================
# MÉMOIRE
# ==============================

def obtenir_dossier_donnees():
    if sys.platform == "win32":
        dossier_base = Path.home() / "AppData" / "Roaming"
        return dossier_base / "StorageUnitConverter"

    if sys.platform == "darwin":
        return (
            Path.home()
            / "Library"
            / "Application Support"
            / "StorageUnitConverter"
        )

    return (
        Path.home()
        / ".config"
        / "storage-unit-converter"
    )

DOSSIER_DONNEES = obtenir_dossier_donnees()
FICHIER_HISTORIQUE = DOSSIER_DONNEES / "history.json"
FICHIER_PREFERENCES = DOSSIER_DONNEES / "preferences.json"


# ==============================
# FENÊTRE
# ==============================

fenetre = tk.Tk()
fenetre.title(
    tr("app.title")
)


if sys.platform.startswith("linux"):
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        chemin_icone = (
            Path(sys._MEIPASS)
            / "assets"
            / "icons"
            / "app-icon.png"
        )
    else:
        chemin_icone = (
            Path(__file__).resolve().parents[2]
            / "assets"
            / "icons"
            / "app-icon.png"
        )

    if chemin_icone.exists():
        icone_application = tk.PhotoImage(
            file=str(chemin_icone)
        )
        fenetre.iconphoto(
            True,
            icone_application
        )

style = ttk.Style()

if sys.platform in ("darwin", "win32"):
    style.theme_use("clam")

configurer_styles_ttk(
    style,
    obtenir_theme(theme_actuel)
)




# ==============================
# FONCTIONS
# ==============================


# GESTION DES PLACEHOLDERS

def effacer_placeholder(event):
    entree = event.widget

    if entree.get() == PLACEHOLDER:
        entree.delete(0, tk.END)
        entree.config(
            fg=obtenir_theme(theme_actuel)["text"]
        )

def remettre_placeholder(event):
    entree = event.widget

    if entree.get() == "":
        entree.insert(0, PLACEHOLDER)
        entree.config(fg=obtenir_theme(theme_actuel)["placeholder"])

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


def obtenir_unites_affichage():
    unites = []

    for groupe in (
        converter.units_decimal,
        converter.units_binary
    ):
        for nom, donnees in groupe.items():
            unites.append(
                f'{donnees["acronyme"]} - {nom}'
            )

    return unites


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
        text=f"{texte_resultat_defaut()} {resultat_formate} {acronyme_resultat}"
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
            tr("error.negative_result")
        )

    except ValeurNegativeError:
        afficher_erreur(
            tr("error.negative_value")
        )

    except ValueError:
        afficher_erreur(
            tr("error.invalid_value")
        )





# COPIER

def copier_resultat():
    texte = label_resultat.cget("text")

    if not texte.startswith(f"{texte_resultat_defaut()} "):
        return

    fenetre.clipboard_clear()
    fenetre.clipboard_append(texte)
    fenetre.update()

    bouton_copier.config(
        text=tr("button.copied")
    )

    fenetre.after(
        1500,
        lambda: bouton_copier.config(
            text=tr("button.copy")
        )
    )


def inverser_unites():
    if operation.get() != OPERATION_CONVERSION:
        return
    
    if not lignes_valeurs:
        return

    unite_source = lignes_valeurs[0]["unite"].get()
    unite_cible = unite_resultat.get()

    lignes_valeurs[0]["unite"].set(unite_cible)
    unite_resultat.set(unite_source)

    label_resultat.config(
        text=texte_resultat_defaut()
    )


# MISE À JOUR DYNAMIQUE DE L'INTERFACE

def mettre_a_jour_interface():
    choix_operation = operation.get()
    minimum = nombre_minimum_lignes()

    if choix_operation == OPERATION_CONVERSION:
        while len(lignes_valeurs) > minimum:
            ligne = lignes_valeurs.pop()
            ligne["frame"].destroy()

        lignes_valeurs[0]["bouton_supprimer"].grid_remove()

        bouton_ajouter_valeur.pack_forget()
        frame_ajout.pack_forget()

        bouton_inverser_unites.pack(
            pady=PADDING_SWAP,
            before=frame_boutons
        )

    else:
        while len(lignes_valeurs) < minimum:
            ajouter_ligne_valeur()
        
        for ligne in lignes_valeurs:
            ligne["bouton_supprimer"].grid()

        frame_ajout.pack(
            before=label_unite_resultat
        )

        bouton_ajouter_valeur.pack(
            pady=10
        )

        bouton_inverser_unites.pack_forget()

    ajuster_hauteur_fenetre()
    focus_premiere_ligne_vide()




# CRÉATION DES MENUS D'UNITÉS

def definir_unite(variable, valeur):
    variable.set(valeur)
    sauvegarder_preferences()

def ajouter_groupe_unites(menu, titre, unites, variable):
    menu.add_command(
        label=f"--- {titre} ---",
        state="disabled"
    )

    for nom, donnees in unites.items():
        texte = f'{donnees["acronyme"]} - {nom}'

        menu.add_command(
            label=texte,
            command=lambda valeur=texte: definir_unite(
                variable,
                valeur
            )
        )

def creer_menu_unites(parent, variable):
    bouton = ttk.Menubutton(
        parent,
        textvariable=variable,
        width=22,
        style="Custom.TMenubutton"
    )

    menu = tk.Menu(
        bouton,
        tearoff=0
    )

    bouton["menu"] = menu
    bouton.menu_unites = menu

    if sys.platform == "win32":
        bouton.bind(
            "<Button-1>",
            lambda event: basculer_menu(event, bouton, menu)
        )

        menu.bind(
            "<Unmap>",
            lambda event: setattr(bouton, "_menu_ouvert", False)
        )

    ajouter_groupe_unites(
        menu,
        tr("group.decimal"),
        converter.units_decimal,
        variable
    )

    menu.add_separator()

    ajouter_groupe_unites(
        menu,
        tr("group.binary"),
        converter.units_binary,
        variable
    )

    return bouton

def mettre_a_jour_menu_unites(bouton):
    menu = bouton.menu_unites

    menu.entryconfig(
        0,
        label=f'--- {tr("group.decimal")} ---'
    )

    index_binaire = len(converter.units_decimal) + 2

    menu.entryconfig(
        index_binaire,
        label=f'--- {tr("group.binary")} ---'
    )



# CRÉATION DU MENU DES OPÉRATIONS

def basculer_menu(event, bouton, menu):
    if getattr(bouton, "_menu_ouvert", False):
        menu.unpost()
        bouton._menu_ouvert = False
    else:
        x = bouton.winfo_rootx()
        y = bouton.winfo_rooty() + bouton.winfo_height()

        bouton._menu_ouvert = True
        menu.post(x, y)

    return "break"



def creer_menu_operations(
    parent,
    variable,
    variable_affichage,
):
    bouton = ttk.Menubutton(
        parent,
        textvariable=variable_affichage,
        width=22,
        style="Custom.TMenubutton"
    )

    menu = tk.Menu(
        bouton,
        tearoff=0
    )

    bouton["menu"] = menu
    bouton.menu_operations = menu

    if sys.platform == "win32":
        bouton.bind(
            "<Button-1>",
            lambda event: basculer_menu(event, bouton, menu)
        )

        menu.bind(
            "<Unmap>",
            lambda event: setattr(bouton, "_menu_ouvert", False)
        )

    def choisir_operation(valeur):
        variable.set(valeur)

        variable_affichage.set(
            obtenir_libelle_operation(valeur)
        )

        mettre_a_jour_interface()
        sauvegarder_preferences()

    for choix in OPERATIONS:
        menu.add_command(
            label=obtenir_libelle_operation(choix),
            command=lambda valeur=choix: choisir_operation(valeur)
        )

    return bouton

def mettre_a_jour_menu_operations():
    menu = menu_operation.menu_operations

    for index, choix in enumerate(OPERATIONS):
        menu.entryconfig(
            index,
            label=obtenir_libelle_operation(choix)
        )

def definir_taille_initiale():
    fenetre.update_idletasks()

    largeur_requise = fenetre.winfo_reqwidth()
    hauteur_requise = fenetre.winfo_reqheight()

    if sys.platform.startswith("linux"):
        largeur = max(
            LARGEUR_FENETRE,
            largeur_requise + 150
        )

        hauteur = max(
            HAUTEUR_MIN_FENETRE,
            hauteur_requise + 100
        )
    else:
        largeur = max(
            LARGEUR_FENETRE,
            largeur_requise
        )

        hauteur = max(
            HAUTEUR_MIN_FENETRE,
            hauteur_requise
        )

    largeur_ecran = fenetre.winfo_screenwidth()
    hauteur_ecran = fenetre.winfo_screenheight()

    largeur = min(
        largeur,
        int(largeur_ecran * 0.95)
    )

    hauteur = min(
        hauteur,
        int(hauteur_ecran * 0.90)
    )

    position_x = max(
        (largeur_ecran - largeur) // 2,
        0
    )

    position_y = max(
        (hauteur_ecran - hauteur) // 2,
        0
    )

    fenetre.geometry(
        f"{largeur}x{hauteur}+{position_x}+{position_y}"
    )


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





# FOCUS

def ajouter_ligne_valeur_et_focus():
    ajouter_ligne_valeur()
    lignes_valeurs[-1]["entree"].focus_set()

def ajouter_valeur_raccourci(event=None):
    if operation.get() == OPERATION_CONVERSION:
        return

    ajouter_ligne_valeur_et_focus()

def focus_premiere_ligne_vide():
    cible = None

    for ligne in lignes_valeurs:
        contenu = ligne["entree"].get().strip()

        if contenu == "" or contenu == PLACEHOLDER:
            cible = ligne["entree"]
            break

    if cible is None and lignes_valeurs:
        cible = lignes_valeurs[0]["entree"]

    if cible is not None:
        fenetre.after_idle(cible.focus_set)


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
        text=texte_resultat_defaut()
    )

    lignes_valeurs[0]["entree"].focus_set()

    sauvegarder_preferences()



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
    theme = obtenir_theme(theme_actuel)

    entree = tk.Entry(
        parent,
        width=22,
        bg=theme["field"],
        fg=theme["text"],
        insertbackground=theme["text"],
        highlightthickness=2,
        highlightbackground=theme["background"],
        highlightcolor=theme["selection"]
    )

    entree.insert(0, PLACEHOLDER)
    entree.config(
        fg=theme["placeholder"]
    )

    entree.bind(
        "<FocusIn>",
        effacer_placeholder
    )

    entree.bind(
        "<FocusOut>",
        remettre_placeholder
    )

    return entree

def creer_bouton_suppression(parent):
    return ttk.Button(
        parent,
        text="×",
        width=2,
        style="Custom.TButton"
    )

def creer_ligne_valeur():

    frame_ligne = tk.Frame(
        frame_valeurs,
        bg=obtenir_theme(theme_actuel)["background"]
    )

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
        padx=(5, 3)
    )

    menu_unite.grid(
        row=0,
        column=1,
        padx=(3, 5)
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
        "menu_unite": menu_unite,
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


# ==============================
# GESTION DES PRÉFÉRENCES
# ==============================

def sauvegarder_preferences():
    choix_operation = operation.get()

    source_units = []

    if lignes_valeurs:
        source_units.append(
            lignes_valeurs[0]["unite"].get()
        )

    if (
        choix_operation in (
            OPERATION_ADDITION,
            OPERATION_SOUSTRACTION
        )
        and len(lignes_valeurs) >= 2
    ):
        source_units.append(
            lignes_valeurs[1]["unite"].get()
        )

    preferences_actuelles = {
        "operation": choix_operation,
        "source_units": source_units,
        "result_unit": unite_resultat.get(),
        "theme": theme_actuel,
        "language": localization.language,
    }

    preferences.save_preferences(
        FICHIER_PREFERENCES,
        preferences_actuelles,
    )


def charger_preferences():
    global theme_actuel

    preferences_chargees = preferences.load_preferences(
        FICHIER_PREFERENCES
    )

    unites_valides = obtenir_unites_affichage()

    preferences_chargees = preferences.validate_preferences(
        preferences_chargees,
        OPERATIONS,
        unites_valides,
        THEMES,
        LANGUES_DISPONIBLES,
    )

    operation_sauvegardee = preferences_chargees.get(
        "operation"
    )

    source_units_sauvegardees = preferences_chargees.get(
        "source_units"
    )

    unite_resultat_sauvegardee = preferences_chargees.get(
        "result_unit"
    )

    theme_sauvegarde = preferences_chargees.get(
        "theme"
    )

    langue_sauvegardee = preferences_chargees.get(
        "language"
    )

    operation.set(
        operation_sauvegardee
    )

    localization.set_language(
        langue_sauvegardee
    )

    operation_affichage.set(
        obtenir_libelle_operation(operation_sauvegardee)
    )

    mettre_a_jour_interface()

    if isinstance(source_units_sauvegardees, list):
        if (len(source_units_sauvegardees) >= 1):
            lignes_valeurs[0]["unite"].set(
                source_units_sauvegardees[0]
            )

        if (
            operation.get() in (
                OPERATION_ADDITION,
                OPERATION_SOUSTRACTION
            )
            and len(lignes_valeurs) >= 2
            and len(source_units_sauvegardees) >= 2
        ):
            lignes_valeurs[1]["unite"].set(
                source_units_sauvegardees[1]
            )

    theme_actuel = theme_sauvegarde

    unite_resultat.set(
        unite_resultat_sauvegardee
    )

    appliquer_langue()



# GESTION DE L'HISTORIQUE

# Chargement de l'historique au démarrage
def charger_historique():
    historique.clear()

    historique.extend(
        history_store.load_history(
            FICHIER_HISTORIQUE,
            MAX_HISTORIQUE
        )
    )

# Sauvegarde de l'historique
def sauvegarder_historique():
    history_store.save_history(
        FICHIER_HISTORIQUE,
        historique
    )

# Ajouter une valeur à l'historique
def ajouter_historique(texte):
    historique.insert(0, texte)

    if len(historique) > MAX_HISTORIQUE:
        historique.pop()

    mettre_a_jour_historique()
    sauvegarder_historique()

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
    sauvegarder_historique()





# ==============================
# CONSTRUCTION DE L'INTERFACE
# ==============================

bouton_theme = ttk.Button(
    fenetre,
    text="☾",
    width=3,
    command=basculer_theme,
    style="Custom.TButton",
)

bouton_theme.place(
    x=20,
    y=20,
    anchor="nw",
)

bouton_parametres = ttk.Button(
    fenetre,
    text="⚙",
    width=3,
    command=ouvrir_parametres,
    style="Custom.TButton",
)

bouton_parametres.place(
    relx=1.0,
    x=-20,
    y=20,
    anchor="ne",
)

# SÉLECTION DE L'OPÉRATION

label_operation = tk.Label(
    fenetre,
    text=tr("label.operation"),
    fg=obtenir_theme(theme_actuel)["text"]
)
label_operation.pack(
    pady=(5, 5)
)

operation = tk.StringVar()
operation_affichage = tk.StringVar()

menu_operation = creer_menu_operations(
    fenetre,
    operation,
    operation_affichage
)

operation.set(OPERATION_DEFAUT)

operation_affichage.set(
    obtenir_libelle_operation(OPERATION_DEFAUT)
)

menu_operation.pack()





# CONTENEUR DES VALEURS

frame_valeurs = tk.Frame(fenetre)
frame_valeurs.pack(
    pady=(18, 15)
)

frame_ajout = tk.Frame(fenetre)

ajouter_ligne_valeur()
lignes_valeurs[0]["entree"].focus_set()
lignes_valeurs[0]["bouton_supprimer"].grid_remove()

bouton_ajouter_valeur = ttk.Button(
    frame_ajout,
    text=tr("button.add_value"),
    command=ajouter_ligne_valeur_et_focus,
    style="Custom.TButton"
)





# UNITÉ DE RÉSULTAT

label_unite_resultat = tk.Label(
    fenetre,
    text=tr("label.result_unit"),
    fg=obtenir_theme(theme_actuel)["text"]
)
label_unite_resultat.pack(
    pady=PADDING_RESULT_LABEL
)


unite_resultat = tk.StringVar(
    value=UNITE_RESULTAT_DEFAUT
)

menu_unite_resultat = creer_menu_unites(
    fenetre,
    unite_resultat
)

menu_unite_resultat.pack(
    pady=PADDING_RESULT_MENU
)

bouton_inverser_unites = ttk.Button(
    fenetre,
    text=tr("button.swap_units"),
    command=inverser_unites,
    style="Custom.TButton"
)

bouton_inverser_unites.pack(
    pady=PADDING_SWAP
)




# BOUTON DE CALCUL ET RÉSULTAT

frame_boutons = tk.Frame(fenetre)
frame_boutons.pack(
    pady=(18, 15)
)

# Bouton calcul
bouton_calculer = ttk.Button(
    frame_boutons,
    text=tr("button.calculate"),
    command=lancer_calcul,
    style="Custom.TButton"
)
bouton_calculer.pack(side="left", padx=10)

# Bouton réinitialiser
bouton_reinitialiser = ttk.Button(
    frame_boutons,
    text=tr("button.reset"),
    command=reinitialiser_interface,
    style="Custom.TButton"
)
bouton_reinitialiser.pack(side="left", padx=10)

# Bouton copier
bouton_copier = ttk.Button(
    frame_boutons,
    text=tr("button.copy"),
    command=copier_resultat,
    style="Custom.TButton"
)
bouton_copier.pack(side="left", padx=10)

# Résultat
label_resultat = tk.Label(
    fenetre,
    text=texte_resultat_defaut(),
    font=("Arial", 14, "bold"),
    fg=obtenir_theme(theme_actuel)["text"]
)
label_resultat.pack(
    pady=(12, 10)
)

# Historique
titre_historique = tk.Label(
    fenetre,
    text=tr("section.history"),
    font=("Arial", 12, "bold"),
    fg=obtenir_theme(theme_actuel)["text"]
)
titre_historique.pack(
    pady=(8, 6)
)

frame_historique = tk.Frame(fenetre)
frame_historique.pack(pady=5)

theme = obtenir_theme(theme_actuel)

liste_historique = tk.Listbox(
    frame_historique,
    width=60,
    height=6,
    bg=theme["field"],
    fg=theme["text"],
    selectbackground=theme["selection"],
    selectforeground=theme["selection_text"]
)

scrollbar_historique = tk.Scrollbar(
    frame_historique,
    orient="vertical",
    command=liste_historique.yview,
    takefocus=False
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
    text=tr("button.clear_history"),
    command=effacer_historique,
    style="Custom.TButton"
)
bouton_effacer_historique.pack(pady=10)





# <ENTER> lance le calcul
fenetre.bind("<Return>", lancer_calcul)
fenetre.bind("<KP_Enter>", lancer_calcul)
# <ESC> pour focus
fenetre.bind(
    "<Escape>",
    lambda event: fenetre.focus_set()
)
# <CTRL/CMD + SHIFT + C> pour copier
fenetre.bind(
    "<Control-Shift-C>",
    lambda event: copier_resultat()
)

# <CTRL/CMD + R> pour reset
fenetre.bind(
    "<Control-r>",
    lambda event: reinitialiser_interface()
)

# <CTRL + SHIFT + S> pour swap
fenetre.bind(
    "<Control-Shift-S>",
    lambda event: inverser_unites()
)

# <CTRL/CMD + SHIFT + +> pour ajouter une valeur
fenetre.bind(
    "<Control-Shift-plus>",
    ajouter_valeur_raccourci
)

fenetre.bind(
    "<Control-KP_Add>",
    ajouter_valeur_raccourci
)

if sys.platform == "darwin":
    fenetre.bind(
        "<Command-Shift-C>",
        lambda event: copier_resultat()
    )

    fenetre.bind(
        "<Command-r>",
        lambda event: reinitialiser_interface()
    )

    fenetre.bind(
        "<Command-Shift-S>",
        lambda event: inverser_unites()
    )

    fenetre.bind(
        "<Command-Shift-plus>",
        ajouter_valeur_raccourci
    )

    fenetre.bind(
        "<Command-KP_Add>",
        ajouter_valeur_raccourci
    )
    
# Cliquer en dehors des zones de texte pour désélectionner
fenetre.bind("<Button-1>", retirer_focus_entree, add="+")

charger_preferences()

charger_historique()
mettre_a_jour_historique()

appliquer_theme()

fenetre.after_idle(definir_taille_initiale)

fenetre.mainloop()