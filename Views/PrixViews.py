import tkinter as tk
from tkinter import ttk, messagebox

from Models.Prix import Prix
from Repositories.PrixRepository import PrixRepository


class PrixView:
	def __init__(self, master):
		self.master = master
		self.master.title("CRUD Prix")
		self.master.geometry("760x520")

		self.repo = PrixRepository()
		self.selected_id = None

		self._build_ui()
		self._load_data()

	def _build_ui(self):
		form = ttk.LabelFrame(self.master, text="Prix")
		form.pack(fill="x", padx=12, pady=10)

		ttk.Label(form, text="Prix unitaire:").grid(row=0, column=0, padx=8, pady=8, sticky="w")
		self.prix_unitaire_entry = ttk.Entry(form, width=20)
		self.prix_unitaire_entry.grid(row=0, column=1, padx=8, pady=8, sticky="w")

		ttk.Label(form, text="Prix weekend:").grid(row=0, column=2, padx=8, pady=8, sticky="w")
		self.prix_weekend_entry = ttk.Entry(form, width=20)
		self.prix_weekend_entry.grid(row=0, column=3, padx=8, pady=8, sticky="w")

		ttk.Label(form, text="Energie solaire:").grid(row=1, column=0, padx=8, pady=8, sticky="w")
		self.energie_solaire_entry = ttk.Entry(form, width=20)
		self.energie_solaire_entry.grid(row=1, column=1, padx=8, pady=8, sticky="w")

		buttons = ttk.Frame(self.master)
		buttons.pack(fill="x", padx=12, pady=5)

		ttk.Button(buttons, text="Ajouter", command=self.ajouter).pack(side="left", padx=4)
		ttk.Button(buttons, text="Modifier", command=self.modifier).pack(side="left", padx=4)
		ttk.Button(buttons, text="Supprimer", command=self.supprimer).pack(side="left", padx=4)
		ttk.Button(buttons, text="Vider", command=self.vider).pack(side="left", padx=4)
		ttk.Button(buttons, text="Rafraichir", command=self._load_data).pack(side="left", padx=4)

		table_frame = ttk.LabelFrame(self.master, text="Liste des prix")
		table_frame.pack(fill="both", expand=True, padx=12, pady=10)

		columns = ("id", "prixUnitaire", "prixWeekend", "EnergieSolaire")
		self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
		self.tree.heading("id", text="ID")
		self.tree.heading("prixUnitaire", text="Prix unitaire")
		self.tree.heading("prixWeekend", text="Prix weekend")
		self.tree.heading("EnergieSolaire", text="Energie solaire")

		self.tree.column("id", width=80, anchor="center")
		self.tree.column("prixUnitaire", width=180, anchor="center")
		self.tree.column("prixWeekend", width=180, anchor="center")
		self.tree.column("EnergieSolaire", width=180, anchor="center")
		self.tree.pack(side="left", fill="both", expand=True)

		sb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
		sb.pack(side="right", fill="y")
		self.tree.configure(yscrollcommand=sb.set)

		self.tree.bind("<<TreeviewSelect>>", self.on_select)

	def _load_data(self):
		for item in self.tree.get_children():
			self.tree.delete(item)

		for prix in self.repo.get_all():
			self.tree.insert(
				"",
				"end",
				values=(
					prix.get_id(),
					prix.get_prixUnitaire(),
					prix.get_prixWeekend(),
					prix.get_EnergieSolaire(),
				),
			)

	def _validate(self):
		prix_unitaire_text = self.prix_unitaire_entry.get().strip()
		prix_weekend_text = self.prix_weekend_entry.get().strip()
		energie_solaire_text = self.energie_solaire_entry.get().strip()

		if not prix_unitaire_text:
			messagebox.showerror("Validation", "Le prix unitaire est obligatoire.")
			return None

		if not energie_solaire_text:
			messagebox.showerror("Validation", "L'energie solaire est obligatoire.")
			return None

		try:
			prix_unitaire = float(prix_unitaire_text)
			prix_weekend = float(prix_weekend_text) if prix_weekend_text else None
			energie_solaire = float(energie_solaire_text)
		except ValueError:
			messagebox.showerror("Validation", "Les valeurs numeriques sont invalides.")
			return None

		return prix_unitaire, prix_weekend, energie_solaire

	def ajouter(self):
		data = self._validate()
		if data is None:
			return

		obj = Prix(None, *data)
		if self.repo.create(obj):
			messagebox.showinfo("Succes", "Prix ajoute.")
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

		obj = Prix(self.selected_id, *data)
		if self.repo.update(obj):
			messagebox.showinfo("Succes", "Prix modifie.")
			self._load_data()
			self.vider()
		else:
			messagebox.showerror("Erreur", "Echec de la modification.")

	def supprimer(self):
		if self.selected_id is None:
			messagebox.showwarning("Suppression", "Selectionnez une ligne.")
			return

		if not messagebox.askyesno("Confirmation", "Supprimer ce prix ?"):
			return

		if self.repo.delete(self.selected_id):
			messagebox.showinfo("Succes", "Prix supprime.")
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

		self.prix_unitaire_entry.delete(0, tk.END)
		self.prix_unitaire_entry.insert(0, values[1])
		self.prix_weekend_entry.delete(0, tk.END)
		self.prix_weekend_entry.insert(0, values[2])
		self.energie_solaire_entry.delete(0, tk.END)
		self.energie_solaire_entry.insert(0, values[3])

	def vider(self):
		self.selected_id = None
		self.prix_unitaire_entry.delete(0, tk.END)
		self.prix_weekend_entry.delete(0, tk.END)
		self.energie_solaire_entry.delete(0, tk.END)


if __name__ == "__main__":
	root = tk.Tk()
	PrixView(root)
	root.mainloop()
