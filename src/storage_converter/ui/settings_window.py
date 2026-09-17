import tkinter as tk
from tkinter import ttk


def ouvrir_fenetre_parametres(
    parent,
    tr,
    langue_actuelle,
    changer_langue,
    theme_actuel,
    changer_theme,
    obtenir_langue_actuelle,
    obtenir_theme_actuel,
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

    titre = ttk.Label(
        frame,
        text=tr("settings.title"),
        font=("Arial", 14, "bold"),
    )
    titre.pack(
        pady=(0, 15)
    )

    label_langue = ttk.Label(
        frame,
        text=tr("settings.language"),
    )

    label_langue.pack(
        pady=(0, 5)
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

    selecteur_langue = ttk.Combobox(
        frame,
        textvariable=variable_langue,
        state="readonly",
        values=tuple(langues_affichees.keys()),
        width=18,
    )
    selecteur_langue.pack(
        pady=(0, 15)
    )

    def appliquer_selection_langue(event=None):
        langue = langues_affichees[
            variable_langue.get()
        ]

        changer_langue(langue)

        rafraichir_textes()

    selecteur_langue.bind(
        "<<ComboboxSelected>>",
        appliquer_selection_langue
    )

    label_theme = ttk.Label(
        frame,
        text=tr("settings.theme"),
    )

    label_theme.pack(
        pady=(0, 5)
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

    selecteur_theme = ttk.Combobox(
        frame,
        textvariable=variable_theme,
        state="readonly",
        values=tuple(themes_affiches.keys()),
        width=18,
    )

    selecteur_theme.pack(
        pady=(0, 15)
    )

    def appliquer_selection_theme(event=None):
        changer_theme(
            themes_affiches[variable_theme.get()]
        )

    selecteur_theme.bind(
        "<<ComboboxSelected>>",
        appliquer_selection_theme
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

        titre.config(
            text=tr("settings.title")
        )

        label_langue.config(
            text=tr("settings.language")
        )

        label_theme.config(
            text=tr("settings.theme")
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

        selecteur_langue["values"] = tuple(
            langues_affichees.keys()
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

        selecteur_theme["values"] = tuple(
            themes_affiches.keys()
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