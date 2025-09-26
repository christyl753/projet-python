
# Ce fichier sert à la gestion des factures des clients 
import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
from datetime import datetime, timedelta
from calendar import monthrange

# Connexion à la base
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='boulangerie'
)

cursor = conn.cursor()

class GestionFacture:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def afficher_fenetre(self, parent):
        fenetre = ttk.Toplevel(parent)
        fenetre.title("Gestion des Factures")
        fenetre.geometry("800x600")
        
        # Frame principal
        main_frame = ttk.Frame(fenetre, padding="20")
        main_frame.pack(expand=True, fill='both')
        
        # Sélection du client
        frame_selection = ttk.Frame(main_frame)
        frame_selection.pack(fill='x', pady=10)
        
        ttk.Label(frame_selection, text="Sélectionner un client:",
                 font=('Helvetica', 12)).pack(side='left', padx=5)
        
        # Récupération de la liste des clients
        self.cursor.execute("SELECT distinct cliente.idCLIENTE, NomCli FROM CLIENTE join livrer on CLIENTE.idCLIENTE = livrer.idCLIENTE;")
        self.clients = self.cursor.fetchall()
        
        self.client_var = tk.StringVar()
        client_cb = ttk.Combobox(frame_selection, 
                                textvariable=self.client_var,
                                values=[c['NomCli'] for c in self.clients],
                                width=30)
        client_cb.pack(side='left', padx=5)

        # Ajout sélection mois et année
        now = datetime.now()
        self.mois_var = tk.StringVar(value=str(now.month))
        self.annee_var = tk.StringVar(value=str(now.year))
        mois_noms = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
        mois_cb = ttk.Combobox(frame_selection, textvariable=self.mois_var, values=[str(i+1) for i in range(12)], width=5, state="readonly")
        mois_cb.pack(side='left', padx=5)
        annee_cb = ttk.Combobox(frame_selection, textvariable=self.annee_var, values=[str(y) for y in range(now.year-5, now.year+2)], width=7, state="readonly")
        annee_cb.pack(side='left', padx=5)
        ttk.Label(frame_selection, text="(Mois / Année)").pack(side='left', padx=2)
        
        ttk.Button(frame_selection, 
                  text="Afficher la facture",
                  command=self.afficher_facture,
                  bootstyle="primary").pack(side='left', padx=5)
        
        # Création du Treeview pour les détails de la facture
        columns = ('date', 'pain', 'quantite', 'prix_unitaire', 'total')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings')
        
        # Configuration des colonnes
        self.tree.heading('date', text='Date')
        self.tree.heading('pain', text='Pain')
        self.tree.heading('quantite', text='Quantité')
        self.tree.heading('prix_unitaire', text='Prix unitaire')
        self.tree.heading('total', text='Total')
        
        self.tree.column('date', width=100)
        self.tree.column('pain', width=200)
        self.tree.column('quantite', width=100)
        self.tree.column('prix_unitaire', width=100)
        self.tree.column('total', width=100)
        
        # Ajout d'une barre de défilement
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(expand=True, fill='both', pady=10)
        scrollbar.pack(side="right", fill="y")
        
        # Label pour le total
        self.total_label = ttk.Label(main_frame, 
                                   text="Total: 0.00 €",
                                   font=('Helvetica', 12, 'bold'))
        self.total_label.pack(pady=10)

    def afficher_facture(self):
        # Effacer les anciennes données
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            client_id = next(c['idCLIENTE'] for c in self.clients 
                           if c['NomCli'] == self.client_var.get())
            mois = int(self.mois_var.get())
            annee = int(self.annee_var.get())
            # Calcul des bornes du mois sélectionné
            date_debut = datetime(annee, mois, 1)
            date_fin = datetime(annee, mois, monthrange(annee, mois)[1])
            # Récupération des commandes du client pour le mois/année choisis
            self.cursor.execute("""
                SELECT l.DateLivraison, p.descPain, l.QuantiteMelange,
                       p.prixPainHT, (l.QuantiteMelange * p.prixPainHT) as total
                FROM livrer l
                JOIN pain p ON l.IDpain = p.IDpain
                WHERE l.idCLIENTE = %s
                AND l.DateLivraison BETWEEN %s AND %s
                ORDER BY l.DateLivraison DESC
            """, (client_id, date_debut.strftime('%Y-%m-%d'), date_fin.strftime('%Y-%m-%d')))
            
            commandes = self.cursor.fetchall()
            total_facture = 0
            
            for cmd in commandes:
                self.tree.insert('', 'end', values=(
                    cmd['DateLivraison'].strftime('%Y-%m-%d'),
                    cmd['descPain'],
                    cmd['QuantiteMelange'],
                    f"{cmd['prixPainHT']:.2f} fcfa",
                    f"{cmd['total']:.2f} fcfa"
                ))
                total_facture += cmd['total']
            
            self.total_label.config(text=f"Total: {total_facture:.2f} FCFA")
            
        except Exception as e:
            messagebox.showerror("Erreur", 
                               f"Erreur lors de la récupération des données: {e}")

# Fermer la connexion
cursor.close()
conn.close()

