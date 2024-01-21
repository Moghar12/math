import tkinter as tk
from tkinter import ttk
from sympy import symbols, sympify
from scipy.integrate import quad, simps
import numpy as np
import matplotlib.pyplot as plt
from sympy import latex
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class IntegralCalculator(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()

        self.create_widgets()

    def create_widgets(self):
        self.create_input_widgets()
        self.create_method_selection()
        self.create_calculation_button()
        self.create_result_label()
        self.create_graph_button()

    def create_input_widgets(self):
        self.function_label = tk.Label(self, text="Fonction :")
        self.function_label.grid(row=0, column=0, padx=10, pady=5)
        self.function_entry = tk.Entry(self)
        self.function_entry.grid(row=0, column=1, padx=10, pady=5)

        self.bounds_label_a = tk.Label(self, text="Borne a :")
        self.bounds_label_a.grid(row=1, column=0, padx=10, pady=5)
        self.bounds_entry_a = tk.Entry(self)
        self.bounds_entry_a.grid(row=1, column=1, padx=10, pady=5)

        self.bounds_label_b = tk.Label(self, text="Borne b :")
        self.bounds_label_b.grid(row=2, column=0, padx=10, pady=5)
        self.bounds_entry_b = tk.Entry(self)
        self.bounds_entry_b.grid(row=2, column=1, padx=10, pady=5)

    def create_method_selection(self):
        self.method_label = tk.Label(self, text="Méthode :")
        self.method_label.grid(row=3, column=0, padx=10, pady=5)
        self.method_combobox = ttk.Combobox(self, values=["trapz", "simps", "quad"])
        self.method_combobox.grid(row=3, column=1, padx=10, pady=5)

    def create_calculation_button(self):
        self.calculate_button = tk.Button(self, text="Calculer", command=self.calculate_integration)
        self.calculate_button.grid(row=4, column=0, columnspan=2, pady=10)

    def create_result_label(self):
        self.result_label = tk.Label(self, text="Résultat :")
        self.result_label.grid(row=5, column=0, padx=10, pady=5)
        self.result_entry = tk.Entry(self, state="readonly")
        self.result_entry.grid(row=5, column=1, padx=10, pady=5)

    def create_graph_button(self):
        self.graph_button = tk.Button(self, text="Afficher le graphe", command=self.plot_graph)
        self.graph_button.grid(row=6, column=0, columnspan=2, pady=10)

    def calculate_integration(self):
        function_expr = self.function_entry.get()
        variable = symbols('x')
        lower_bound = float(self.bounds_entry_a.get())
        upper_bound = float(self.bounds_entry_b.get())
        method = self.method_combobox.get()

        try:
            function = sympify(function_expr)

            if method == "quad":
                result, _ = quad(lambda x: float(function.subs(variable, x)), lower_bound, upper_bound)
            elif method == "trapz":
                result = np.trapz([float(function.subs(variable, x)) for x in np.linspace(lower_bound, upper_bound, 1000)],
                                  dx=(upper_bound - lower_bound) / 1000)
            elif method == "simps":
                result = simps([float(function.subs(variable, x)) for x in np.linspace(lower_bound, upper_bound, 1000)],
                               dx=(upper_bound - lower_bound) / 1000)
            else:
                raise ValueError("Méthode non supportée")

            self.result_entry.config(state="normal")
            self.result_entry.delete(0, tk.END)
            self.result_entry.insert(0, f"{result}")
            self.result_entry.config(state="readonly")
        except Exception as e:
            self.result_entry.config(state="normal")
            self.result_entry.delete(0, tk.END)
            self.result_entry.insert(0, f"Erreur: {str(e)}")
            self.result_entry.config(state="readonly")

    def plot_graph(self):
        try:
            function_expr = self.function_entry.get()
            variable = symbols('x')
            lower_bound = float(self.bounds_entry_a.get())
            upper_bound = float(self.bounds_entry_b.get())
            method = self.method_combobox.get()

            function = sympify(function_expr)

            x_values = np.linspace(lower_bound, upper_bound, 1000)
            y_values = [float(function.subs(variable, x)) for x in x_values]

            plt.figure()
            plt.plot(x_values, y_values, label='Fonction à intégrer')
            plt.fill_between(x_values, y_values, alpha=0.2, label='Zone sous la courbe')

            plt.title(f'Graphe de l\'intégrale: ${latex(sympify(function))}$')
            plt.xlabel('x')
            plt.ylabel('y')
            plt.legend()

            canvas = FigureCanvasTkAgg(plt.gcf(), master=self)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.grid(row=7, column=0, columnspan=2, pady=10)

        except Exception as e:
            tk.messagebox.showerror("Erreur", f"Erreur: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Calcul d'Intégrale")  # Mettez à jour le titre ici
    app = IntegralCalculator(root)
    root.mainloop()
