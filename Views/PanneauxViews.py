import tkinter as tk
from tkinter import ttk, messagebox

from Models.Panneau import Panneau
from Repositories.PanneauRepository import PanneauRepository


class PanneauView:
	def __init__(self, master):
		self.master = master
		self.master.title("CRUD Panneau")
		self.master.geometry("1180x600")

		self.repo = PanneauRepository()
		self.selected_id = None

		self._build_ui()
		self._load_data()

	def _build_ui(self):
		form = ttk.LabelFrame(self.master, text="Panneau")
		form.pack(fill="x", padx=12, pady=10)

		ttk.Label(form, text="Nom:").grid(row=0, column=0, padx=8, pady=8, sticky="w")
		self.nom_entry = ttk.Entry(form, width=18)
		self.nom_entry.grid(row=0, column=1, padx=8, pady=8, sticky="w")

		ttk.Label(form, text="Rendement:").grid(row=0, column=2, padx=8, pady=8, sticky="w")
		self.rendement_entry = ttk.Entry(form, width=14)
		self.rendement_entry.grid(row=0, column=3, padx=8, pady=8, sticky="w")

		ttk.Label(form, text="Puissance A:").grid(row=0, column=4, padx=8, pady=8, sticky="w")
		self.puissance_a_entry = ttk.Entry(form, width=14)
		self.puissance_a_entry.grid(row=0, column=5, padx=8, pady=8, sticky="w")

		ttk.Label(form, text="Puissance B:").grid(row=1, column=0, padx=8, pady=8, sticky="w")
		self.puissance_b_entry = ttk.Entry(form, width=18)
		self.puissance_b_entry.grid(row=1, column=1, padx=8, pady=8, sticky="w")

		ttk.Label(form, text="Energie:").grid(row=1, column=2, padx=8, pady=8, sticky="w")
		self.energie_entry = ttk.Entry(form, width=14)
		self.energie_entry.grid(row=1, column=3, padx=8, pady=8, sticky="w")

		ttk.Label(form, text="Prix unitaire:").grid(row=1, column=4, padx=8, pady=8, sticky="w")
		self.prix_unitaire_entry = ttk.Entry(form, width=14)
		self.prix_unitaire_entry.grid(row=1, column=5, padx=8, pady=8, sticky="w")

		ttk.Label(form, text="Prix weekend:").grid(row=2, column=0, padx=8, pady=8, sticky="w")
		self.prix_weekend_entry = ttk.Entry(form, width=18)
		self.prix_weekend_entry.grid(row=2, column=1, padx=8, pady=8, sticky="w")

		buttons = ttk.Frame(self.master)
		buttons.pack(fill="x", padx=12, pady=5)

		ttk.Button(buttons, text="Ajouter", command=self.ajouter).pack(side="left", padx=4)
		ttk.Button(buttons, text="Modifier", command=self.modifier).pack(side="left", padx=4)
		ttk.Button(buttons, text="Supprimer", command=self.supprimer).pack(side="left", padx=4)
		ttk.Button(buttons, text="Vider", command=self.vider).pack(side="left", padx=4)
		ttk.Button(buttons, text="Rafraichir", command=self._load_data).pack(side="left", padx=4)

		table_frame = ttk.LabelFrame(self.master, text="Liste des panneaux")
		table_frame.pack(fill="both", expand=True, padx=12, pady=10)

		columns = ("id", "nom", "rendement", "puissanceA", "puissanceB", "energie", "prixUnitaire", "prixWeekend")
		self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
		self.tree.heading("id", text="ID")
		self.tree.heading("nom", text="Nom")
		self.tree.heading("rendement", text="Rendement")
		self.tree.heading("puissanceA", text="Puissance A")
		self.tree.heading("puissanceB", text="Puissance B")
		self.tree.heading("energie", text="Energie")
		self.tree.heading("prixUnitaire", text="Prix unitaire")
		self.tree.heading("prixWeekend", text="Prix weekend")

		self.tree.column("id", width=70, anchor="center")
		self.tree.column("nom", width=200, anchor="w")
		self.tree.column("rendement", width=120, anchor="center")
		self.tree.column("puissanceA", width=120, anchor="center")
		self.tree.column("puissanceB", width=120, anchor="center")
		self.tree.column("energie", width=120, anchor="center")
		self.tree.column("prixUnitaire", width=130, anchor="center")
		self.tree.column("prixWeekend", width=130, anchor="center")
		self.tree.pack(side="left", fill="both", expand=True)

		sb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
		sb.pack(side="right", fill="y")
		self.tree.configure(yscrollcommand=sb.set)

		self.tree.bind("<<TreeviewSelect>>", self.on_select)

	def _load_data(self):
		for item in self.tree.get_children():
			self.tree.delete(item)

		for pan in self.repo.get_all():
			self.tree.insert(
				"",
				"end",
				values=(
					pan.get_idPanneau(),
					pan.get_nom(),
					pan.get_rendement(),
					pan.get_puissanceA(),
					pan.get_puissanceB(),
					pan.get_energie(),
					pan.get_prixUnitaire(),
					pan.get_prixWeekend(),
				),
			)

	def _validate(self):
		nom = self.nom_entry.get().strip()
		if not nom:
			messagebox.showerror("Validation", "Le nom est obligatoire.")
			return None

		try:
			rendement = float(self.rendement_entry.get().strip())
			puissance_a = float(self.puissance_a_entry.get().strip())
			puissance_b = float(self.puissance_b_entry.get().strip())
			energie = float(self.energie_entry.get().strip())
			prix_unitaire = float(self.prix_unitaire_entry.get().strip())
			prix_weekend_text = self.prix_weekend_entry.get().strip()
			prix_weekend = float(prix_weekend_text) if prix_weekend_text else None
		except ValueError:
			messagebox.showerror("Validation", "Les valeurs numeriques sont invalides.")
			return None

		return nom, rendement, puissance_a, puissance_b, energie, prix_unitaire, prix_weekend

	def ajouter(self):
		data = self._validate()
		if data is None:
			return

		obj = Panneau(None, *data)
		if self.repo.create(obj):
			messagebox.showinfo("Succes", "Panneau ajoute.")
			self._load_data()
			self.vider()
		else:
			messagebox.showerror("Erreur", "Echec de l'ajout.")

	def modifier(self):
		if self.selected_id is None:
			messagebox.showwarning("Modification", "Selectionnez une ligne.")
			return

		data = self._validate()
		if data is None:
			return

		obj = Panneau(self.selected_id, *data)
		if self.repo.update(obj):
			messagebox.showinfo("Succes", "Panneau modifie.")
			self._load_data()
			self.vider()
		else:
			messagebox.showerror("Erreur", "Echec de la modification.")

	def supprimer(self):
		if self.selected_id is None:
			messagebox.showwarning("Suppression", "Selectionnez une ligne.")
			return

		if not messagebox.askyesno("Confirmation", "Supprimer ce panneau ?"):
			return

		if self.repo.delete(self.selected_id):
			messagebox.showinfo("Succes", "Panneau supprime.")
			self._load_data()
			self.vider()
		else:
			messagebox.showerror("Erreur", "Echec de la suppression.")

	def on_select(self, _event):
		selected = self.tree.selection()
		if not selected:
			return

		values = self.tree.item(selected[0], "values")
		self.selected_id = int(values[0])

		self.nom_entry.delete(0, tk.END)
		self.nom_entry.insert(0, values[1])
		self.rendement_entry.delete(0, tk.END)
		self.rendement_entry.insert(0, values[2])
		self.puissance_a_entry.delete(0, tk.END)
		self.puissance_a_entry.insert(0, values[3])
		self.puissance_b_entry.delete(0, tk.END)
		self.puissance_b_entry.insert(0, values[4])
		self.energie_entry.delete(0, tk.END)
		self.energie_entry.insert(0, values[5])
		self.prix_unitaire_entry.delete(0, tk.END)
		self.prix_unitaire_entry.insert(0, values[6])
		self.prix_weekend_entry.delete(0, tk.END)
		self.prix_weekend_entry.insert(0, values[7])

	def vider(self):
		self.selected_id = None
		self.nom_entry.delete(0, tk.END)
		self.rendement_entry.delete(0, tk.END)
		self.puissance_a_entry.delete(0, tk.END)
		self.puissance_b_entry.delete(0, tk.END)
		self.energie_entry.delete(0, tk.END)
		self.prix_unitaire_entry.delete(0, tk.END)
		self.prix_weekend_entry.delete(0, tk.END)


if __name__ == "__main__":
	root = tk.Tk()
	PanneauView(root)
	root.mainloop()
