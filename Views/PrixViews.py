import tkinter as tk
from tkinter import ttk, messagebox

from Models.Prix import Prix
from Repositories.PrixRepository import PrixRepository


class PrixView:
	def __init__(self, master):
		self.master = master
		self.master.title("CRUD Prix")
		self.master.geometry("900x560")

		self.repo = PrixRepository()
		self.selected_id = None

		self._build_ui()
		self._load_data()

	def _build_ui(self):
		form = ttk.LabelFrame(self.master, text="Configuration Prix")
		form.pack(fill="x", padx=12, pady=10)

		ttk.Label(form, text="Prix ouvrable:").grid(row=0, column=0, padx=8, pady=8, sticky="w")
		self.prix_ouvrable_entry = ttk.Entry(form, width=20)
		self.prix_ouvrable_entry.grid(row=0, column=1, padx=8, pady=8, sticky="w")

		ttk.Label(form, text="Prix weekend:").grid(row=0, column=2, padx=8, pady=8, sticky="w")
		self.prix_weekend_entry = ttk.Entry(form, width=20)
		self.prix_weekend_entry.grid(row=0, column=3, padx=8, pady=8, sticky="w")

		ttk.Label(form, text="Puissance:").grid(row=1, column=0, padx=8, pady=8, sticky="w")
		self.puissance_entry = ttk.Entry(form, width=20)
		self.puissance_entry.grid(row=1, column=1, padx=8, pady=8, sticky="w")

		buttons = ttk.Frame(self.master)
		buttons.pack(fill="x", padx=12, pady=5)

		ttk.Button(buttons, text="Ajouter", command=self.ajouter).pack(side="left", padx=4)
		ttk.Button(buttons, text="Modifier", command=self.modifier).pack(side="left", padx=4)
		ttk.Button(buttons, text="Supprimer", command=self.supprimer).pack(side="left", padx=4)
		ttk.Button(buttons, text="Vider", command=self.vider).pack(side="left", padx=4)
		ttk.Button(buttons, text="Rafraichir", command=self._load_data).pack(side="left", padx=4)

		table_frame = ttk.LabelFrame(self.master, text="Liste des configurations")
		table_frame.pack(fill="both", expand=True, padx=12, pady=10)

		columns = ("id", "prix_ouvrable", "prix_weekend", "puissance")
		self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
		self.tree.heading("id", text="ID")
		self.tree.heading("prix_ouvrable", text="Prix ouvrable")
		self.tree.heading("prix_weekend", text="Prix weekend")
		self.tree.heading("puissance", text="Puissance")

		self.tree.column("id", width=70, anchor="center")
		self.tree.column("prix_ouvrable", width=200, anchor="center")
		self.tree.column("prix_weekend", width=200, anchor="center")
		self.tree.column("puissance", width=180, anchor="center")
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
					prix.get_idPrix(),
					prix.get_prixOuvrable(),
					prix.get_prixWeekend(),
					prix.get_puissance(),
				),
			)

	def _validate(self):
		try:
			prix_ouvrable = float(self.prix_ouvrable_entry.get().strip())
			prix_weekend = float(self.prix_weekend_entry.get().strip())
			puissance_txt = self.puissance_entry.get().strip()
			puissance = float(puissance_txt) if puissance_txt else None
		except ValueError:
			messagebox.showerror("Validation", "Les valeurs doivent etre numeriques.")
			return None

		return prix_ouvrable, prix_weekend, puissance

	def ajouter(self):
		data = self._validate()
		if data is None:
			return

		prix_ouvrable, prix_weekend, puissance = data
		obj = Prix(None, prix_ouvrable, prix_weekend, puissance)

		if self.repo.create(obj):
			messagebox.showinfo("Succes", "Configuration prix ajoutee.")
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

		prix_ouvrable, prix_weekend, puissance = data
		obj = Prix(self.selected_id, prix_ouvrable, prix_weekend, puissance)

		if self.repo.update(obj):
			messagebox.showinfo("Succes", "Configuration prix modifiee.")
			self._load_data()
			self.vider()
		else:
			messagebox.showerror("Erreur", "Echec de la modification.")

	def supprimer(self):
		if self.selected_id is None:
			messagebox.showwarning("Suppression", "Selectionnez une ligne.")
			return

		if not messagebox.askyesno("Confirmation", "Supprimer cette configuration prix ?"):
			return

		if self.repo.delete(self.selected_id):
			messagebox.showinfo("Succes", "Configuration prix supprimee.")
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

		self.prix_ouvrable_entry.delete(0, tk.END)
		self.prix_ouvrable_entry.insert(0, values[1])
		self.prix_weekend_entry.delete(0, tk.END)
		self.prix_weekend_entry.insert(0, values[2])
		self.puissance_entry.delete(0, tk.END)
		self.puissance_entry.insert(0, values[3])

	def vider(self):
		self.selected_id = None
		self.prix_ouvrable_entry.delete(0, tk.END)
		self.prix_weekend_entry.delete(0, tk.END)
		self.puissance_entry.delete(0, tk.END)


if __name__ == "__main__":
	root = tk.Tk()
	PrixView(root)
	root.mainloop()
