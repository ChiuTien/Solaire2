import tkinter as tk
from tkinter import ttk, messagebox

from Repositories.AppareilRepository import AppareilRepository
from Repositories.AugmentationRepository import AugmentationRepository
from Repositories.ConsommationRepository import ConsommationRepository
from Repositories.EnergieSolaireRepository import EnergieSolaireRepository
from Repositories.PanneauRepository import PanneauRepository
from Repositories.PrixRepository import PrixRepository
from Services.ConsommationService import ConsommationService
from Services.PanneauService import PanneauService
from Services.PrixPuissanceJournaliereRestante import calcul_augmentation, prix_achat


class ConsommationAnalyseView:
    ALL_APPS_LABEL = "Tous les appareils"

    def __init__(self, master):
        self.master = master
        self.master.title("Analyse Consommation")
        self.master.geometry("1180x700")

        self.appareil_repo = AppareilRepository()
        self.consommation_repo = ConsommationRepository()
        self.energie_repo = EnergieSolaireRepository()
        self.panneau_repo = PanneauRepository()
        self.prix_repo = PrixRepository()
        self.augmentation_repo = AugmentationRepository()

        self.appareils_map = {}
        self.panneaux_map = {}
        self.prix_configs_map = {}

        self._build_ui()
        self._load_appareils()
        self._load_panneaux()
        self._load_prix_configs()

    def _build_ui(self):
        top = ttk.LabelFrame(self.master, text="Parametres")
        top.pack(fill="x", padx=12, pady=10)

        ttk.Label(top, text="Appareil:").grid(row=0, column=0, padx=8, pady=8, sticky="w")
        self.appareil_combo = ttk.Combobox(top, state="readonly", width=35)
        self.appareil_combo.grid(row=0, column=1, padx=8, pady=8, sticky="w")

        ttk.Label(top, text="Panneau:").grid(row=1, column=0, padx=8, pady=8, sticky="w")
        self.panneau_combo = ttk.Combobox(top, state="readonly", width=35)
        self.panneau_combo.grid(row=1, column=1, padx=8, pady=8, sticky="w")
        self.panneau_combo.bind("<<ComboboxSelected>>", self.on_panneau_selected)

        ttk.Label(top, text="Configuration prix:").grid(row=0, column=3, padx=8, pady=8, sticky="w")
        self.prix_config_combo = ttk.Combobox(top, state="readonly", width=35)
        self.prix_config_combo.grid(row=0, column=4, padx=8, pady=8, sticky="w")

        ttk.Label(top, text="Energie elementaire:").grid(row=2, column=3, padx=8, pady=8, sticky="w")
        self.energie_unitaire_entry = ttk.Entry(top, width=18)
        self.energie_unitaire_entry.grid(row=2, column=4, padx=8, pady=8, sticky="w")

        ttk.Button(top, text="Calculer", command=self.calculer).grid(row=0, column=2, padx=8, pady=8)

        summary = ttk.LabelFrame(self.master, text="Resultats")
        summary.pack(fill="x", padx=12, pady=4)

        self.pic_var = tk.StringVar(value="Pic: -")
        self.puissance_scolaire_var = tk.StringVar(value="Puissance scolaire: -")
        self.puissance_restante_var = tk.StringVar(value="Puissance restante: -")
        self.prix_journalier_var = tk.StringVar(value="Prix achat (ouvrable): -")
        self.prix_weekend_var = tk.StringVar(value="Prix achat (weekend): -")
        self.augmentation_ouvrable_var = tk.StringVar(value="Supplement augmentation (ouvrable): -")
        self.augmentation_weekend_var = tk.StringVar(value="Supplement augmentation (weekend): -")
        self.prix_total_ouvrable_var = tk.StringVar(value="Total ouvrable: -")
        self.prix_total_weekend_var = tk.StringVar(value="Total weekend: -")
        self.augmentations_appliquees_var = tk.StringVar(value="Augmentations appliquees: -")

        ttk.Label(summary, textvariable=self.pic_var).grid(row=0, column=0, padx=12, pady=8, sticky="w")
        ttk.Label(summary, textvariable=self.puissance_scolaire_var).grid(row=0, column=1, padx=12, pady=8, sticky="w")
        ttk.Label(summary, textvariable=self.puissance_restante_var).grid(row=0, column=2, padx=12, pady=8, sticky="w")
        ttk.Label(summary, textvariable=self.prix_journalier_var).grid(row=1, column=0, padx=12, pady=8, sticky="w")
        ttk.Label(summary, textvariable=self.prix_weekend_var).grid(row=1, column=1, padx=12, pady=8, sticky="w")
        ttk.Label(summary, textvariable=self.augmentation_ouvrable_var).grid(row=2, column=0, padx=12, pady=8, sticky="w")
        ttk.Label(summary, textvariable=self.augmentation_weekend_var).grid(row=2, column=1, padx=12, pady=8, sticky="w")
        ttk.Label(summary, textvariable=self.prix_total_ouvrable_var).grid(row=3, column=0, padx=12, pady=8, sticky="w")
        ttk.Label(summary, textvariable=self.prix_total_weekend_var).grid(row=3, column=1, padx=12, pady=8, sticky="w")
        ttk.Label(summary, textvariable=self.augmentations_appliquees_var).grid(row=4, column=0, columnspan=3, padx=12, pady=8, sticky="w")

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

    def _load_panneaux(self):
        panneaux = self.panneau_repo.get_all()
        values = []
        self.panneaux_map = {}

        for panneau in panneaux:
            label = f"{panneau.get_idPanneau()} - {panneau.get_nom()}"
            values.append(label)
            self.panneaux_map[label] = panneau

        self.panneau_combo["values"] = values
        if values:
            self.panneau_combo.current(0)
            self._fill_panneau_fields(values[0])

    def _load_prix_configs(self):
        prix_list = self.prix_repo.get_all()
        values = []
        self.prix_configs_map = {}

        for prix in prix_list:
            label = (
                f"{prix.get_idPrix()} - Ouvrable: {prix.get_prixOuvrable()} | "
                f"Weekend: {prix.get_prixWeekend()}"
            )
            values.append(label)
            self.prix_configs_map[label] = prix

        self.prix_config_combo["values"] = values
        if values:
            self.prix_config_combo.current(len(values) - 1)

    def _fill_panneau_fields(self, label):
        panneau = self.panneaux_map.get(label)
        if panneau is None:
            return

        self.energie_unitaire_entry.delete(0, tk.END)
        self.energie_unitaire_entry.insert(0, str(panneau.get_energie() or ""))

    def on_panneau_selected(self, _event):
        self._fill_panneau_fields(self.panneau_combo.get().strip())

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

        if not consommations:
            messagebox.showinfo("Analyse", message_aucune_conso)
            self._clear_trees()
            self.pic_var.set("Pic: -")
            self.puissance_scolaire_var.set("Puissance scolaire: -")
            self.puissance_restante_var.set("Puissance restante: -")
            self.prix_journalier_var.set("Prix achat (ouvrable): -")
            self.prix_weekend_var.set("Prix achat (weekend): -")
            self.augmentation_ouvrable_var.set("Supplement augmentation (ouvrable): -")
            self.augmentation_weekend_var.set("Supplement augmentation (weekend): -")
            self.prix_total_ouvrable_var.set("Total ouvrable: -")
            self.prix_total_weekend_var.set("Total weekend: -")
            self.augmentations_appliquees_var.set("Augmentations appliquees: -")
            return

        consommation_journee = ConsommationService.retourner_consommation_journee(consommations)
        consommation_soiree = ConsommationService.retourner_consommation_soiree(consommations)
        consommation_journee_fusionnee = PanneauService.calculer_consommation_fusionnee(consommation_journee)

        pic = PanneauService.retourner_pic(consommation_journee_fusionnee)
        puissance_scolaire = PanneauService.calcul_puissance_scolaire(consommation_journee_fusionnee, energie_solaires)
        puissance_restante = PanneauService.calcul_puissance_restante(consommation_journee_fusionnee, energie_solaires)

        selected_prix_label = self.prix_config_combo.get().strip()
        if not selected_prix_label or selected_prix_label not in self.prix_configs_map:
            messagebox.showwarning("Analyse", "Veuillez selectionner une configuration de prix.")
            return

        selected_prix = self.prix_configs_map[selected_prix_label]

        try:
            energie_unitaire = float(self.energie_unitaire_entry.get().strip())
        except ValueError:
            messagebox.showerror(
                "Analyse",
                "Energie elementaire doit etre numerique.",
            )
            return

        # Les prix (ouvrable/weekend) viennent de la configuration selectionnee.
        prix_journalier_achat, prix_weekend_achat = prix_achat(
            consommation_restante=puissance_restante,
            energie_unitaire=energie_unitaire,
            prix_ouvrable=selected_prix.get_prixOuvrable(),
            prix_weekend=selected_prix.get_prixWeekend(),
        )

        augmentations = self.augmentation_repo.get_all()
        consommation_complete = list(consommation_journee_fusionnee) + list(consommation_soiree)
        sup_ouvrable, sup_weekend, details_augmentations = calcul_augmentation(
            consommation_complete,
            augmentations,
            energie_unitaire,
            selected_prix.get_prixOuvrable(),
            selected_prix.get_prixWeekend(),
        )

        total_ouvrable = prix_journalier_achat + sup_ouvrable
        total_weekend = prix_weekend_achat + sup_weekend

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
        self.prix_journalier_var.set(f"Prix achat (weekend): {prix_journalier_achat}")
        self.prix_weekend_var.set(f"Prix achat (ouvrable): {prix_weekend_achat}")
        self.augmentation_ouvrable_var.set(f"Supplement augmentation (weekend): {sup_ouvrable}")
        self.augmentation_weekend_var.set(f"Supplement augmentation (ouvrable): {sup_weekend}")
        self.prix_total_ouvrable_var.set(f"Total weekend: {total_ouvrable}")
        self.prix_total_weekend_var.set(f"Total ouvrable: {total_weekend}")

        if details_augmentations:
            self.augmentations_appliquees_var.set(
                "Augmentations appliquees: " + " | ".join(details_augmentations)
            )
        else:
            self.augmentations_appliquees_var.set("Augmentations appliquees: aucune")


if __name__ == "__main__":
    root = tk.Tk()
    ConsommationAnalyseView(root)
    root.mainloop()
