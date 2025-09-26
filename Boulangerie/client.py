
# ce fichier sert à l'enregistrement des clients dans la base de données
import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk

# Connexion à la base
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='boulangerie'
)

cursor = conn.cursor()

class GestionClient:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def afficher_fenetre(self, parent):
        fenetre = ttk.Toplevel(parent)
        fenetre.title("Nouveau Client")
        fenetre.geometry("500x400")
        
        form_frame = ttk.Frame(fenetre, padding="20")
        form_frame.pack(expand=True, fill='both')
        
        ttk.Label(form_frame, text="Enregistrement d'un nouveau client",
                 font=('Helvetica', 16, 'bold')).pack(pady=20)
        
        # Champs adaptés à la table CLIENTE : NomCli, AdrCli, VilleCli 
        champs = [
            ("Nom:", "nom"),
            ("Adresse:", "adresse"),
            ("Ville:", "Ville"),
        ]
        entries = {}
        
        for label_text, key in champs:
            frame = ttk.Frame(form_frame)
            frame.pack(fill='x', pady=10)
            
            ttk.Label(frame, text=label_text, width=15).pack(side='left')
            entry = ttk.Entry(frame, width=30)
            entry.pack(side='left', padx=10)
            entries[key] = entry
        
        ttk.Button(form_frame, text="Enregistrer",
                  command=lambda: self.sauvegarder_client(
                      entries['nom'].get(),
                      entries['adresse'].get(),
                      entries['Ville'].get(),
                      fenetre)).pack(pady=10)

    def sauvegarder_client(self, nom, adresse, Ville, fenetre):
        if not all([nom, adresse, Ville]):
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs!")
            return
        
        try:
            self.cursor.execute("""
                INSERT INTO CLIENTE (NomCli, AdrCli, VilleCli)
                VALUES (%s, %s, %s)
            """, (nom, adresse, Ville))
            self.conn.commit()
            messagebox.showinfo("Succès", "Client enregistré avec succès!")
            fenetre.destroy()
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'enregistrement: {e}")

# Fermer la connexion
cursor.close()
conn.close()

