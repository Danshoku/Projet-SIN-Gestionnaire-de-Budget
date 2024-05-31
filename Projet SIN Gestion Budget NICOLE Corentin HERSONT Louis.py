# Importation des differente bibliothèque à utiliser
from tkinter import *
import tkinter as tk
from tkinter import messagebox as ms
import tkinter.simpledialog as sd
import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Création des fenêtres tkinter
fenetre_principale = tk.Tk()

# Création des variables de couleur
fg = 'black'

# Personnalisation de la fenêtre principale
fenetre_principale.title("App Gestion de Budget") # Changer le nom de la fenetre
fenetre_principale.iconbitmap("Logo_App.ico") # Ajouter un logo
fenetre_principale.resizable(width=False, height=False) # Forcer la fenetre à rester à la même taille

# Dictionnaire pour stocker les données de chaque compte et variables utile
comptes = {}
nom_compte_courant = ""

# Fonction pour mettre à jour la liste des revenus affichée dans la box
def mettre_a_jour_liste_revenus():
    listbox_revenus.delete(0, tk.END) # Supprimer le contenue de la box
    # Ajouter la liste des revenus dans la box
    for index, revenu in enumerate(comptes[nom_compte_courant]['revenus']):
        listbox_revenus.insert(tk.END, f"{index}. {revenu['date']} - {revenu['montant']}€ - {revenu['commentaire']}")

# Fonction pour mettre à jour la liste des depenses affichée dans la box
def mettre_a_jour_liste_depenses():
    listbox_depenses.delete(0, tk.END) # Supprimer le contenue de la box
    # Ajouter la liste des depenses dans la box
    for index, depense in enumerate(comptes[nom_compte_courant]['depenses']):
        listbox_depenses.insert(tk.END, f"{index}. {depense['date']} - {depense['montant']}€ - {depense['commentaire']}")

# Fonction pour ajouter un revenu au compte courant
def ajouter_revenu():
    if nom_compte_courant:
        montant = float(entree_revenu.get())
        date = entree_date_revenu.get()
        commentaire = entree_commentaire_revenu.get()
        comptes[nom_compte_courant]['revenus'].append({'montant': montant, 'date': date, 'commentaire': commentaire})
        entree_revenu.delete(0, tk.END)
        entree_date_revenu.delete(0, tk.END)
        entree_commentaire_revenu.delete(0, tk.END)
        mettre_a_jour_solde()
        sauvegarder_donnees()
    else:
        nom_compte_courant_existe_pas()
        entree_revenu.delete(0, tk.END)

# Fonction pour modifier un revenu au compte courant
def modifier_revenu():
    if nom_compte_courant:
        index = int(sd.askstring("Modifier Revenu", "Entrez l'index du revenu à modifier:"))
        if 0 <= index < len(comptes[nom_compte_courant]['revenus']):
            nouveau_montant = float(sd.askstring("Modifier Revenu", "Entrez le nouveau montant:"))
            nouvelle_date = sd.askstring("Modifier Revenu", "Entrez la nouvelle date:")
            nouveau_commentaire = sd.askstring("Modifier Revenu", "Entrez le nouveau commentaire:")
            comptes[nom_compte_courant]['revenus'][index] = {'montant': nouveau_montant, 'date': nouvelle_date, 'commentaire': nouveau_commentaire}
            mettre_a_jour_solde()
            sauvegarder_donnees()
        else:
            ms.showerror("Erreur", "Index invalide")
    else:
        nom_compte_courant_existe_pas()

# Fonction pour supprimer un revenu au compte courant
def supprimer_revenu():
    if nom_compte_courant:
        index = int(sd.askstring("Supprimer Revenu", "Entrez l'index du revenu à supprimer:"))
        if 0 <= index < len(comptes[nom_compte_courant]['revenus']):
            comptes[nom_compte_courant]['revenus'].pop(index)
            mettre_a_jour_solde()
            sauvegarder_donnees()
        else:
            ms.showerror("Erreur", "Index invalide")
    else:
        nom_compte_courant_existe_pas()

# Fonction pour ajouter une dépense au compte courant
def ajouter_depense():
    if nom_compte_courant:
        montant = float(entree_depense.get())
        date = entree_date_depense.get()
        commentaire = entree_commentaire_depense.get()
        comptes[nom_compte_courant]['depenses'].append({'montant': montant, 'date': date, 'commentaire': commentaire})
        entree_depense.delete(0, tk.END)
        entree_date_depense.delete(0, tk.END)
        entree_commentaire_depense.delete(0, tk.END)
        mettre_a_jour_solde()
        sauvegarder_donnees()
    else:
        nom_compte_courant_existe_pas()
        entree_depense.delete(0, tk.END)

