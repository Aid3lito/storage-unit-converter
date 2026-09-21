import tkinter as tk
from tkinter import ttk


def creer_selecteur(
    parent,
    variable_affichage,
    options,
    callback,
):
    bouton = ttk.Menubutton(
        parent,
        textvariable=variable_affichage,
        width=22,
        style="Custom.TMenubutton",
    )

    menu = tk.Menu(
        bouton,
        tearoff=0,
    )

    bouton["menu"] = menu
    bouton.menu_options = menu

    for libelle, valeur in options.items():
        menu.add_command(
            label=libelle,
            command=lambda valeur=valeur: callback(valeur),
        )

    return bouton


def mettre_a_jour_selecteur(
    bouton,
    options,
    callback,
):
    menu = bouton.menu_options

    menu.delete(0, "end")

    for libelle, valeur in options.items():
        menu.add_command(
            label=libelle,
            command=lambda valeur=valeur: callback(valeur),
        )

def ouvrir_fenetre_parametres(
    parent,
    tr,
    langue_actuelle,
    changer_langue,
    theme_actuel,
    changer_theme,
    obtenir_langue_actuelle,
    obtenir_theme_actuel,
    changer_operation_demarrage,
    obtenir_operation_demarrage,
    changer_unite_entree_demarrage,
    obtenir_unite_entree_demarrage,
    unites_disponibles,
    fenetre_existante=None,
):
    if (
        fenetre_existante is not None
        and fenetre_existante.winfo_exists()
    ):
        fenetre_existante.lift()
        fenetre_existante.focus_force()
        return fenetre_existante

    fenetre_parametres = tk.Toplevel(parent)

    fenetre_parametres.title(
        tr("settings.title")
    )

    fenetre_parametres.resizable(
        False,
        False
    )

    fenetre_parametres.transient(parent)

    frame = ttk.Frame(
        fenetre_parametres,
        padding=20,
    )
    frame.pack(
        fill="both",
        expand=True
    )

    label_langue = ttk.Label(
        frame,
        text=tr("settings.language"),
    )

    label_langue.pack(
        pady=(10, 5)
    )

    langues_affichees = {
        tr("language.english"): "en",
        tr("language.french"): "fr",
    }

    langue_affichee_actuelle = next(
        label
        for label, code in langues_affichees.items()
        if code == langue_actuelle
    )

    variable_langue = tk.StringVar(
            value=langue_affichee_actuelle
        )

    def appliquer_selection_langue(langue):
        changer_langue(langue)

        rafraichir_textes()

    selecteur_langue = creer_selecteur(
        frame,
        variable_langue,
        langues_affichees,
        appliquer_selection_langue,
    )

    selecteur_langue.pack(
        pady=(0, 25)
    )

    label_theme = ttk.Label(
        frame,
        text=tr("settings.theme"),
    )

    label_theme.pack(
        pady=(0, 25)
    )

    themes_affiches = {
        tr("theme.light"): "light",
        tr("theme.dark"): "dark",
    }

    theme_affiche_actuel = next(
        label
        for label, code in themes_affiches.items()
        if code == theme_actuel
    )

    variable_theme = tk.StringVar(
        value=theme_affiche_actuel
    )

    def appliquer_selection_theme(theme):
        changer_theme(theme)

        variable_theme.set(
            next(
                label
                for label, code in themes_affiches.items()
                if code == theme
            )
        )

    selecteur_theme = creer_selecteur(
        frame,
        variable_theme,
        themes_affiches,
        appliquer_selection_theme,
    )

    selecteur_theme.pack(
        pady=(0, 20)
    )

    label_operation_demarrage = ttk.Label(
        frame,
        text=tr("settings.default_operation"),
    )

    label_operation_demarrage.pack(
        pady=(0, 5)
    )

    operations_affichees = {
        tr("operation.conversion"): "conversion",
        tr("operation.addition"): "addition",
        tr("operation.subtraction"): "subtraction",
    }

    operation_affichee_actuelle = next(
        label
        for label, code in operations_affichees.items()
        if code == obtenir_operation_demarrage()
    )

    variable_operation_demarrage = tk.StringVar(
        value=operation_affichee_actuelle
    )

    def appliquer_selection_operation_demarrage(operation):
        changer_operation_demarrage(operation)

        variable_operation_demarrage.set(
            next(
                label
                for label, code in operations_affichees.items()
                if code == operation
            )
        )

    selecteur_operation_demarrage = creer_selecteur(
        frame,
        variable_operation_demarrage,
        operations_affichees,
        appliquer_selection_operation_demarrage,
    )

    selecteur_operation_demarrage.pack(
        pady=(0, 25)
    )

    label_unite_entree_demarrage = ttk.Label(
        frame,
        text=tr("settings.default_input_unit"),
    )

    label_unite_entree_demarrage.pack(
        pady=(0, 5)
    )

    variable_unite_entree_demarrage = tk.StringVar(
        value=obtenir_unite_entree_demarrage()
    )

    options_unites = {
        unite: unite
        for unite in unites_disponibles
    }

    def appliquer_selection_unite_entree_demarrage(unite):
        changer_unite_entree_demarrage(unite)

        variable_unite_entree_demarrage.set(
            unite
        )

    selecteur_unite_entree_demarrage = creer_selecteur(
        frame,
        variable_unite_entree_demarrage,
        options_unites,
        appliquer_selection_unite_entree_demarrage,
    )

    selecteur_unite_entree_demarrage.pack(
        pady=(0, 25)
    )

    bouton_fermer = ttk.Button(
        frame,
        text=tr("button.close"),
        command=fenetre_parametres.destroy,
    )
    bouton_fermer.pack()

    def rafraichir_textes():
        fenetre_parametres.title(
            tr("settings.title")
        )

        label_langue.config(
            text=tr("settings.language")
        )

        label_theme.config(
            text=tr("settings.theme")
        )

        label_operation_demarrage.config(
            text=tr("settings.default_operation")
        )

        label_unite_entree_demarrage.config(
            text=tr("settings.default_input_unit")
        )

        bouton_fermer.config(
            text=tr("button.close")
        )

        nouvelles_langues_affichees = {
            tr("language.english"): "en",
            tr("language.french"): "fr",
        }

        langues_affichees.clear()
        langues_affichees.update(
            nouvelles_langues_affichees
        )

        mettre_a_jour_selecteur(
            selecteur_langue,
            langues_affichees,
            appliquer_selection_langue,
        )

        variable_langue.set(
            next(
                label
                for label, code in langues_affichees.items()
                if code == obtenir_langue_actuelle()
            )
        )   

        nouveaux_themes_affiches = {
            tr("theme.light"): "light",
            tr("theme.dark"): "dark",
        }

        themes_affiches.clear()
        themes_affiches.update(
            nouveaux_themes_affiches
        )

        mettre_a_jour_selecteur(
            selecteur_theme,
            themes_affiches,
            appliquer_selection_theme,
        )

        nouvelles_operations_affichees = {
            tr("operation.conversion"): "conversion",
            tr("operation.addition"): "addition",
            tr("operation.subtraction"): "subtraction",
        }

        operations_affichees.clear()
        operations_affichees.update(
            nouvelles_operations_affichees
        )

        mettre_a_jour_selecteur(
            selecteur_operation_demarrage,
            operations_affichees,
            appliquer_selection_operation_demarrage,
        )

        variable_operation_demarrage.set(
            next(
                label
                for label, code in operations_affichees.items()
                if code == obtenir_operation_demarrage()
            )
        )

        variable_theme.set(
            next(
                label
                for label, code in themes_affiches.items()
                if code == obtenir_theme_actuel()
            )
        )

    fenetre_parametres.grab_set()

    return fenetre_parametres