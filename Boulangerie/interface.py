
""" Ce fichier sert à la gestion de l'interface principale de l'application
 et fait appel aux autres fichiers ou modules pour fonctionner correctement."""
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
from client import GestionClient
from commande import GestionCommande
from melange import GestionMelange
from facture import GestionFacture
import mysql.connector

class ApplicationGestion:
    def __init__(self):
        self.fenetre = ttk.Window(themename="cosmo")
        self.fenetre.title("Système de Gestion des Commandes")
        self.fenetre.geometry("1000x700")
        
        self.connecter_bd()
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        
        self.client_manager = GestionClient(self.conn, self.cursor)
        self.commande_manager = GestionCommande(self.conn, self.cursor)
        self.melange_manager = GestionMelange(self.conn, self.cursor)
        self.facture_manager = GestionFacture(self.conn, self.cursor)
        
        self.creer_menu()

    def connecter_bd(self):
        try:
            self.conn = mysql.connector.connect(
                host='127.0.0.1',
                port=3306,
                user='root',
                password='root',
                database='boulangerie'
            )
            self.cursor = self.conn.cursor(dictionary=True)
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur de connexion", f"Impossible de se connecter à la base de données: {err}")

    def creer_menu(self):
        titre_frame = ttk.Frame(self.fenetre)
        titre_frame.pack(fill='x', pady=20)
        
        titre = ttk.Label(titre_frame, 
                         text="BOULANGERIE - SYSTÈME DE GESTION", 
                         font=('Helvetica', 24, 'bold'),
                         bootstyle="primary")
        titre.pack()
        
        boutons = [
            ("Nouveau Client", self.client_manager.afficher_fenetre, "👤", "success"),
            ("Nouvelle Commande", self.commande_manager.afficher_fenetre, "📝", "info"),
            ("Mélanges Semaine", self.melange_manager.afficher_fenetre, "🔄", "warning"),
            ("Éditer Factures", self.facture_manager.afficher_fenetre, "📊", "danger")
        ]
        
        main_frame = ttk.Frame(self.fenetre)
        main_frame.pack(expand=True, fill='both', padx=50, pady=20)
        main_frame.columnconfigure((0, 1), weight=1)
        
        for idx, (texte, commande, icone, style) in enumerate(boutons):
            frame_bouton = ttk.Frame(main_frame)
            frame_bouton.grid(row=idx//2, column=idx%2, padx=20, pady=20, sticky='nsew')
            btn = ttk.Button(frame_bouton, 
                           text=f"{icone} {texte}",
                           command=lambda cmd=commande: cmd(self.fenetre),
                           bootstyle=style,
                           width=25)
            btn.pack(pady=10)

    def executer(self):
        self.fenetre.mainloop()

if __name__ == "__main__":
    app = ApplicationGestion()

    app.executer()
