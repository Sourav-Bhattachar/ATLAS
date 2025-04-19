import tkinter as tk
from tkinter import ttk, messagebox
import periodictable

# Element data: symbol, atomic number, group, period, color
elements = [
    ("H", 1, 1, 1, "lightgray"), ("He", 2, 18, 1, "lightblue"),
    ("Li", 3, 1, 2, "orange"), ("Be", 4, 2, 2, "orange"),
    ("B", 5, 13, 2, "#0d9cf2"), ("C", 6, 14, 2, "#0d9cf2"),
    ("N", 7, 15, 2, "#0d9cf2"), ("O", 8, 16, 2, "#0d9cf2"),
    ("F", 9, 17, 2, "#0d9cf2"), ("Ne", 10, 18, 2, "lightblue"),
    ("Na", 11, 1, 3, "orange"), ("Mg", 12, 2, 3, "orange"),
    ("Al", 13, 13, 3, "lightyellow"), ("Si", 14, 14, 3, "#0d9cf2"),
    ("P", 15, 15, 3, "#0d9cf2"), ("S", 16, 16, 3, "#0d9cf2"),
    ("Cl", 17, 17, 3, "#0d9cf2"), ("Ar", 18, 18, 3, "lightblue"),
    ("K", 19, 1, 4, "orange"), ("Ca", 20, 2, 4, "orange"),
    ("Sc", 21, 3, 4, "violet"), ("Ti", 22, 4, 4, "violet"), ("V", 23, 5, 4, "violet"),
    ("Cr", 24, 6, 4, "violet"), ("Mn", 25, 7, 4, "violet"), ("Fe", 26, 8, 4, "violet"),
    ("Co", 27, 9, 4, "violet"), ("Ni", 28, 10, 4, "violet"), ("Cu", 29, 11, 4, "violet"),
    ("Zn", 30, 12, 4, "violet"), ("Ga", 31, 13, 4, "lightyellow"), ("Ge", 32, 14, 4, "#0d9cf2"),
    ("As", 33, 15, 4, "#0d9cf2"), ("Se", 34, 16, 4, "#0d9cf2"),
    ("Br", 35, 17, 4, "#0d9cf2"), ("Kr", 36, 18, 4, "lightblue"),
    ("Rb", 37, 1, 5, "orange"), ("Sr", 38, 2, 5, "orange"),
    ("Y", 39, 3, 5, "violet"), ("Zr", 40, 4, 5, "violet"), ("Nb", 41, 5, 5, "violet"),
    ("Mo", 42, 6, 5, "violet"), ("Tc", 43, 7, 5, "violet"), ("Ru", 44, 8, 5, "violet"),
    ("Rh", 45, 9, 5, "violet"), ("Pd", 46, 10, 5, "violet"), ("Ag", 47, 11, 5, "violet"),
    ("Cd", 48, 12, 5, "violet"), ("In", 49, 13, 5, "lightyellow"), ("Sn", 50, 14, 5, "lightyellow"),
    ("Sb", 51, 15, 5, "#0d9cf2"), ("Te", 52, 16, 5, "#0d9cf2"),
    ("I", 53, 17, 5, "#0d9cf2"), ("Xe", 54, 18, 5, "lightblue"),
    ("Cs", 55, 1, 6, "orange"), ("Ba", 56, 2, 6, "orange"), ("La", 57, 3, 9, "pink"),
    ("Ce", 58, 4, 9, "pink"), ("Pr", 59, 5, 9, "pink"), ("Nd", 60, 6, 9, "pink"),
    ("Pm", 61, 7, 9, "pink"), ("Sm", 62, 8, 9, "pink"), ("Eu", 63, 9, 9, "pink"),
    ("Gd", 64, 10, 9, "pink"), ("Tb", 65, 11, 9, "pink"), ("Dy", 66, 12, 9, "pink"),
    ("Ho", 67, 13, 9, "pink"), ("Er", 68, 14, 9, "pink"), ("Tm", 69, 15, 9, "pink"),
    ("Yb", 70, 16, 9, "pink"), ("Lu", 71, 17, 9, "pink"),
    ("Hf", 72, 4, 6, "violet"), ("Ta", 73, 5, 6, "violet"), ("W", 74, 6, 6, "violet"),
    ("Re", 75, 7, 6, "violet"), ("Os", 76, 8, 6, "violet"), ("Ir", 77, 9, 6, "violet"),
    ("Pt", 78, 10, 6, "violet"), ("Au", 79, 11, 6, "violet"), ("Hg", 80, 12, 6, "violet"),
    ("Tl", 81, 13, 6, "lightyellow"), ("Pb", 82, 14, 6, "lightyellow"),
    ("Bi", 83, 15, 6, "#0d9cf2"), ("Po", 84, 16, 6, "#0d9cf2"),
    ("At", 85, 17, 6, "#0d9cf2"), ("Rn", 86, 18, 6, "lightblue"),
    ("Fr", 87, 1, 7, "orange"), ("Ra", 88, 2, 7, "orange"), ("Ac", 89, 3, 10, "lightpink"),
    ("Th", 90, 4, 10, "lightpink"), ("Pa", 91, 5, 10, "lightpink"), ("U", 92, 6, 10, "lightpink"),
    ("Np", 93, 7, 10, "lightpink"), ("Pu", 94, 8, 10, "lightpink"), ("Am", 95, 9, 10, "lightpink"),
    ("Cm", 96, 10, 10, "lightpink"), ("Bk", 97, 11, 10, "lightpink"), ("Cf", 98, 12, 10, "lightpink"),
    ("Es", 99, 13, 10, "lightpink"), ("Fm", 100, 14, 10, "lightpink"),
    ("Md", 101, 15, 10, "lightpink"), ("No", 102, 16, 10, "lightpink"), ("Lr", 103, 17, 10, "lightpink"),
    ("Rf", 104, 4, 7, "violet"), ("Db", 105, 5, 7, "violet"), ("Sg", 106, 6, 7, "violet"),
    ("Bh", 107, 7, 7, "violet"), ("Hs", 108, 8, 7, "violet"), ("Mt", 109, 9, 7, "violet"),
    ("Ds", 110, 10, 7, "violet"), ("Rg", 111, 11, 7, "violet"), ("Cn", 112, 12, 7, "violet"),
    ("Nh", 113, 13, 7, "lightyellow"), ("Fl", 114, 14, 7, "lightyellow"),
    ("Mc", 115, 15, 7, "#0d9cf2"), ("Lv", 116, 16, 7, "#0d9cf2"),
    ("Ts", 117, 17, 7, "#0d9cf2"), ("Og", 118, 18, 7, "lightblue"),
]