# Fonction pour modifier une dépense au compte courant
def modifier_depense():
    if nom_compte_courant:
        index = int(sd.askstring("Modifier Dépense", "Entrez l'index de la dépense à modifier:"))
        if 0 <= index < len(comptes[nom_compte_courant]['depenses']):
            nouveau_montant = float(sd.askstring("Modifier Dépense", "Entrez le nouveau montant:"))
            nouvelle_date = sd.askstring("Modifier Dépense", "Entrez la nouvelle date:")
            nouveau_commentaire = sd.askstring("Modifier Dépense", "Entrez le nouveau commentaire:")
            comptes[nom_compte_courant]['depenses'][index] = {'montant': nouveau_montant, 'date': nouvelle_date, 'commentaire': nouveau_commentaire}
            mettre_a_jour_solde()
            sauvegarder_donnees()
        else:
            ms.showerror("Erreur", "Index invalide")
    else:
        nom_compte_courant_existe_pas()

# Fonction pour supprimer une dépense au compte courant
def supprimer_depense():
    if nom_compte_courant:
        index = int(sd.askstring("Supprimer Dépense", "Entrez l'index de la dépense à supprimer:"))
        if 0 <= index < len(comptes[nom_compte_courant]['depenses']):
            comptes[nom_compte_courant]['depenses'].pop(index)
            mettre_a_jour_solde()
            sauvegarder_donnees()
        else:
            ms.showerror("Erreur", "Index invalide")
    else:
        nom_compte_courant_existe_pas()

# Fonction de l'ajout de notre solde initial
def ajouter_solde_initial():
    if nom_compte_courant:
        comptes[nom_compte_courant]['solde_initial'] = float(entree_solde_initial.get())
        entree_solde_initial.delete(0, tk.END)
        mettre_a_jour_solde()
        sauvegarder_donnees()
    else:
        nom_compte_courant_existe_pas()
        entree_solde_initial.delete(0, tk.END)

# Modification des different solde et de leurs etiquettes associées
def mettre_a_jour_solde():
    if not nom_compte_courant:
        return
    compte = comptes[nom_compte_courant]
    solde_initial = compte.get('solde_initial', 0)
    total_revenus = sum(item['montant'] for item in compte['revenus'])
    total_depenses = sum(item['montant'] for item in compte['depenses'])
    solde = solde_initial + total_revenus - total_depenses

    etiquette_compte_solde_initial.config(text=f"{solde_initial} €")
    etiquette_compte_revenus.config(text=f"{total_revenus} €")
    etiquette_compte_depenses.config(text=f"{total_depenses} €")
    etiquette_solde.config(text=f"{solde} €")
    mettre_a_jour_liste_revenus()
    mettre_a_jour_liste_depenses()

    date_actuelle = datetime.now()
    mois_actuel, année_actuelle = date_actuelle.month, date_actuelle.year

    si_mois_actuel = lambda date: datetime.strptime(date, '%d/%m/%Y').month == mois_actuel and datetime.strptime(date, '%d/%m/%Y').year == année_actuelle
    si_année_actuelle = lambda date: datetime.strptime(date, '%d/%m/%Y').year == année_actuelle

    total_revenus_mensuels = sum(item['montant'] for item in compte['revenus'] if si_mois_actuel(item['date']))
    total_depenses_mensuelles = sum(item['montant'] for item in compte['depenses'] if si_mois_actuel(item['date']))
    solde_mensuel = total_revenus_mensuels - total_depenses_mensuelles
    etiquette_solde_mensuel.config(text=f"{solde_mensuel} €")

    total_revenus_annuels = sum(item['montant'] for item in compte['revenus'] if si_année_actuelle(item['date']))
    total_depenses_annuelles = sum(item['montant'] for item in compte['depenses'] if si_année_actuelle(item['date']))
    solde_annuel = total_revenus_annuels - total_depenses_annuelles
    etiquette_solde_annuel.config(text=f"{solde_annuel} €")

# Ajout du compte courant
def ajouter_nom_compte_courant():
    global nom_compte_courant
    nom_compte_courant = entree_nom_compte_courant.get()
    entree_nom_compte_courant.delete(0, tk.END)
    etiquette_compte_de.config(text=f"{nom_compte_courant}")
    if nom_compte_courant not in comptes:
        comptes[nom_compte_courant] = {'solde_initial': 0, 'revenus': [], 'depenses': []}
        sauvegarder_donnees()
    charger_donnees()

# Erreur du compte courant non selectionner
def nom_compte_courant_existe_pas():
    ms.showinfo("Erreur de chargement", "Aucun compte courant n'est sélectionné")

