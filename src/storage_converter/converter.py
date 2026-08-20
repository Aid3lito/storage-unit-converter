import json
from pathlib import Path


# LIBRARIES
DOSSIER_MODULE = Path(__file__).resolve().parent

fichier_decimal = open(
    DOSSIER_MODULE / "units_decimal.json",
    encoding="utf-8"
)
units_decimal = json.load(fichier_decimal)

fichier_binary = open(
    DOSSIER_MODULE / "units_binary.json",
    encoding="utf-8"
)
units_binary = json.load(fichier_binary)

toutes_les_units = units_decimal | units_binary

# NORMALISATION DU TEXTE
def normaliser_texte(texte):
    texte = texte.strip().lower()
    texte = texte.replace(" ", "")
    texte = texte.replace("-", "")
    return texte


# TROUVER L'UNITÉ
def trouver_unite(saisie):
    saisie = normaliser_texte(saisie)
    for nom, donnees in toutes_les_units.items():
        if normaliser_texte(donnees["acronyme"]) == saisie or normaliser_texte(nom) == saisie or normaliser_texte((nom + "s")) == saisie :
            return nom

    return "Impossible !"


#FONCTION D'AFFICHAGE DES UNITÉS
def afficher_unités():
    print("\n=== AVAILABLE UNITS ===\n")
    print(f'{"Unités décimales":<30}{"Unités binaires"}')
    for (nom_decimal, donnees_decimal), (nom_binary, donnees_binary) in zip(
        units_decimal.items(),
        units_binary.items()
        ):
            colonne_decimal = f'{donnees_decimal["acronyme"]:<4} - {nom_decimal}'
            colonne_binary = f'{donnees_binary["acronyme"]:<4} - {nom_binary}'
            print(f"{colonne_decimal:<30}{colonne_binary}")


# FONCTION DE VALIDATION D'UNITÉ
def demander_unite(message):
    while True:
        saisie = input(message)
        if saisie == "?":
            afficher_unités()
            continue

        unite = trouver_unite(saisie)
        if unite != "Impossible !":
            return unite
        else :
            print("\nUnknown unit! Please try again.\n")


#FONCTION DE VALIDATION NUMÉRIQUE
def demander_valeur(message):
    while True:
        try :
            saisie = float(input(message).strip().replace(",", "."))
            if saisie < 0:
                print("Negative values are not allowed!")
            else :
                return saisie
        except ValueError :
            print("\nInvalid value! Please enter a number.\n")


# FONCTION DE CONVERSION
def convertir(valeur, unite_depart, unite_arrivee):
    valeur_byte = valeur * toutes_les_units[unite_depart]["valeur"]
    resultat = valeur_byte / toutes_les_units[unite_arrivee]["valeur"]
    return resultat


# FONCTION DE CALCUL
def calculer(valeur_1, unite_1, valeur_2, unite_2, unite_resultat, operation):
    valeur_1_convertie = convertir(valeur_1, unite_1, unite_resultat)
    valeur_2_convertie = convertir(valeur_2, unite_2, unite_resultat)

    if operation == "+":
        resultat = valeur_1_convertie + valeur_2_convertie
        return resultat
    elif operation == "-":
        resultat = valeur_1_convertie - valeur_2_convertie
        if resultat < 0:
            return None
        
        return resultat


# FONCTION D'AFFICHAGE
def afficher_resultat(resultat, unite):
    if resultat is None :
        print("\nOperation impossible: the result cannot be negative.")
    else :
        resultat_arrondi = round(resultat, 2)
        acronyme = toutes_les_units[unite]["acronyme"]
        print(resultat_arrondi, acronyme)


# INPUT
def demander_choix():
    while True:
        choix = input(
            "\nWhat would you like to do?\n\n"
            "1. Conversion\n"
            "2. Addition\n"
            "3. Subtraction\n\n"
            "Your choice (enter a number): "
        )

        if choix in ["1", "2", "3"]:
            return choix

        print("Invalid choice! Please enter 1, 2, or 3.\n")

# CHOIX 1 : CONVERSION
def effectuer_conversion():
    valeur = demander_valeur("Value to convert (number only): ")
    unite_depart = demander_unite("Source unit (type ? to list units): ")
    unite_arrivee = demander_unite("Target unit (type ? to list units): ")
    resultat = convertir(valeur, unite_depart, unite_arrivee)
    afficher_resultat(resultat, unite_arrivee)


# CHOIX 2 ET 3 : CALCULER
def effectuer_calcul(operation):
    valeur_1 = demander_valeur("First value (number only): ")
    unite_1 = demander_unite("Unit of the first value (type ? to list units): ")
    valeur_2 = demander_valeur("Second value (number only): ")
    unite_2 = demander_unite("Unit of the second value (type ? to list units): ")
    unite_resultat = demander_unite("Result unit (type ? to list units): ")
    resultat = calculer(valeur_1, unite_1, valeur_2, unite_2, unite_resultat, operation)
    afficher_resultat(resultat, unite_resultat)


# MAIN
if __name__ == "__main__":
    while True :
        choix = demander_choix()

        if choix == "1" :
            effectuer_conversion()

        elif choix == "2" :
            effectuer_calcul("+")

        elif choix == "3" :
            effectuer_calcul("-")

        else :
            print("Invalid choice!")

        while True:
            continuer = input("\nWould you like to perform another operation? (Y/N): ").lower()

            if continuer in ["y", "n"]:
                break

            print("Invalid choice! Please enter Y or N.")
        
        if continuer == "n" :
            break