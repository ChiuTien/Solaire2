import tkinter as tk
from tkinter import ttk

from Views.AppareilViews import AppareilView
from Views.BatterieViews import BatterieView
from Views.ConsommationAnalyseView import ConsommationAnalyseView
from Views.ConsommationAppareil import ConsommationAppareilView
from Views.PanneauxViews import PanneauView
from Views.PrixViews import PrixView


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
	style.configure("Page.TFrame", background=colors["bg"])
	style.configure(
		"Hero.TFrame",
		background=colors["primary"],
		relief="solid",
		borderwidth=1,
		bordercolor=colors["primary"],
	)
	style.configure("HeroTitle.TLabel", background=colors["primary"], foreground="#ffffff", font="{Segoe UI} 18 bold")
	style.configure("HeroSub.TLabel", background=colors["primary"], foreground="#d1fae5", font="{Segoe UI} 10")
	style.configure(
		"Card.TFrame",
		background=colors["surface"],
		relief="solid",
		borderwidth=1,
		bordercolor=colors["border"],
		lightcolor=colors["border"],
		darkcolor=colors["border"],
	)
	style.configure("Section.TLabel", background=colors["surface"], foreground=colors["muted_text"], font="{Segoe UI} 10 bold")
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
	style.configure("Menu.TButton", font="{Segoe UI} 10 bold", padding=(16, 14))
	style.map(
		"Menu.TButton",
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
		self.master.geometry("760x460")
		self.master.minsize(700, 420)
		self.master.configure(bg="#f5f7fb")
		self.master.columnconfigure(0, weight=1)
		self.master.rowconfigure(0, weight=1)

		page = ttk.Frame(master, style="Page.TFrame", padding=22)
		page.grid(row=0, column=0, sticky="nsew")
		page.columnconfigure(0, weight=1)

		header = ttk.Frame(page, style="Hero.TFrame", padding=(20, 16))
		header.grid(row=0, column=0, sticky="ew")
		ttk.Label(header, text="Gestion Solaire", style="HeroTitle.TLabel").pack(anchor="w")
		ttk.Label(header, text="Selectionnez un module pour demarrer", style="HeroSub.TLabel").pack(anchor="w", pady=(3, 0))

		card = ttk.Frame(page, style="Card.TFrame", padding=16)
		card.grid(row=1, column=0, sticky="ew", pady=(14, 0))
		card.columnconfigure(0, weight=1)
		card.columnconfigure(1, weight=1)

		ttk.Label(card, text="Choisir une interface", style="Section.TLabel").grid(row=0, column=0, columnspan=2, sticky="w", padx=4, pady=(2, 10))

		actions = [
			("CRUD Appareil", self.open_appareil),
			("CRUD Batterie", self.open_batterie),
			("CRUD Panneau", self.open_panneau),
			("CRUD Consommation", self.open_consommation),
			("CRUD Prix", self.open_prix),
			("Analyse Consommation", self.open_analyse),
		]

		for idx, (label, action) in enumerate(actions):
			row = 1 + (idx // 2)
			col = idx % 2
			columnspan = 1

			btn = ttk.Button(card, text=label, command=action, style="Menu.TButton")
			btn.grid(row=row, column=col, columnspan=columnspan, sticky="ew", padx=6, pady=6)

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

	def open_prix(self):
		PrixView(self._open_window("CRUD Prix"))

	def open_analyse(self):
		ConsommationAnalyseView(self._open_window("Analyse Consommation"))


def run_interface():
	root = tk.Tk()
	apply_theme(root)
	MenuPrincipal(root)
	root.mainloop()


if __name__ == "__main__":
	run_interface()
