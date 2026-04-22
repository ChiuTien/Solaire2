import tkinter as tk
from tkinter import ttk

from Views.AppareilViews import AppareilView
from Views.BatterieViews import BatterieView
from Views.ConsommationAnalyseView import ConsommationAnalyseView
from Views.ConsommationAppareil import ConsommationAppareilView
from Views.PanneauxViews import PanneauView


class MenuPrincipal:
	def __init__(self, master):
		self.master = master
		self.master.title("Gestion Solaire - Menu")
		self.master.geometry("460x280")

		frame = ttk.LabelFrame(master, text="Choisir une interface")
		frame.pack(fill="both", expand=True, padx=14, pady=14)

		ttk.Button(frame, text="CRUD Appareil", command=self.open_appareil).pack(fill="x", padx=12, pady=8)
		ttk.Button(frame, text="CRUD Batterie", command=self.open_batterie).pack(fill="x", padx=12, pady=8)
		ttk.Button(frame, text="CRUD Panneau", command=self.open_panneau).pack(fill="x", padx=12, pady=8)
		ttk.Button(frame, text="CRUD Consommation", command=self.open_consommation).pack(fill="x", padx=12, pady=8)
		ttk.Button(frame, text="Analyse Consommation", command=self.open_analyse).pack(fill="x", padx=12, pady=8)

	def _open_window(self, title):
		window = tk.Toplevel(self.master)
		window.title(title)
		return window

	def open_appareil(self):
		AppareilView(self._open_window("CRUD Appareil"))

	def open_batterie(self):
		BatterieView(self._open_window("CRUD Batterie"))

	def open_panneau(self):
		PanneauView(self._open_window("CRUD Panneau"))

	def open_consommation(self):
		ConsommationAppareilView(self._open_window("CRUD Consommation"))

	def open_analyse(self):
		ConsommationAnalyseView(self._open_window("Analyse Consommation"))


def run_interface():
	root = tk.Tk()
	MenuPrincipal(root)
	root.mainloop()


if __name__ == "__main__":
	run_interface()