# Ajouter du texte dans les entry
def ajout_texte_entry(entry, texte):
    entry.insert(0, texte)
    entry.bind("<FocusIn>", lambda event: supprimer_texte_entry(entry, texte))
    entry.bind("<FocusOut>", lambda event: remplacer_texte_entry(entry, texte))

# Supprimer le texte dans les entry
def supprimer_texte_entry(entry, texte):
    if entry.get() == texte:
        entry.delete(0, tk.END)
        entry.config(fg='black')

# Remplacer le texte dans les entry
def remplacer_texte_entry(entry, texte):
    if entry.get() == "":
        entry.insert(0, texte)
        entry.config(fg='grey')

# Sauvegarder le dictionnaire du compte
def sauvegarder_donnees():
    try:
        with open("comptes.json", "w") as fichier:
            json.dump(comptes, fichier)
    except Exception as erreur:
        ms.showerror("Erreur", f"Erreur lors de la sauvegarde des données : {str(erreur)}")

# Charger le dictionnaire du compte
def charger_donnees():
    global comptes
    try:
        with open("comptes.json", "r") as fichier:
            comptes = json.load(fichier)
        mettre_a_jour_solde()
    except Exception as erreur:
        ms.showerror("Erreur", f"Erreur lors du chargement des données : {str(erreur)}")

# Afficher les graphique depenses et revenus
def afficher_graphiques():
    if not nom_compte_courant:
        ms.showinfo("Erreur", "Aucun compte courant n'est sélectionné")
        return

    compte = comptes[nom_compte_courant]
    maintenant = datetime.now()
    mois_actuel, annee_actuel = maintenant.month, maintenant.year

    # Convertir les dates en objets datetime
    revenus_dates = [(datetime.strptime(item['date'], '%d/%m/%Y'), item['montant']) for item in compte['revenus']]
    depenses_dates = [(datetime.strptime(item['date'], '%d/%m/%Y'), item['montant']) for item in compte['depenses']]

    # Filtrer les données du mois et de l'année courants
    revenus_mensuels = [montant for date, montant in revenus_dates if date.month == mois_actuel and date.year == annee_actuel]
    depenses_mensuelles = [montant for date, montant in depenses_dates if date.month == mois_actuel and date.year == annee_actuel]
    dates_mensuelles = [date for date, montant in revenus_dates + depenses_dates if date.month == mois_actuel and date.year == annee_actuel]

    revenus_annuels = [montant for date, montant in revenus_dates if date.year == annee_actuel]
    depenses_annuelles = [montant for date, montant in depenses_dates if date.year == annee_actuel]
    dates_annuelles = [date for date, montant in revenus_dates + depenses_dates if date.year == annee_actuel]

    # Trier les dates
    dates_mensuelles = sorted(list(set(dates_mensuelles)))
    dates_annuelles = sorted(list(set(dates_annuelles)))

    # Cumuler les montants pour chaque date
    revenus_mensuels_cumules = [sum(montant for date, montant in revenus_dates if date <= d and date.month == mois_actuel and date.year == annee_actuel) for d in dates_mensuelles]
    depenses_mensuelles_cumules = [sum(montant for date, montant in depenses_dates if date <= d and date.month == mois_actuel and date.year == annee_actuel) for d in dates_mensuelles]

    revenus_annuels_cumules = [sum(montant for date, montant in revenus_dates if date <= d and date.year == annee_actuel) for d in dates_annuelles]
    depenses_annuelles_cumules = [sum(montant for date, montant in depenses_dates if date <= d and date.year == annee_actuel) for d in dates_annuelles]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))

    # Graphique mensuel
    ax1.plot(dates_mensuelles, revenus_mensuels_cumules, label='Revenus', color='green')
    ax1.plot(dates_mensuelles, depenses_mensuelles_cumules, label='Dépenses', color='red')
    ax1.set_title('Revenus et Dépenses du Mois')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Montant (€)')
    ax1.legend()
    ax1.grid(True)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))

    # Graphique annuel
    ax2.plot(dates_annuelles, revenus_annuels_cumules, label='Revenus', color='green')
    ax2.plot(dates_annuelles, depenses_annuelles_cumules, label='Dépenses', color='red')
    ax2.set_title('Revenus et Dépenses de l\'Année')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Montant (€)')
    ax2.legend()
    ax2.grid(True)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))

    fig.autofmt_xdate()  # Mettre les dates sur l'axe x

    plt.show()

# Chargement initial des données
charger_donnees()

