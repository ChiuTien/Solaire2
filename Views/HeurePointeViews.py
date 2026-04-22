import tkinter as tk
from tkinter import ttk, messagebox

from Models.HeurePointe import HeurePointe
from Repositories.HeurePointeRepository import HeurePointeRepository


class HeurePointeView:
	def __init__(self, master):
		self.master = master
		self.master.title("CRUD Heure Pointe")
		self.master.geometry("820x540")

		self.repo = HeurePointeRepository()
		self.selected_id = None

		self._build_ui()
		self._load_data()

	def _build_ui(self):
		form = ttk.LabelFrame(self.master, text="Heure de pointe")
		form.pack(fill="x", padx=12, pady=10)

		ttk.Label(form, text="Heure debut (HH:MM):").grid(row=0, column=0, padx=8, pady=8, sticky="w")
		self.heure_debut_entry = ttk.Entry(form, width=18)
		self.heure_debut_entry.grid(row=0, column=1, padx=8, pady=8, sticky="w")

		ttk.Label(form, text="Heure fin (HH:MM):").grid(row=0, column=2, padx=8, pady=8, sticky="w")
		self.heure_fin_entry = ttk.Entry(form, width=18)
		self.heure_fin_entry.grid(row=0, column=3, padx=8, pady=8, sticky="w")

		ttk.Label(form, text="Pourcentage:").grid(row=1, column=0, padx=8, pady=8, sticky="w")
		self.pourcentage_entry = ttk.Entry(form, width=18)
		self.pourcentage_entry.grid(row=1, column=1, padx=8, pady=8, sticky="w")

		buttons = ttk.Frame(self.master)
		buttons.pack(fill="x", padx=12, pady=5)

		ttk.Button(buttons, text="Ajouter", command=self.ajouter).pack(side="left", padx=4)
		ttk.Button(buttons, text="Modifier", command=self.modifier).pack(side="left", padx=4)
		ttk.Button(buttons, text="Supprimer", command=self.supprimer).pack(side="left", padx=4)
		ttk.Button(buttons, text="Vider", command=self.vider).pack(side="left", padx=4)
		ttk.Button(buttons, text="Rafraichir", command=self._load_data).pack(side="left", padx=4)

		table_frame = ttk.LabelFrame(self.master, text="Liste des heures de pointe")
		table_frame.pack(fill="both", expand=True, padx=12, pady=10)

		columns = ("id", "heureDebut", "heureFin", "pourcentage")
		self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
		self.tree.heading("id", text="ID")
		self.tree.heading("heureDebut", text="Heure debut")
		self.tree.heading("heureFin", text="Heure fin")
		self.tree.heading("pourcentage", text="Pourcentage")

		self.tree.column("id", width=80, anchor="center")
		self.tree.column("heureDebut", width=170, anchor="center")
		self.tree.column("heureFin", width=170, anchor="center")
		self.tree.column("pourcentage", width=160, anchor="center")
		self.tree.pack(side="left", fill="both", expand=True)

		sb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
		sb.pack(side="right", fill="y")
		self.tree.configure(yscrollcommand=sb.set)

		self.tree.bind("<<TreeviewSelect>>", self.on_select)

	def _load_data(self):
		for item in self.tree.get_children():
			self.tree.delete(item)

		for hp in self.repo.get_all():
			self.tree.insert(
				"",
				"end",
				values=(
					hp.get_id(),
					hp.get_heureDebut(),
					hp.get_heureFin(),
					hp.get_pourcentage(),
				),
			)

	def _validate(self):
		heure_debut = self.heure_debut_entry.get().strip()
		heure_fin = self.heure_fin_entry.get().strip()
		pourcentage_text = self.pourcentage_entry.get().strip()

		if not heure_debut or not heure_fin:
			messagebox.showerror("Validation", "Heure debut et heure fin sont obligatoires.")
			return None

		if not pourcentage_text:
			messagebox.showerror("Validation", "Le pourcentage est obligatoire.")
			return None

		try:
			pourcentage = float(pourcentage_text)
		except ValueError:
			messagebox.showerror("Validation", "Le pourcentage doit etre numerique.")
			return None

		return heure_debut, heure_fin, pourcentage

	def ajouter(self):
		data = self._validate()
		if data is None:
			return

		obj = HeurePointe(None, *data)
		if self.repo.create(obj):
			messagebox.showinfo("Succes", "Heure de pointe ajoutee.")
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

		obj = HeurePointe(self.selected_id, *data)
		if self.repo.update(obj):
			messagebox.showinfo("Succes", "Heure de pointe modifiee.")
			self._load_data()
			self.vider()
		else:
			messagebox.showerror("Erreur", "Echec de la modification.")

	def supprimer(self):
		if self.selected_id is None:
			messagebox.showwarning("Suppression", "Selectionnez une ligne.")
			return

		if not messagebox.askyesno("Confirmation", "Supprimer cette heure de pointe ?"):
			return

		if self.repo.delete(self.selected_id):
			messagebox.showinfo("Succes", "Heure de pointe supprimee.")
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

		self.heure_debut_entry.delete(0, tk.END)
		self.heure_debut_entry.insert(0, values[1])
		self.heure_fin_entry.delete(0, tk.END)
		self.heure_fin_entry.insert(0, values[2])
		self.pourcentage_entry.delete(0, tk.END)
		self.pourcentage_entry.insert(0, values[3])

	def vider(self):
		self.selected_id = None
		self.heure_debut_entry.delete(0, tk.END)
		self.heure_fin_entry.delete(0, tk.END)
		self.pourcentage_entry.delete(0, tk.END)


if __name__ == "__main__":
	root = tk.Tk()
	HeurePointeView(root)
	root.mainloop()
