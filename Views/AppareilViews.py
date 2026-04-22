import tkinter as tk
from tkinter import ttk, messagebox

from Models.Appareil import Appareil
from Repositories.AppareilRepository import AppareilRepository


class AppareilView:
	def __init__(self, master):
		self.master = master
		self.master.title("CRUD Appareil")
		self.master.geometry("620x450")

		self.repo = AppareilRepository()
		self.selected_id = None

		self._build_ui()
		self._load_data()

	def _build_ui(self):
		form = ttk.LabelFrame(self.master, text="Appareil")
		form.pack(fill="x", padx=12, pady=10)

		ttk.Label(form, text="Nom:").grid(row=0, column=0, padx=8, pady=8, sticky="w")
		self.nom_entry = ttk.Entry(form, width=45)
		self.nom_entry.grid(row=0, column=1, padx=8, pady=8, sticky="w")

		buttons = ttk.Frame(self.master)
		buttons.pack(fill="x", padx=12, pady=5)

		ttk.Button(buttons, text="Ajouter", command=self.ajouter).pack(side="left", padx=4)
		ttk.Button(buttons, text="Modifier", command=self.modifier).pack(side="left", padx=4)
		ttk.Button(buttons, text="Supprimer", command=self.supprimer).pack(side="left", padx=4)
		ttk.Button(buttons, text="Vider", command=self.vider).pack(side="left", padx=4)
		ttk.Button(buttons, text="Rafraichir", command=self._load_data).pack(side="left", padx=4)

		table_frame = ttk.LabelFrame(self.master, text="Liste des appareils")
		table_frame.pack(fill="both", expand=True, padx=12, pady=10)

		self.tree = ttk.Treeview(table_frame, columns=("id", "nom"), show="headings")
		self.tree.heading("id", text="ID")
		self.tree.heading("nom", text="Nom")
		self.tree.column("id", width=80, anchor="center")
		self.tree.column("nom", width=460, anchor="w")
		self.tree.pack(side="left", fill="both", expand=True)

		sb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
		sb.pack(side="right", fill="y")
		self.tree.configure(yscrollcommand=sb.set)

		self.tree.bind("<<TreeviewSelect>>", self.on_select)

	def _load_data(self):
		for item in self.tree.get_children():
			self.tree.delete(item)

		for app in self.repo.get_all():
			self.tree.insert("", "end", values=(app.get_idAppareil(), app.get_nom()))

	def _validate(self):
		nom = self.nom_entry.get().strip()
		if not nom:
			messagebox.showerror("Validation", "Le nom est obligatoire.")
			return None
		return nom

	def ajouter(self):
		nom = self._validate()
		if nom is None:
			return

		if self.repo.create(Appareil(None, nom)):
			messagebox.showinfo("Succes", "Appareil ajoute.")
			self._load_data()
			self.vider()
		else:
			messagebox.showerror("Erreur", "Echec de l'ajout.")

	def modifier(self):
		if self.selected_id is None:
			messagebox.showwarning("Modification", "Selectionnez une ligne.")
			return

		nom = self._validate()
		if nom is None:
			return

		if self.repo.update(Appareil(self.selected_id, nom)):
			messagebox.showinfo("Succes", "Appareil modifie.")
			self._load_data()
			self.vider()
		else:
			messagebox.showerror("Erreur", "Echec de la modification.")

	def supprimer(self):
		if self.selected_id is None:
			messagebox.showwarning("Suppression", "Selectionnez une ligne.")
			return

		if not messagebox.askyesno("Confirmation", "Supprimer cet appareil ?"):
			return

		if self.repo.delete(self.selected_id):
			messagebox.showinfo("Succes", "Appareil supprime.")
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

	def vider(self):
		self.selected_id = None
		self.nom_entry.delete(0, tk.END)


if __name__ == "__main__":
	root = tk.Tk()
	AppareilView(root)
	root.mainloop()
