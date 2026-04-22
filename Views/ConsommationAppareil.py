import tkinter as tk
from tkinter import ttk, messagebox

from Models.Consommation import Consommation
from Repositories.AppareilRepository import AppareilRepository
from Repositories.ConsommationRepository import ConsommationRepository


class ConsommationAppareilView:
    def __init__(self, master):
        self.master = master
        self.master.title("CRUD Consommation Appareil")
        self.master.geometry("900x520")

        self.consommation_repo = ConsommationRepository()
        self.appareil_repo = AppareilRepository()

        self.appareils_map = {}
        self.selected_id_consommation = None

        self._build_ui()
        self._load_appareils()
        self._load_consommations()

    def _build_ui(self):
        form_frame = ttk.LabelFrame(self.master, text="Saisie Consommation")
        form_frame.pack(fill="x", padx=12, pady=10)

        ttk.Label(form_frame, text="Appareil:").grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.appareil_combo = ttk.Combobox(form_frame, state="readonly", width=35)
        self.appareil_combo.grid(row=0, column=1, padx=8, pady=8, sticky="w")

        ttk.Label(form_frame, text="Heure debut (HH:MM):").grid(row=0, column=2, padx=8, pady=8, sticky="w")
        self.heure_debut_entry = ttk.Entry(form_frame, width=20)
        self.heure_debut_entry.grid(row=0, column=3, padx=8, pady=8, sticky="w")

        ttk.Label(form_frame, text="Heure fin (HH:MM):").grid(row=1, column=0, padx=8, pady=8, sticky="w")
        self.heure_fin_entry = ttk.Entry(form_frame, width=20)
        self.heure_fin_entry.grid(row=1, column=1, padx=8, pady=8, sticky="w")

        ttk.Label(form_frame, text="Consommation:").grid(row=1, column=2, padx=8, pady=8, sticky="w")
        self.consommation_entry = ttk.Entry(form_frame, width=20)
        self.consommation_entry.grid(row=1, column=3, padx=8, pady=8, sticky="w")

        button_frame = ttk.Frame(self.master)
        button_frame.pack(fill="x", padx=12, pady=4)

        ttk.Button(button_frame, text="Ajouter", command=self.ajouter).pack(side="left", padx=4)
        ttk.Button(button_frame, text="Modifier", command=self.modifier).pack(side="left", padx=4)
        ttk.Button(button_frame, text="Supprimer", command=self.supprimer).pack(side="left", padx=4)
        ttk.Button(button_frame, text="Vider", command=self.vider_formulaire).pack(side="left", padx=4)
        ttk.Button(button_frame, text="Rafraichir", command=self._load_consommations).pack(side="left", padx=4)

        table_frame = ttk.LabelFrame(self.master, text="Liste des Consommations")
        table_frame.pack(fill="both", expand=True, padx=12, pady=10)

        columns = ("id", "id_appareil", "appareil", "heure_debut", "heure_fin", "consommation")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("id_appareil", text="ID Appareil")
        self.tree.heading("appareil", text="Nom Appareil")
        self.tree.heading("heure_debut", text="Heure debut")
        self.tree.heading("heure_fin", text="Heure fin")
        self.tree.heading("consommation", text="Consommation")

        self.tree.column("id", width=70, anchor="center")
        self.tree.column("id_appareil", width=100, anchor="center")
        self.tree.column("appareil", width=220, anchor="w")
        self.tree.column("heure_debut", width=110, anchor="center")
        self.tree.column("heure_fin", width=110, anchor="center")
        self.tree.column("consommation", width=120, anchor="center")

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def _load_appareils(self):
        appareils = self.appareil_repo.get_all()
        values = []
        self.appareils_map = {}

        for app in appareils:
            key = f"{app.get_idAppareil()} - {app.get_nom()}"
            values.append(key)
            self.appareils_map[key] = app.get_idAppareil()

        self.appareil_combo["values"] = values
        if values:
            self.appareil_combo.current(0)

    def _get_appareil_name(self, id_appareil):
        for key, value in self.appareils_map.items():
            if value == id_appareil:
                parts = key.split(" - ", 1)
                return parts[1] if len(parts) > 1 else key
        return "Inconnu"

    def _load_consommations(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        consommations = self.consommation_repo.get_all()
        for conso in consommations:
            id_app = conso.get_idAppareil()
            self.tree.insert(
                "",
                "end",
                values=(
                    conso.get_idConsommation(),
                    id_app,
                    self._get_appareil_name(id_app),
                    conso.get_heureDebut(),
                    conso.get_heureFin(),
                    conso.get_consommation(),
                ),
            )

    def _validate_inputs(self):
        appareil_label = self.appareil_combo.get().strip()
        heure_debut = self.heure_debut_entry.get().strip()
        heure_fin = self.heure_fin_entry.get().strip()
        consommation = self.consommation_entry.get().strip()

        if not appareil_label:
            messagebox.showerror("Validation", "Veuillez selectionner un appareil.")
            return None

        if appareil_label not in self.appareils_map:
            messagebox.showerror("Validation", "Appareil invalide.")
            return None

        if not heure_debut or not heure_fin:
            messagebox.showerror("Validation", "Veuillez saisir heure debut et heure fin.")
            return None

        try:
            float(consommation)
        except ValueError:
            messagebox.showerror("Validation", "La consommation doit etre numerique.")
            return None

        return (
            self.appareils_map[appareil_label],
            heure_debut,
            heure_fin,
            float(consommation),
        )

    def ajouter(self):
        data = self._validate_inputs()
        if data is None:
            return

        id_appareil, heure_debut, heure_fin, consommation = data
        conso = Consommation(None, id_appareil, heure_debut, heure_fin, consommation)

        if self.consommation_repo.create(conso):
            messagebox.showinfo("Succes", "Consommation ajoutee avec succes.")
            self._load_consommations()
            self.vider_formulaire()
        else:
            messagebox.showerror("Erreur", "Echec lors de l'ajout.")

    def modifier(self):
        if self.selected_id_consommation is None:
            messagebox.showwarning("Modification", "Veuillez selectionner une consommation a modifier.")
            return

        data = self._validate_inputs()
        if data is None:
            return

        id_appareil, heure_debut, heure_fin, consommation = data
        conso = Consommation(
            self.selected_id_consommation,
            id_appareil,
            heure_debut,
            heure_fin,
            consommation,
        )

        if self.consommation_repo.update(conso):
            messagebox.showinfo("Succes", "Consommation modifiee avec succes.")
            self._load_consommations()
            self.vider_formulaire()
        else:
            messagebox.showerror("Erreur", "Echec lors de la modification.")

    def supprimer(self):
        if self.selected_id_consommation is None:
            messagebox.showwarning("Suppression", "Veuillez selectionner une consommation a supprimer.")
            return

        if not messagebox.askyesno("Confirmation", "Supprimer cette consommation ?"):
            return

        if self.consommation_repo.delete(self.selected_id_consommation):
            messagebox.showinfo("Succes", "Consommation supprimee avec succes.")
            self._load_consommations()
            self.vider_formulaire()
        else:
            messagebox.showerror("Erreur", "Echec lors de la suppression.")

    def on_select(self, _event):
        selected = self.tree.selection()
        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        self.selected_id_consommation = int(values[0])
        id_appareil = int(values[1])

        appareil_value = None
        for label, app_id in self.appareils_map.items():
            if app_id == id_appareil:
                appareil_value = label
                break

        if appareil_value:
            self.appareil_combo.set(appareil_value)

        self.heure_debut_entry.delete(0, tk.END)
        self.heure_debut_entry.insert(0, values[3])

        self.heure_fin_entry.delete(0, tk.END)
        self.heure_fin_entry.insert(0, values[4])

        self.consommation_entry.delete(0, tk.END)
        self.consommation_entry.insert(0, values[5])

    def vider_formulaire(self):
        self.selected_id_consommation = None
        self.heure_debut_entry.delete(0, tk.END)
        self.heure_fin_entry.delete(0, tk.END)
        self.consommation_entry.delete(0, tk.END)
        if self.appareil_combo["values"]:
            self.appareil_combo.current(0)


if __name__ == "__main__":
    root = tk.Tk()
    ConsommationAppareilView(root)
    root.mainloop()
