import tkinter as tk
from tkinter import ttk

from Views.AppareilViews import AppareilView
from Views.BatterieViews import BatterieView
from Views.ConsommationAnalyseView import ConsommationAnalyseView
from Views.ConsommationAppareil import ConsommationAppareilView
from Views.PanneauxViews import PanneauView


class MenuPrincipal:
	def __init__(self, master):
		self.master = master
		self._setup_theme()
		self.master.title("Gestion Solaire - Menu")
		self.master.geometry("560x370")
		self.master.minsize(520, 340)

		container = ttk.Frame(master, style="App.TFrame")
		container.pack(fill="both", expand=True, padx=18, pady=18)

		header = ttk.Frame(container, style="App.TFrame")
		header.pack(fill="x", pady=(0, 12))

		ttk.Label(header, text="Gestion Solaire", style="Title.TLabel").pack(anchor="w")
		ttk.Label(
			header,
			text="Selectionne un module pour ouvrir une vue de gestion.",
			style="Subtitle.TLabel"
		).pack(anchor="w", pady=(2, 0))

		frame = ttk.LabelFrame(container, text="Choisir une interface", style="Card.TLabelframe")
		frame.pack(fill="both", expand=True)

		ttk.Button(frame, text="CRUD Appareil", command=self.open_appareil, style="Primary.TButton").pack(fill="x", padx=14, pady=(10, 8))
		ttk.Button(frame, text="CRUD Batterie", command=self.open_batterie, style="Primary.TButton").pack(fill="x", padx=14, pady=8)
		ttk.Button(frame, text="CRUD Panneau", command=self.open_panneau, style="Primary.TButton").pack(fill="x", padx=14, pady=8)
		ttk.Button(frame, text="CRUD Consommation", command=self.open_consommation, style="Primary.TButton").pack(fill="x", padx=14, pady=8)
		ttk.Button(frame, text="Analyse Consommation", command=self.open_analyse, style="Primary.TButton").pack(fill="x", padx=14, pady=(8, 12))

	def _setup_theme(self):
		palette = {
			"bg": "#F4F8F6",
			"surface": "#FFFFFF",
			"primary": "#1F7A5C",
			"primary_hover": "#2D8D6C",
			"primary_active": "#17654C",
			"text": "#16352B",
			"muted": "#5B726A",
			"border": "#D5E4DE",
		}

		self.master.configure(bg=palette["bg"])
		self.master.option_add("*Font", "Segoe UI 10")

		style = ttk.Style(self.master)
		style.theme_use("clam")

		style.configure("App.TFrame", background=palette["bg"])

		style.configure(
			"Title.TLabel",
			background=palette["bg"],
			foreground=palette["text"],
			font=("Segoe UI Semibold", 18),
		)
		style.configure(
			"Subtitle.TLabel",
			background=palette["bg"],
			foreground=palette["muted"],
			font=("Segoe UI", 10),
		)

		style.configure(
			"Card.TLabelframe",
			background=palette["surface"],
			bordercolor=palette["border"],
			borderwidth=1,
			relief="solid",
		)
		style.configure(
			"Card.TLabelframe.Label",
			background=palette["surface"],
			foreground=palette["text"],
			font=("Segoe UI Semibold", 11),
		)

		style.configure(
			"Primary.TButton",
			background=palette["primary"],
			foreground="#FFFFFF",
			borderwidth=0,
			focuscolor=palette["surface"],
			padding=(12, 8),
			font=("Segoe UI Semibold", 10),
		)
		style.map(
			"Primary.TButton",
			background=[
				("pressed", palette["primary_active"]),
				("active", palette["primary_hover"]),
			],
			foreground=[("disabled", "#DDE9E4")],
		)

	def _open_window(self, title):
		window = tk.Toplevel(self.master)
		window.title(title)
		window.configure(bg="#F4F8F6")
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
	MenuPrincipal(root)
	root.mainloop()


if __name__ == "__main__":
	run_interface()