# Création des widgets pour la fenêtre principale
nom_fichier = PhotoImage(file='Fond_ecran_principal.png')
ajout_image_de_fond = tk.Label(fenetre_principale, image=nom_fichier)
ajout_image_de_fond.pack()

etiquette_compte_de = tk.Label(fenetre_principale, text="Aucun")
etiquette_compte_de.place(x=210, y=148)

entree_nom_compte_courant = tk.Entry(fenetre_principale)
entree_nom_compte_courant.place(x=65, y=185)
ajout_texte_entry(entree_nom_compte_courant, "Nom du compte")

bouton_ajouter_nom_compte_courant = tk.Button(fenetre_principale, text="Ajouter le nom du compte", command=ajouter_nom_compte_courant)
bouton_ajouter_nom_compte_courant.place(x=200, y=182)

etiquette_compte_solde_initial = tk.Label(fenetre_principale, text="Aucun")
etiquette_compte_solde_initial.place(x=245, y=255)

entree_solde_initial = tk.Entry(fenetre_principale)
entree_solde_initial.place(x=65, y=292)
ajout_texte_entry(entree_solde_initial, "Solde initial")

bouton_ajouter_solde_initial = tk.Button(fenetre_principale, text="Ajouter un solde initial", command=ajouter_solde_initial)
bouton_ajouter_solde_initial.place(x=200, y=289)

etiquette_compte_revenus = tk.Label(fenetre_principale, text="Aucun")
etiquette_compte_revenus.place(x=560, y=145)

entree_revenu = tk.Entry(fenetre_principale)
entree_revenu.place(x=410, y=190)
ajout_texte_entry(entree_revenu, "Montant du revenu")

entree_date_revenu = tk.Entry(fenetre_principale)
entree_date_revenu.place(x=410, y=230)
ajout_texte_entry(entree_date_revenu, "Date du revenu")

entree_commentaire_revenu = tk.Entry(fenetre_principale)
entree_commentaire_revenu.place(x=410, y=270)
ajout_texte_entry(entree_commentaire_revenu, "Commentaire")

bouton_ajouter_revenu = tk.Button(fenetre_principale, text="Ajouter un revenu", command=ajouter_revenu)
bouton_ajouter_revenu.place(x=550, y=187)

bouton_modifier_revenu = tk.Button(fenetre_principale, text="Modifier un revenu", command=modifier_revenu)
bouton_modifier_revenu.place(x=550, y=227)

bouton_supprimer_revenu = tk.Button(fenetre_principale, text="Supprimer un revenu", command=supprimer_revenu)
bouton_supprimer_revenu.place(x=550, y=267)

etiquette_compte_depenses = tk.Label(fenetre_principale, text="Aucun")
etiquette_compte_depenses.place(x=930, y=145)

entree_depense = tk.Entry(fenetre_principale)
entree_depense.place(x=755, y=190)
ajout_texte_entry(entree_depense, "Montant de dépense")

entree_date_depense = tk.Entry(fenetre_principale)
entree_date_depense.place(x=755, y=230)
ajout_texte_entry(entree_date_depense, "Date de la dépense")

entree_commentaire_depense = tk.Entry(fenetre_principale)
entree_commentaire_depense.place(x=755, y=270)
ajout_texte_entry(entree_commentaire_depense, "Commentaire")

bouton_ajouter_depense = tk.Button(fenetre_principale, text="Ajouter une dépense", command=ajouter_depense)
bouton_ajouter_depense.place(x=894, y=187)

bouton_modifier_depense = tk.Button(fenetre_principale, text="Modifier une dépense", command=modifier_depense)
bouton_modifier_depense.place(x=894, y=227)

bouton_supprimer_depense = tk.Button(fenetre_principale, text="Supprimer une dépense", command=supprimer_depense)
bouton_supprimer_depense.place(x=894, y=267)

etiquette_solde = tk.Label(fenetre_principale, text="Aucun")
etiquette_solde.place(x=185, y=379)

etiquette_solde_mensuel = tk.Label(fenetre_principale, text="Aucun")
etiquette_solde_mensuel.place(x=265, y=488)

etiquette_solde_annuel = tk.Label(fenetre_principale, text="Aucun")
etiquette_solde_annuel.place(x=253, y=597)

listbox_revenus = Listbox(fenetre_principale, width=50, height=19)
listbox_revenus.place(x=397, y=345)

listbox_depenses = Listbox(fenetre_principale, width=50, height=19)
listbox_depenses.place(x=744, y=345)

bouton_afficher_graphiques = tk.Button(fenetre_principale, text="Afficher les Graphiques", command=afficher_graphiques)
bouton_afficher_graphiques.place(x=950, y=40)

# Lancement de la fenêtre principale
fenetre_principale.mainloop()