THEME_LIGHT = {
    "background": "#F0F0F0",
    "field": "#FFFFFF",
    "text": "#000000",
    "placeholder": "#808080",
    "selection": "#0078D7",
    "selection_text": "#FFFFFF",
    "button_background": "#E8E8E8",
    "button_active": "#D8D8D8",
    "button_text": "#000000",
}

THEME_DARK = {
    "background": "#1E1E1E",
    "field": "#2B2B2B",
    "text": "#E8E8E8",
    "placeholder": "#A0A0A0",
    "selection": "#3A7AFE",
    "selection_text": "#FFFFFF",
    "button_background": "#3A3A3A",
    "button_active": "#4A4A4A",
    "button_text": "#F2F2F2",
}

THEMES = {
    "light": THEME_LIGHT,
    "dark": THEME_DARK,
}

THEME_DEFAUT = "light"

def obtenir_theme(nom_theme):
    return THEMES[nom_theme]