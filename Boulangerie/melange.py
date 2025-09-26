# ce fichier sert à la gestion des melanges necessaires pour les commandes de la semaine prochaine
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk

class GestionMelange:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def afficher_fenetre(self, parent):
        fenetre = ttk.Toplevel(parent)
        fenetre.title("Mélanges de la Semaine")
        fenetre.geometry("800x600")
        
        # Création du Treeview
        columns = ('pain', 'melange', 'quantite')
        tree = ttk.Treeview(fenetre, columns=columns, show='headings')
        
        # Configuration des colonnes
        for col in columns:
            tree.heading(col, text=col.title())
        
        # Récupération des mélanges
        self.cursor.execute("""
            SELECT pain.DescPain, melange.DescMelange, livrer.QuantiteMelange
            FROM livrer 
            JOIN pain ON livrer.IDpain = pain.IDpain 
            JOIN melange ON pain.IDMelange = melange.IDMelange 
            WHERE livrer.DateLivraison BETWEEN 
                DATE_SUB(DATE_ADD(CURDATE(), INTERVAL 7 DAY), INTERVAL WEEKDAY(DATE_ADD(CURDATE(), INTERVAL 7 DAY)) DAY)
                AND 
                DATE_ADD(DATE_ADD(CURDATE(), INTERVAL 7 DAY), INTERVAL (6 - WEEKDAY(DATE_ADD(CURDATE(), INTERVAL 7 DAY))) DAY);
        """)
        
        melanges = self.cursor.fetchall()
        
        for melange in melanges:
            tree.insert('', 'end', values=(
                melange['DescPain'],
                melange['DescMelange'],
                melange['QuantiteMelange']
            ))
        

        tree.pack(expand=True, fill='both', padx=20, pady=20)
