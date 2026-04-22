import tkinter as tk
from tkinter import ttk, messagebox

from Models.Batterie import Batterie
from Repositories.BatterieRepository import BatterieRepository


class BatterieView:
	def __init__(self, master):
		self.master = master
		self.master.title("CRUD Batterie")
		self.master.geometry("980x560")

		self.repo = BatterieRepository()
		self.selected_id = None

		self._build_ui()
		self._load_data()

	def _build_ui(self):
		form = ttk.LabelFrame(self.master, text="Batterie")
		form.pack(fill="x", padx=12, pady=10)

		ttk.Label(form, text="Nom:").grid(row=0, column=0, padx=8, pady=8, sticky="w")
		self.nom_entry = ttk.Entry(form, width=24)
		self.nom_entry.grid(row=0, column=1, padx=8, pady=8, sticky="w")

		ttk.Label(form, text="Rendement:").grid(row=0, column=2, padx=8, pady=8, sticky="w")
		self.rendement_entry = ttk.Entry(form, width=16)
		self.rendement_entry.grid(row=0, column=3, padx=8, pady=8, sticky="w")

		ttk.Label(form, text="Capacite:").grid(row=1, column=0, padx=8, pady=8, sticky="w")
		self.capacite_entry = ttk.Entry(form, width=24)
		self.capacite_entry.grid(row=1, column=1, padx=8, pady=8, sticky="w")

		ttk.Label(form, text="Charge debut (HH:MM):").grid(row=1, column=2, padx=8, pady=8, sticky="w")
		self.charge_debut_entry = ttk.Entry(form, width=16)
		self.charge_debut_entry.grid(row=1, column=3, padx=8, pady=8, sticky="w")

		ttk.Label(form, text="Charge fin (HH:MM):").grid(row=1, column=4, padx=8, pady=8, sticky="w")
		self.charge_fin_entry = ttk.Entry(form, width=16)
		self.charge_fin_entry.grid(row=1, column=5, padx=8, pady=8, sticky="w")

		buttons = ttk.Frame(self.master)
		buttons.pack(fill="x", padx=12, pady=5)

		ttk.Button(buttons, text="Ajouter", command=self.ajouter).pack(side="left", padx=4)
		ttk.Button(buttons, text="Modifier", command=self.modifier).pack(side="left", padx=4)
		ttk.Button(buttons, text="Supprimer", command=self.supprimer).pack(side="left", padx=4)
		ttk.Button(buttons, text="Vider", command=self.vider).pack(side="left", padx=4)
		ttk.Button(buttons, text="Rafraichir", command=self._load_data).pack(side="left", padx=4)

		table_frame = ttk.LabelFrame(self.master, text="Liste des batteries")
		table_frame.pack(fill="both", expand=True, padx=12, pady=10)

		columns = ("id", "nom", "rendement", "capacite", "chargeDebut", "chargeFin")
		self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
		self.tree.heading("id", text="ID")
		self.tree.heading("nom", text="Nom")
		self.tree.heading("rendement", text="Rendement")
		self.tree.heading("capacite", text="Capacite")
		self.tree.heading("chargeDebut", text="Charge debut")
		self.tree.heading("chargeFin", text="Charge fin")

		self.tree.column("id", width=70, anchor="center")
		self.tree.column("nom", width=220, anchor="w")
		self.tree.column("rendement", width=120, anchor="center")
		self.tree.column("capacite", width=120, anchor="center")
		self.tree.column("chargeDebut", width=120, anchor="center")
		self.tree.column("chargeFin", width=120, anchor="center")
		self.tree.pack(side="left", fill="both", expand=True)

		sb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
		sb.pack(side="right", fill="y")
		self.tree.configure(yscrollcommand=sb.set)

		self.tree.bind("<<TreeviewSelect>>", self.on_select)

	def _load_data(self):
		for item in self.tree.get_children():
			self.tree.delete(item)

		for bat in self.repo.get_all():
			self.tree.insert(
				"",
				"end",
				values=(
					bat.get_idBatterie(),
					bat.get_nom(),
					bat.get_rendement(),
					bat.get_capacite(),
					bat.get_chargeDebut(),
					bat.get_chargeFin(),
				),
			)

	def _validate(self):
		nom = self.nom_entry.get().strip()
		rendement = self.rendement_entry.get().strip()
		capacite = self.capacite_entry.get().strip()
		charge_debut = self.charge_debut_entry.get().strip()
		charge_fin = self.charge_fin_entry.get().strip()

		if not nom:
			messagebox.showerror("Validation", "Le nom est obligatoire.")
			return None

		try:
			rendement = float(rendement)
			capacite = float(capacite) if capacite else None
		except ValueError:
			messagebox.showerror("Validation", "Rendement/Capacite doivent etre numeriques.")
			return None

		return nom, rendement, capacite, charge_debut or None, charge_fin or None

	def ajouter(self):
		data = self._validate()
		if data is None:
			return

		nom, rendement, capacite, charge_debut, charge_fin = data
		obj = Batterie(None, nom, rendement, capacite, charge_debut, charge_fin)

		if self.repo.create(obj):
			messagebox.showinfo("Succes", "Batterie ajoutee.")
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

		nom, rendement, capacite, charge_debut, charge_fin = data
		obj = Batterie(self.selected_id, nom, rendement, capacite, charge_debut, charge_fin)

		if self.repo.update(obj):
			messagebox.showinfo("Succes", "Batterie modifiee.")
			self._load_data()
			self.vider()
		else:
			messagebox.showerror("Erreur", "Echec de la modification.")

	def supprimer(self):
		if self.selected_id is None:
			messagebox.showwarning("Suppression", "Selectionnez une ligne.")
			return

		if not messagebox.askyesno("Confirmation", "Supprimer cette batterie ?"):
			return

		if self.repo.delete(self.selected_id):
			messagebox.showinfo("Succes", "Batterie supprimee.")
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
		self.capacite_entry.delete(0, tk.END)
		self.capacite_entry.insert(0, values[3])
		self.charge_debut_entry.delete(0, tk.END)
		self.charge_debut_entry.insert(0, values[4])
		self.charge_fin_entry.delete(0, tk.END)
		self.charge_fin_entry.insert(0, values[5])

	def vider(self):
		self.selected_id = None
		self.nom_entry.delete(0, tk.END)
		self.rendement_entry.delete(0, tk.END)
		self.capacite_entry.delete(0, tk.END)
		self.charge_debut_entry.delete(0, tk.END)
		self.charge_fin_entry.delete(0, tk.END)


if __name__ == "__main__":
	root = tk.Tk()
	BatterieView(root)
	root.mainloop()
