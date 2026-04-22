import tkinter as tk
from tkinter import ttk

from Views.AppareilViews import AppareilView
from Views.BatterieViews import BatterieView
from Views.ConsommationAnalyseView import ConsommationAnalyseView
from Views.ConsommationAppareil import ConsommationAppareilView
from Views.PanneauxViews import PanneauView
from Views.PrixViews import PrixView
from theme import apply_dark_theme


class MenuPrincipal:
	def __init__(self, master):
		self.master = master
		self.master.title("Gestion Solaire - Menu Principal")
		self.master.geometry("550x600")
		self.master.resizable(False, False)

		# Header avec titre
		header = ttk.Frame(master, style='Header.TFrame')
		header.pack(fill="x", padx=0, pady=0)

		title_label = ttk.Label(header, text="☀ GESTION SOLAIRE", style='Title.TLabel')
		title_label.pack(pady=20, padx=20)

		subtitle = ttk.Label(header, text="Système de Gestion d'Énergie Solaire", style='Subtitle.TLabel')
		subtitle.pack(pady=(0, 20), padx=20)

		# Séparateur
		separator1 = ttk.Frame(master, height=2)
		separator1.pack(fill="x", padx=0, pady=0)

		# Section: Gestion des données
		section1 = ttk.LabelFrame(master, text="⚙ GESTION DES DONNÉES")
		section1.pack(fill="x", padx=20, pady=15)

		ttk.Button(section1, text="📱 Appareils", command=self.open_appareil).pack(fill="x", padx=10, pady=8)
		ttk.Button(section1, text="🔋 Batteries", command=self.open_batterie).pack(fill="x", padx=10, pady=8)
		ttk.Button(section1, text="☀️ Panneaux Solaires", command=self.open_panneau).pack(fill="x", padx=10, pady=8)
		ttk.Button(section1, text="💵 Prix", command=self.open_prix).pack(fill="x", padx=10, pady=8)

		# Section: Consommation
		section2 = ttk.LabelFrame(master, text="📊 CONSOMMATION")
		section2.pack(fill="x", padx=20, pady=15)

		ttk.Button(section2, text="📈 Consommation Appareil", command=self.open_consommation).pack(fill="x", padx=10, pady=8)
		ttk.Button(section2, text="📉 Analyse Consommation", command=self.open_analyse).pack(fill="x", padx=10, pady=8)

		# Pied de page
		footer_frame = ttk.Frame(master)
		footer_frame.pack(fill="x", padx=20, pady=15)
		footer_label = ttk.Label(footer_frame, text="v1.0 - Projet Tahina", style='Subtitle.TLabel')
		footer_label.pack()

	def _open_window(self, title):
		window = tk.Toplevel(self.master)
		window.title(title)
		# Appliquer le thème à la nouvelle fenêtre
		apply_dark_theme(window)
		return window

	def open_appareil(self):
		AppareilView(self._open_window("CRUD Appareil"))

	def open_batterie(self):
		BatterieView(self._open_window("CRUD Batterie"))

	def open_panneau(self):
		PanneauView(self._open_window("CRUD Panneau"))

	def open_prix(self):
		PrixView(self._open_window("CRUD Prix"))

	def open_consommation(self):
		ConsommationAppareilView(self._open_window("CRUD Consommation"))

	def open_analyse(self):
		ConsommationAnalyseView(self._open_window("Analyse Consommation"))


def run_interface():
	root = tk.Tk()
	apply_dark_theme(root)
	MenuPrincipal(root)
	root.mainloop()


if __name__ == "__main__":
	run_interface()
