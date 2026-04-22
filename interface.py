import tkinter as tk
from tkinter import ttk

from Views.AppareilViews import AppareilView
from Views.BatterieViews import BatterieView
from Views.ConsommationAnalyseView import ConsommationAnalyseView
from Views.ConsommationAppareil import ConsommationAppareilView
from Views.PanneauxViews import PanneauView


def apply_theme(root):
	style = ttk.Style(root)
	style.theme_use("clam")

	colors = {
		"bg": "#f5f7fb",
		"surface": "#ffffff",
		"primary": "#0f766e",
		"primary_hover": "#0b5f59",
		"text": "#0f172a",
		"muted_text": "#475569",
		"border": "#dbe3ef",
		"table_alt": "#f8fafc",
	}

	root.configure(bg=colors["bg"])

	style.configure("TFrame", background=colors["bg"])
	style.configure(
		"TLabelframe",
		background=colors["surface"],
		foreground=colors["text"],
		bordercolor=colors["border"],
		lightcolor=colors["border"],
		darkcolor=colors["border"],
		relief="solid",
		borderwidth=1,
		padding=10,
	)
	style.configure(
		"TLabelframe.Label",
		background=colors["surface"],
		foreground=colors["muted_text"],
		font="{Segoe UI} 10 bold",
	)

	style.configure(
		"TLabel",
		background=colors["surface"],
		foreground=colors["text"],
		font="{Segoe UI} 10",
	)

	style.configure(
		"TEntry",
		fieldbackground="#ffffff",
		foreground=colors["text"],
		bordercolor=colors["border"],
		insertcolor=colors["text"],
		padding=6,
	)
	style.map("TEntry", bordercolor=[("focus", colors["primary"])])

	style.configure(
		"TButton",
		background=colors["primary"],
		foreground="#ffffff",
		font="{Segoe UI} 10 bold",
		padding=(12, 8),
		borderwidth=0,
		relief="flat",
	)
	style.map(
		"TButton",
		background=[("active", colors["primary_hover"]), ("pressed", colors["primary_hover"])],
		foreground=[("disabled", "#e2e8f0")],
	)

	style.configure(
		"Treeview",
		background="#ffffff",
		fieldbackground="#ffffff",
		foreground=colors["text"],
		rowheight=28,
		bordercolor=colors["border"],
		lightcolor=colors["border"],
		darkcolor=colors["border"],
	)
	style.configure(
		"Treeview.Heading",
		background="#eef2f7",
		foreground=colors["muted_text"],
		font="{Segoe UI} 10 bold",
		relief="flat",
		padding=(8, 8),
	)
	style.map("Treeview", background=[("selected", "#d6f5ee")], foreground=[("selected", colors["text"])])
	style.map("Treeview.Heading", background=[("active", "#e2e8f0")])

	style.configure("Vertical.TScrollbar", gripcount=0, background="#e2e8f0", bordercolor=colors["border"], arrowsize=12)

	root.option_add("*Font", "{Segoe UI} 10")


class MenuPrincipal:
	def __init__(self, master):
		self.master = master
		self.master.title("Gestion Solaire - Menu")
		self.master.geometry("520x360")
		self.master.minsize(500, 340)
		self.master.configure(bg="#f5f7fb")

		header = ttk.Frame(master)
		header.pack(fill="x", padx=16, pady=(14, 6))
		ttk.Label(header, text="Gestion Solaire", font="{Segoe UI} 16 bold").pack(anchor="w")
		ttk.Label(header, text="Selectionnez un module pour commencer", font="{Segoe UI} 10").pack(anchor="w", pady=(2, 0))

		frame = ttk.LabelFrame(master, text="Choisir une interface")
		frame.pack(fill="both", expand=True, padx=16, pady=(8, 16))

		ttk.Button(frame, text="CRUD Appareil", command=self.open_appareil).pack(fill="x", padx=10, pady=7)
		ttk.Button(frame, text="CRUD Batterie", command=self.open_batterie).pack(fill="x", padx=10, pady=7)
		ttk.Button(frame, text="CRUD Panneau", command=self.open_panneau).pack(fill="x", padx=10, pady=7)
		ttk.Button(frame, text="CRUD Consommation", command=self.open_consommation).pack(fill="x", padx=10, pady=7)
		ttk.Button(frame, text="Analyse Consommation", command=self.open_analyse).pack(fill="x", padx=10, pady=7)

	def _open_window(self, title):
		window = tk.Toplevel(self.master)
		window.title(title)
		return window

	def open_appareil(self):
		AppareilView(self._open_window("CRUD Appareil"))

	def open_batterie(self):
		BatterieView(self._open_window("CRUD Batterie"))

	def open_panneau(self):
		PanneauView(self._open_window("CRUD Panneau"))

	def open_consommation(self):
		ConsommationAppareilView(self._open_window("CRUD Consommation"))

	def open_analyse(self):
		ConsommationAnalyseView(self._open_window("Analyse Consommation"))


def run_interface():
	root = tk.Tk()
	apply_theme(root)
	MenuPrincipal(root)
	root.mainloop()


if __name__ == "__main__":
	run_interface()
