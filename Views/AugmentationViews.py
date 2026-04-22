import tkinter as tk
from tkinter import ttk, messagebox

from Models.Augmentation import Augmentation
from Repositories.AugmentationRepository import AugmentationRepository


class AugmentationView:
	def __init__(self, master):
		self.master = master
		self.master.title("CRUD Augmentation")
		self.master.geometry("980x520")

		self.repo = AugmentationRepository()
		self.selected_id = None

		self._build_ui()
		self._load_data()

	def _build_ui(self):
		form = ttk.LabelFrame(self.master, text="Augmentation")
		form.pack(fill="x", padx=12, pady=10)

		ttk.Label(form, text="% Ouvrable:").grid(row=0, column=0, padx=8, pady=8, sticky="w")
		self.pourcentage_ouvrable_entry = ttk.Entry(form, width=22)
		self.pourcentage_ouvrable_entry.grid(row=0, column=1, padx=8, pady=8, sticky="w")

		ttk.Label(form, text="% Weekend:").grid(row=0, column=2, padx=8, pady=8, sticky="w")
		self.pourcentage_weekend_entry = ttk.Entry(form, width=22)
		self.pourcentage_weekend_entry.grid(row=0, column=3, padx=8, pady=8, sticky="w")

		ttk.Label(form, text="Heure debut (HH:MM):").grid(row=1, column=0, padx=8, pady=8, sticky="w")
		self.heure_debut_entry = ttk.Entry(form, width=22)
		self.heure_debut_entry.grid(row=1, column=1, padx=8, pady=8, sticky="w")

		ttk.Label(form, text="Heure fin (HH:MM):").grid(row=1, column=2, padx=8, pady=8, sticky="w")
		self.heure_fin_entry = ttk.Entry(form, width=22)
		self.heure_fin_entry.grid(row=1, column=3, padx=8, pady=8, sticky="w")

		buttons = ttk.Frame(self.master)
		buttons.pack(fill="x", padx=12, pady=5)

		ttk.Button(buttons, text="Ajouter", command=self.ajouter).pack(side="left", padx=4)
		ttk.Button(buttons, text="Modifier", command=self.modifier).pack(side="left", padx=4)
		ttk.Button(buttons, text="Supprimer", command=self.supprimer).pack(side="left", padx=4)
		ttk.Button(buttons, text="Vider", command=self.vider).pack(side="left", padx=4)
		ttk.Button(buttons, text="Rafraichir", command=self._load_data).pack(side="left", padx=4)

		table_frame = ttk.LabelFrame(self.master, text="Liste des augmentations")
		table_frame.pack(fill="both", expand=True, padx=12, pady=10)

		columns = ("id", "pourcentageOuvrable", "pourcentageWeekend", "heureDebut", "heureFin")
		self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
		self.tree.heading("id", text="ID")
		self.tree.heading("pourcentageOuvrable", text="% Ouvrable")
		self.tree.heading("pourcentageWeekend", text="% Weekend")
		self.tree.heading("heureDebut", text="Heure debut")
		self.tree.heading("heureFin", text="Heure fin")

		self.tree.column("id", width=100, anchor="center")
		self.tree.column("pourcentageOuvrable", width=220, anchor="center")
		self.tree.column("pourcentageWeekend", width=220, anchor="center")
		self.tree.column("heureDebut", width=180, anchor="center")
		self.tree.column("heureFin", width=180, anchor="center")
		self.tree.pack(side="left", fill="both", expand=True)

		sb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
		sb.pack(side="right", fill="y")
		self.tree.configure(yscrollcommand=sb.set)

		self.tree.bind("<<TreeviewSelect>>", self.on_select)

	def _load_data(self):
		for item in self.tree.get_children():
			self.tree.delete(item)

		for augmentation in self.repo.get_all():
			self.tree.insert(
				"",
				"end",
				values=(
					augmentation.get_idAugmentation(),
					augmentation.get_pourcentageOuvrable(),
					augmentation.get_pourcentageWeekend(),
					augmentation.get_heureDebut(),
					augmentation.get_heureFin(),
				),
			)

	def _validate(self):
		pourcentage_ouvrable = self.pourcentage_ouvrable_entry.get().strip()
		pourcentage_weekend = self.pourcentage_weekend_entry.get().strip()
		heure_debut = self.heure_debut_entry.get().strip()
		heure_fin = self.heure_fin_entry.get().strip()

		if not pourcentage_ouvrable or not pourcentage_weekend or not heure_debut or not heure_fin:
			messagebox.showerror("Validation", "Tous les champs sont obligatoires.")
			return None

		try:
			pourcentage_ouvrable = float(pourcentage_ouvrable)
			pourcentage_weekend = float(pourcentage_weekend)
		except ValueError:
			messagebox.showerror("Validation", "Les champs doivent etre numeriques.")
			return None

		return pourcentage_ouvrable, pourcentage_weekend, heure_debut, heure_fin

	def ajouter(self):
		data = self._validate()
		if data is None:
			return

		pourcentage_ouvrable, pourcentage_weekend, heure_debut, heure_fin = data
		obj = Augmentation(None, pourcentage_ouvrable, pourcentage_weekend, heure_debut, heure_fin)

		if self.repo.create(obj):
			messagebox.showinfo("Succes", "Augmentation ajoutee.")
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

		pourcentage_ouvrable, pourcentage_weekend, heure_debut, heure_fin = data
		obj = Augmentation(self.selected_id, pourcentage_ouvrable, pourcentage_weekend, heure_debut, heure_fin)

		if self.repo.update(obj):
			messagebox.showinfo("Succes", "Augmentation modifiee.")
			self._load_data()
			self.vider()
		else:
			messagebox.showerror("Erreur", "Echec de la modification.")

	def supprimer(self):
		if self.selected_id is None:
			messagebox.showwarning("Suppression", "Selectionnez une ligne.")
			return

		if not messagebox.askyesno("Confirmation", "Supprimer cette augmentation ?"):
			return

		if self.repo.delete(self.selected_id):
			messagebox.showinfo("Succes", "Augmentation supprimee.")
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

		self.pourcentage_ouvrable_entry.delete(0, tk.END)
		self.pourcentage_ouvrable_entry.insert(0, values[1])
		self.pourcentage_weekend_entry.delete(0, tk.END)
		self.pourcentage_weekend_entry.insert(0, values[2])
		self.heure_debut_entry.delete(0, tk.END)
		self.heure_debut_entry.insert(0, values[3])
		self.heure_fin_entry.delete(0, tk.END)
		self.heure_fin_entry.insert(0, values[4])

	def vider(self):
		self.selected_id = None
		self.pourcentage_ouvrable_entry.delete(0, tk.END)
		self.pourcentage_weekend_entry.delete(0, tk.END)
		self.heure_debut_entry.delete(0, tk.END)
		self.heure_fin_entry.delete(0, tk.END)


if __name__ == "__main__":
	root = tk.Tk()
	AugmentationView(root)
	root.mainloop()
