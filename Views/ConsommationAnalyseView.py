import tkinter as tk
from tkinter import ttk, messagebox

from Repositories.AppareilRepository import AppareilRepository
from Repositories.ConsommationRepository import ConsommationRepository
from Repositories.EnergieSolaireRepository import EnergieSolaireRepository
from Repositories.HeurePointeRepository import HeurePointeRepository
from Repositories.PrixRepository import PrixRepository
from Services.ConsommationService import ConsommationService
from Services.PanneauService import PanneauService
from Services.PrixPuissanceJournaliereRestante import prix_achat


class ConsommationAnalyseView:
    ALL_APPS_LABEL = "Tous les appareils"

    def __init__(self, master):
        self.master = master
        self.master.title("Analyse Consommation")
        self.master.geometry("1180x700")

        self.appareil_repo = AppareilRepository()
        self.consommation_repo = ConsommationRepository()
        self.energie_repo = EnergieSolaireRepository()
        self.heure_pointe_repo = HeurePointeRepository()
        self.prix_repo = PrixRepository()

        self.appareils_map = {}
        self.prix_map = {}

        self._build_ui()
        self._load_appareils()
        self._load_prix()

    def _build_ui(self):
        top = ttk.LabelFrame(self.master, text="Parametres")
        top.pack(fill="x", padx=12, pady=10)

        ttk.Label(top, text="Appareil:").grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.appareil_combo = ttk.Combobox(top, state="readonly", width=35)
        self.appareil_combo.grid(row=0, column=1, padx=8, pady=8, sticky="w")

        ttk.Label(top, text="Tarif (table prix):").grid(row=1, column=0, padx=8, pady=8, sticky="w")
        self.prix_combo = ttk.Combobox(top, state="readonly", width=35)
        self.prix_combo.grid(row=1, column=1, padx=8, pady=8, sticky="w")
        self.prix_combo.bind("<<ComboboxSelected>>", self.on_prix_selected)

        ttk.Label(top, text="Prix journaliere:").grid(row=0, column=3, padx=8, pady=8, sticky="w")
        self.prix_journaliere_entry = ttk.Entry(top, width=18)
        self.prix_journaliere_entry.grid(row=0, column=4, padx=8, pady=8, sticky="w")

        ttk.Label(top, text="Prix weekend:").grid(row=1, column=3, padx=8, pady=8, sticky="w")
        self.prix_weekend_entry = ttk.Entry(top, width=18)
        self.prix_weekend_entry.grid(row=1, column=4, padx=8, pady=8, sticky="w")

        ttk.Label(top, text="Energie elementaire:").grid(row=2, column=3, padx=8, pady=8, sticky="w")
        self.energie_unitaire_entry = ttk.Entry(top, width=18)
        self.energie_unitaire_entry.grid(row=2, column=4, padx=8, pady=8, sticky="w")

        ttk.Button(top, text="Calculer", command=self.calculer).grid(row=0, column=2, padx=8, pady=8)

        summary = ttk.LabelFrame(self.master, text="Resultats")
        summary.pack(fill="x", padx=12, pady=4)

        self.pic_var = tk.StringVar(value="Pic: -")
        self.puissance_scolaire_var = tk.StringVar(value="Puissance scolaire: -")
        self.puissance_restante_var = tk.StringVar(value="Puissance restante: -")
        self.prix_journalier_var = tk.StringVar(value="Prix achat (journalier): -")
        self.prix_weekend_var = tk.StringVar(value="Prix achat (weekend): -")

        ttk.Label(summary, textvariable=self.pic_var).grid(row=0, column=0, padx=12, pady=8, sticky="w")
        ttk.Label(summary, textvariable=self.puissance_scolaire_var).grid(row=0, column=1, padx=12, pady=8, sticky="w")
        ttk.Label(summary, textvariable=self.puissance_restante_var).grid(row=0, column=2, padx=12, pady=8, sticky="w")
        ttk.Label(summary, textvariable=self.prix_journalier_var).grid(row=1, column=0, padx=12, pady=8, sticky="w")
        ttk.Label(summary, textvariable=self.prix_weekend_var).grid(row=1, column=1, padx=12, pady=8, sticky="w")

        tables = ttk.Frame(self.master)
        tables.pack(fill="both", expand=True, padx=12, pady=8)

        left = ttk.LabelFrame(tables, text="Consommation journee (fusionnee)")
        left.pack(side="left", fill="both", expand=True, padx=(0, 6))

        right = ttk.LabelFrame(tables, text="Consommation soiree")
        right.pack(side="left", fill="both", expand=True, padx=(6, 0))

        columns = ("id_appareil", "debut", "fin", "conso")
        self.tree_journee = ttk.Treeview(left, columns=columns, show="headings")
        self.tree_soiree = ttk.Treeview(right, columns=columns, show="headings")

        for tree in (self.tree_journee, self.tree_soiree):
            tree.heading("id_appareil", text="ID Appareil")
            tree.heading("debut", text="Heure debut")
            tree.heading("fin", text="Heure fin")
            tree.heading("conso", text="Consommation")
            tree.column("id_appareil", width=90, anchor="center")
            tree.column("debut", width=120, anchor="center")
            tree.column("fin", width=120, anchor="center")
            tree.column("conso", width=130, anchor="center")

        self.tree_journee.pack(side="left", fill="both", expand=True)
        self.tree_soiree.pack(side="left", fill="both", expand=True)

        sb_j = ttk.Scrollbar(left, orient="vertical", command=self.tree_journee.yview)
        sb_j.pack(side="right", fill="y")
        self.tree_journee.configure(yscrollcommand=sb_j.set)

        sb_s = ttk.Scrollbar(right, orient="vertical", command=self.tree_soiree.yview)
        sb_s.pack(side="right", fill="y")
        self.tree_soiree.configure(yscrollcommand=sb_s.set)

    def _load_appareils(self):
        appareils = self.appareil_repo.get_all()
        values = [self.ALL_APPS_LABEL]
        self.appareils_map = {}

        for app in appareils:
            label = f"{app.get_idAppareil()} - {app.get_nom()}"
            values.append(label)
            self.appareils_map[label] = app.get_idAppareil()

        self.appareil_combo["values"] = values
        if values:
            self.appareil_combo.current(0)

    def _load_prix(self):
        prix_list = self.prix_repo.get_all()
        values = []
        self.prix_map = {}

        for prix in prix_list:
            label = f"{prix.get_id()} - PU:{prix.get_prixUnitaire()} - PW:{prix.get_prixWeekend()}"
            values.append(label)
            self.prix_map[label] = prix

        self.prix_combo["values"] = values
        if values:
            self.prix_combo.current(0)
            self._fill_prix_fields(values[0])

    def _fill_prix_fields(self, label):
        prix = self.prix_map.get(label)
        if prix is None:
            return

        self.prix_journaliere_entry.delete(0, tk.END)
        self.prix_journaliere_entry.insert(0, str(prix.get_prixUnitaire() or ""))

        self.prix_weekend_entry.delete(0, tk.END)
        self.prix_weekend_entry.insert(0, str(prix.get_prixWeekend() or ""))

        self.energie_unitaire_entry.delete(0, tk.END)
        self.energie_unitaire_entry.insert(0, str(prix.get_EnergieSolaire() or ""))

    def on_prix_selected(self, _event):
        self._fill_prix_fields(self.prix_combo.get().strip())

    def _clear_trees(self):
        for tree in (self.tree_journee, self.tree_soiree):
            for item in tree.get_children():
                tree.delete(item)

    @staticmethod
    def _as_values(consommation):
        return (
            consommation.get_idAppareil(),
            consommation.get_heureDebut(),
            consommation.get_heureFin(),
            consommation.get_consommation(),
        )

    def calculer(self):
        selection = self.appareil_combo.get().strip()
        if not selection:
            messagebox.showwarning("Analyse", "Veuillez selectionner un appareil.")
            return

        if selection == self.ALL_APPS_LABEL:
            consommations = self.consommation_repo.get_all()
            message_aucune_conso = "Aucune consommation trouvee."
        else:
            if selection not in self.appareils_map:
                messagebox.showwarning("Analyse", "Veuillez selectionner un appareil valide.")
                return

            id_appareil = self.appareils_map[selection]
            consommations = self.consommation_repo.get_by_appareil_id(id_appareil)
            message_aucune_conso = "Aucune consommation trouvee pour cet appareil."

        energie_solaires = self.energie_repo.get_all()
        heure_pointes = self.heure_pointe_repo.get_all()

        if not consommations:
            messagebox.showinfo("Analyse", message_aucune_conso)
            self._clear_trees()
            self.pic_var.set("Pic: -")
            self.puissance_scolaire_var.set("Puissance scolaire: -")
            self.puissance_restante_var.set("Puissance restante: -")
            self.prix_journalier_var.set("Prix achat (journalier): -")
            self.prix_weekend_var.set("Prix achat (weekend): -")
            return

        consommation_journee = ConsommationService.retourner_consommation_journee(consommations)
        consommation_soiree = ConsommationService.retourner_consommation_soiree(consommations)
        consommation_journee_fusionnee = PanneauService.calculer_consommation_fusionnee(consommation_journee)

        pic = PanneauService.retourner_pic(consommation_journee_fusionnee)
        puissance_scolaire = PanneauService.calcul_puissance_scolaire(consommation_journee_fusionnee, energie_solaires)
        puissance_restante = PanneauService.calcul_puissance_restante(consommation_journee_fusionnee, energie_solaires)

        try:
            energie_unitaire = float(self.energie_unitaire_entry.get().strip())
            prix_journaliere = float(self.prix_journaliere_entry.get().strip())
            prix_weekend_text = self.prix_weekend_entry.get().strip()
            prix_weekend = float(prix_weekend_text) if prix_weekend_text else prix_journaliere
        except ValueError:
            messagebox.showerror(
                "Analyse",
                "Prix journaliere, prix weekend et energie elementaire doivent etre numeriques.",
            )
            return

        # Utilisation de la nouvelle fonction prix_achat.
        prix_journalier_achat, prix_weekend_achat = prix_achat(
            consommation_restante=puissance_restante,
            energie_unitaire=energie_unitaire,
            prix_journaliere=prix_journaliere,
            prix_weekend=prix_weekend,
            consommations_journee=consommation_journee_fusionnee,
            heure_pointes=heure_pointes,
        )

        self._clear_trees()
        for conso in consommation_journee_fusionnee:
            self.tree_journee.insert("", "end", values=self._as_values(conso))

        for conso in consommation_soiree:
            self.tree_soiree.insert("", "end", values=self._as_values(conso))

        if pic is None:
            self.pic_var.set("Pic: -")
        else:
            self.pic_var.set(
                f"Pic: {pic.get_heureDebut()} - {pic.get_heureFin()} = {pic.get_consommation()}"
            )

        self.puissance_scolaire_var.set(f"Puissance scolaire: {puissance_scolaire}")
        self.puissance_restante_var.set(f"Puissance restante: {puissance_restante}")
        self.prix_journalier_var.set(f"Prix achat (journalier): {prix_journalier_achat}")
        self.prix_weekend_var.set(f"Prix achat (weekend): {prix_weekend_achat}")


if __name__ == "__main__":
    root = tk.Tk()
    ConsommationAnalyseView(root)
    root.mainloop()