def show_element_info(symbol):
    try:
        element = getattr(periodictable, symbol.capitalize())
    except AttributeError:
        messagebox.showerror("Error", f"Element {symbol} not found!")
        return

    # Create or update info window
    if not hasattr(show_element_info, 'info_window') or not show_element_info.info_window.winfo_exists():
        show_element_info.info_window = tk.Toplevel()
        show_element_info.info_window.title("Element Information")
        show_element_info.info_window.geometry("320x300")
        
        main_frame = ttk.Frame(show_element_info.info_window, padding=20)
        main_frame.pack(fill='both', expand=True)
        
        # Symbol display
        symbol_label = ttk.Label(main_frame, font=('Arial', 48))
        symbol_label.pack(pady=10)
        show_element_info.symbol_label = symbol_label
        
        # Property labels
        properties = [
            "Name:", "Atomic Number:", "Atomic Mass:",
            "Density:", "Group:", "Period:", "Electron Configuration:"
        ]
        show_element_info.info_labels = []
        for prop in properties:
            label = ttk.Label(main_frame, text='', font=('Times New Roman', 12))
            label.pack(anchor='w', padx=20)
            show_element_info.info_labels.append(label)
    else:
        # Bring existing window to front
        show_element_info.info_window.lift()

    # Update labels with element data
    show_element_info.symbol_label.config(text=element.symbol)
    show_element_info.info_labels[0].config(text=f"Name: {element.name.capitalize()}")
    show_element_info.info_labels[1].config(text=f"Atomic Number: {element.number}")
    show_element_info.info_labels[2].config(text=f"Atomic Mass: {element.mass:.3f} amu")
    
    density = getattr(element, 'density', 'N/A')
    show_element_info.info_labels[3].config(text=f"Density: {density} g/cm³" if density else "Density: N/A")
   

periodic_table_window = None

def create_periodic_table(parent):
    global periodic_table_window
    if periodic_table_window is not None and periodic_table_window.winfo_exists():
        periodic_table_window.lift()  # Bring to front if already open
        return periodic_table_window
    
    periodic_table_window = tk.Toplevel(parent)
    periodic_table_window.title("Chemistry Periodic Table")
    periodic_table_window.configure(bg="#0cf397")
    
    for symbol, number, col, row, color in elements:
        btn = tk.Button(
            periodic_table_window,
            text=f"{symbol}\n{number}",
            width=6,
            height=3,
            bg=color,
            relief="ridge",
            bd=1,
            font=("Helvetica", 8, "bold"),
            command=lambda s=symbol: show_element_info(s)
        )
        btn.grid(row=row, column=col, padx=2, pady=2)
    
    return periodic_table_window
    
