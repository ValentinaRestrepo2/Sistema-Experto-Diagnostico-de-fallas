import tkinter as tk
from Sistema_Experto import SistemaExperto


class SistemaInterfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Experto - Politécnico JIC")
        self.root.geometry("920x600")

        self.se = SistemaExperto()

        # Encabezado interfaz
        EncabezadoInterfaz = tk.Frame(self.root, bg="#f2f2f2")
        EncabezadoInterfaz.pack(fill="x", pady=6)
        tk.Label(EncabezadoInterfaz, text="Sistema experto", font=("Arial", 20, "bold"),
                 bg="#f2f2f2").pack(side="left", padx=10)
        tk.Button(EncabezadoInterfaz, text="Sistema difuso", font=("Arial", 12),
                  command=self.abrirSistemaDifuso).pack(side="right", padx=12)

        #Input de hecho
        input_hecho = tk.Frame(self.root, bg="#f2f2f2")
        input_hecho.pack(pady=8)
        tk.Label(input_hecho, text="Ingrese un hecho:", font=("Arial", 12),
                 bg="#f2f2f2").pack()
        self.eHecho = tk.Entry(input_hecho, width=70, font=("Arial", 12))
        self.eHecho.pack(pady=4)
        self.eHecho.bind("<Return>", self._on_enter) # se agrega al presionar Enter

        # Salidas
        panel = tk.Frame(self.root, bg="#f2f2f2")
        panel.pack(fill="both", expand=True, padx=18, pady=10)

        # Panel de hechos
        panelhecho = tk.Frame(panel, bg="#f2f2f2")
        panelhecho.pack(side="left", fill="both", expand=True, padx=10)
        tk.Label(panelhecho, text="Hechos", font=("Arial", 12, "bold"),
                 bg="#f2f2f2").pack(anchor="w")
        self.txt_hechos = tk.Text(panelhecho, height=22, width=52, font=("Consolas", 10), bg="white")
        self.txt_hechos.pack(fill="both", expand=True, pady=5)

        # Panel de agenda
        panelagenda = tk.Frame(panel, bg="#f2f2f2")
        panelagenda.pack(side="right", fill="both", expand=True, padx=10)
        tk.Label(panelagenda, text="Agenda", font=("Arial", 12, "bold"),
                 bg="#f2f2f2").pack(anchor="w")
        self.txt_agenda = tk.Text(panelagenda, height=22, width=52, font=("Consolas", 10), bg="white")
        self.txt_agenda.pack(fill="both", expand=True, pady=5)

        # Reeestablecer sistema
        tk.Button(self.root, text="🔄 Reestablecer sistema", bg="#d9534f", fg="white",
                  font=("Arial", 12), command=self._resetear).pack(pady=8)

        self._refrescar()

    def _on_enter(self, _event=None):
        hecho = self.eHecho.get().strip()
        if hecho:
            self.se.agregarHecho(hecho)
            self.eHecho.delete(0, tk.END)
            self._refrescar()

    def _refrescar(self):
        self.txt_hechos.delete("1.0", tk.END)
        self.txt_hechos.insert(tk.END, "\n".join(self.se.verHechos()))
        self.txt_agenda.delete("1.0", tk.END)
        agenda = self.se.verAgenda()
        if agenda:
            self.txt_agenda.insert(tk.END, "\n".join(agenda))
        else:
            self.txt_agenda.insert(tk.END, "(Sin activaciones)")

    def _resetear(self):
        self.se.reestablecer()
        self._refrescar()

    def abrirSistemaDifuso(self):
        top = tk.Toplevel(self.root)
        top.title("Sistema difuso")
        tk.Label(top, text="Aquí irá la interfaz de lógica difusa.",
                 font=("Arial", 14)).pack(pady=40)


if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaInterfaz(root)
    root.mainloop()
