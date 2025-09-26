"""
Ce projet a été réalisé par:
Bitomo Joëlle 
Nfon II Elaine
Ngoh yom Alan
"""
import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as ttk
from datetime import datetime, timedelta
#Ce fichier sert à l'Enregistrement des commandes dans la base de données

# Connexion à la base de donnée locale 
conn = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='root',
    database='boulangerie'
)

cursor = conn.cursor(dictionary=True)

class GestionCommande:
    def __init__(self, conn, cursor):
        self.conn = conn
        self.cursor = cursor

    def afficher_fenetre(self, parent):
        fenetre = ttk.Toplevel(parent)
        fenetre.title("Nouvelle Commande")
        fenetre.geometry("600x500")
        
        form_frame = ttk.Frame(fenetre, padding="20")
        form_frame.pack(expand=True, fill='both')
        
        # Sélection du client
        self.cursor.execute("SELECT idCLIENTE, NomCli FROM CLIENTE")
        clients = self.cursor.fetchall()
        
        ttk.Label(form_frame, text="Client:").pack(pady=5)
        client_var = tk.StringVar()
        client_cb = ttk.Combobox(form_frame, textvariable=client_var, state="readonly")
        client_cb['values'] = [c['NomCli'] for c in clients]
        client_cb.pack(pady=5)

        # Sélection du pain
        self.cursor.execute("SELECT IDpain, descPain, prixPainHT FROM pain")
        pains = self.cursor.fetchall()
        
        ttk.Label(form_frame, text="Pain:").pack(pady=5)
        pain_var = tk.StringVar()
        pain_cb = ttk.Combobox(form_frame, textvariable=pain_var, state="disabled")
        pain_cb['values'] = [f"{p['descPain']} - {p['prixPainHT']} fcfa" for p in pains]
        pain_cb.pack(pady=5)
        
        # Quantité
        ttk.Label(form_frame, text="Quantité:").pack(pady=5)
        quantite_var = tk.StringVar()
        quantite_entry = ttk.Entry(form_frame, textvariable=quantite_var, state="disabled")
        quantite_entry.pack(pady=5)
        
        # Date de livraison (modifiable)
        ttk.Label(form_frame, text="Date de livraison (YYYY-MM-DD):").pack(pady=5)
        date_var = tk.StringVar()
        date_var.set((datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d'))
        date_entry = ttk.Entry(form_frame, textvariable=date_var, state="disabled")
        date_entry.pack(pady=5)
        
        enregistrer_btn = ttk.Button(form_frame, text="Enregistrer la commande", state="disabled")
        enregistrer_btn.pack(pady=20)

        # Fonction pour activer les champs après choix du client
        def activer_champs(event=None):
            if client_var.get():
                pain_cb.config(state="readonly")
                quantite_entry.config(state="normal")
                date_entry.config(state="normal")
                enregistrer_btn.config(state="normal")
            else:
                pain_cb.config(state="disabled")
                quantite_entry.config(state="disabled")
                date_entry.config(state="disabled")
                enregistrer_btn.config(state="disabled")

        client_cb.bind("<<ComboboxSelected>>", activer_champs)

        # Commande d'enregistrement
        def enregistrer():
            try:
                client_id = next(c['idCLIENTE'] for c in clients if c['NomCli'] == client_var.get())
                pain_index = [f"{p['descPain']} - {p['prixPainHT']} fcfa" for p in pains].index(pain_var.get())
                pain_id = pains[pain_index]['IDpain']
                quantite = quantite_var.get()
                date = date_var.get()
                if not pain_var.get() or not quantite or not date:
                    messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")
                    return
                self.cursor.execute("""
                    INSERT INTO livrer (IDpain, idCLIENTE, DateLivraison, QuantiteMelange)
                    VALUES (%s, %s, %s, %s)
                """, (pain_id, client_id, date, quantite))
                self.conn.commit()
                messagebox.showinfo("Succès", "Commande enregistrée!")
                fenetre.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de l'enregistrement: {e}")

        enregistrer_btn.config(command=enregistrer)

# Fermer la connexion
cursor.close()
conn.close()
