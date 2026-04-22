import tkinter as tk
from tkinter import ttk


def apply_dark_theme(root):
	"""
	Applique un thème noir et blanc moderne à l'application tkinter.
	"""
	style = ttk.Style()

	# Couleurs du thème amélioré
	bg_dark = "#0d0d0d"  # Noir très foncé
	bg_medium = "#1a1a1a"  # Gris très foncé
	bg_light = "#2d2d2d"  # Gris foncé
	fg_white = "#ffffff"  # Blanc
	fg_light = "#e8e8e8"  # Gris clair
	accent_primary = "#00a8e8"  # Cyan/Bleu clair
	accent_hover = "#0088c0"  # Cyan foncé
	accent_active = "#006699"  # Bleu foncé
	accent_secondary = "#808080"  # Gris moyen

	# Configuration du thème global
	style.theme_use('clam')

	# Configure les couleurs de base
	root.configure(bg=bg_dark)

	# TFrame
	style.configure('TFrame', background=bg_dark, foreground=fg_white)
	style.configure('Header.TFrame', background=bg_medium, foreground=fg_white)
	style.configure('TLabelframe', background=bg_medium, foreground=fg_white, borderwidth=2)
	style.configure('TLabelframe.Label', background=bg_medium, foreground=accent_primary, font=('TkDefaultFont', 10, 'bold'))

	# TLabel
	style.configure('TLabel', background=bg_dark, foreground=fg_white)
	style.configure('Title.TLabel', background=bg_dark, foreground=accent_primary, font=('TkDefaultFont', 14, 'bold'))
	style.configure('Subtitle.TLabel', background=bg_dark, foreground=fg_light, font=('TkDefaultFont', 10))
	style.configure('Header.TLabel', background=bg_medium, foreground=accent_primary, font=('TkDefaultFont', 11, 'bold'))

	# TButton - Style principal
	style.configure('TButton',
					background=accent_primary,
					foreground='#000000',
					borderwidth=0,
					focuscolor='none',
					padding=8,
					font=('TkDefaultFont', 10, 'bold'))
	style.map('TButton',
			  background=[('active', accent_hover), ('pressed', accent_active)],
			  foreground=[('active', '#000000')])

	# TButton - Style secondaire
	style.configure('Secondary.TButton',
					background=bg_light,
					foreground=accent_primary,
					borderwidth=1,
					focuscolor='none',
					padding=8,
					font=('TkDefaultFont', 10))
	style.map('Secondary.TButton',
			  background=[('active', accent_secondary)],
			  foreground=[('active', fg_white)])

	# TEntry
	style.configure('TEntry',
					fieldbackground=bg_light,
					foreground=fg_white,
					borderwidth=2,
					relief='solid',
					padding=4)
	style.map('TEntry',
			  fieldbackground=[('focus', bg_medium)],
			  bordercolor=[('focus', accent_primary)])

	# TCombobox
	style.configure('TCombobox',
					fieldbackground=bg_light,
					foreground=fg_white,
					background=bg_light,
					borderwidth=2,
					padding=4)
	style.map('TCombobox',
			  fieldbackground=[('readonly', bg_light), ('focus', bg_medium)],
			  foreground=[('readonly', fg_white)])

	# Treeview
	style.configure('Treeview',
					background=bg_light,
					foreground=fg_white,
					fieldbackground=bg_light,
					borderwidth=1)
	style.configure('Treeview.Heading',
					background=accent_primary,
					foreground='#000000',
					borderwidth=1,
					font=('TkDefaultFont', 9, 'bold'))
	style.map('Treeview',
			  background=[('selected', accent_primary)],
			  foreground=[('selected', '#000000')])
	style.map('Treeview.Heading',
			  background=[('active', accent_hover)])

	# TScrollbar
	style.configure('TScrollbar',
					background=bg_light,
					troughcolor=bg_dark,
					borderwidth=1,
					arrowcolor=fg_white)

	# Panedwindow
	style.configure('TPanedwindow', background=bg_dark)
