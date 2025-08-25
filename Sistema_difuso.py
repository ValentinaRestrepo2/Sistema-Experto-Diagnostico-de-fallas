import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


class SistemaDifuso:
    def __init__(self, root):
        self.root = root
        self.root.title("Diagnóstico Difuso de Velocidad de Internet")
        self.root.geometry("850x400")

        # Variables difusas
        self.velocidad = ctrl.Antecedent(np.arange(0, 101, 1), 'velocidad')
        self.latencia = ctrl.Antecedent(np.arange(0, 201, 1), 'latencia')
        self.perdida = ctrl.Antecedent(np.arange(0, 21, 1), 'perdida')
        self.diagnostico = ctrl.Consequent(np.arange(0, 101, 1), 'diagnostico')

        # Funciones de membresía
        self.velocidad['lenta'] = fuzz.trapmf(self.velocidad.universe, [0, 0, 10, 25])
        self.velocidad['normal'] = fuzz.trapmf(self.velocidad.universe, [15, 30, 60, 75])
        self.velocidad['rapida'] = fuzz.trapmf(self.velocidad.universe, [65, 85, 100, 100])

        self.latencia['baja'] = fuzz.trapmf(self.latencia.universe, [0, 0, 20, 60])
        self.latencia['media'] = fuzz.trapmf(self.latencia.universe, [40, 70, 110, 140])
        self.latencia['alta'] = fuzz.trapmf(self.latencia.universe, [120, 160, 200, 200])

        self.perdida['nula'] = fuzz.trapmf(self.perdida.universe, [0, 0, 0.5, 2])
        self.perdida['leve'] = fuzz.trapmf(self.perdida.universe, [1, 3, 7, 12])
        self.perdida['grave'] = fuzz.trapmf(self.perdida.universe, [10, 15, 20, 20])

        self.diagnostico['lento'] = fuzz.trapmf(self.diagnostico.universe, [0, 0, 20, 45])
        self.diagnostico['normal'] = fuzz.trapmf(self.diagnostico.universe, [35, 50, 60, 75])
        self.diagnostico['rapido'] = fuzz.trapmf(self.diagnostico.universe, [65, 80, 100, 100])

        # Reglas
        reglas = [
            ctrl.Rule(self.velocidad['lenta'] | self.latencia['alta'] | self.perdida['grave'], self.diagnostico['lento']),
            ctrl.Rule(self.velocidad['normal'] & self.latencia['media'] & self.perdida['leve'], self.diagnostico['normal']),
            ctrl.Rule(self.velocidad['rapida'] & self.latencia['baja'] & self.perdida['nula'], self.diagnostico['rapido']),
            ctrl.Rule(self.velocidad['rapida'] & self.perdida['leve'], self.diagnostico['normal']),
            ctrl.Rule(self.velocidad['normal'] & self.latencia['baja'] & self.perdida['nula'], self.diagnostico['normal'])
        ]

        self.sistema_ctrl = ctrl.ControlSystem(reglas)
        self.sistema = ctrl.ControlSystemSimulation(self.sistema_ctrl)

        # Interfaz
        frame_izq = tk.Frame(self.root)
        frame_izq.pack(side="left", padx=20, pady=20)

        frame_der = tk.Frame(self.root)
        frame_der.pack(side="right", padx=20, pady=20, fill="both", expand=True)

        # Entradas
        tk.Label(frame_izq, text="Velocidad (Mbps):").grid(row=0, column=0, sticky="w")
        self.entrada_velocidad = ttk.Entry(frame_izq)
        self.entrada_velocidad.grid(row=0, column=1)

        tk.Label(frame_izq, text="Latencia (ms):").grid(row=1, column=0, sticky="w")
        self.entrada_latencia = ttk.Entry(frame_izq)
        self.entrada_latencia.grid(row=1, column=1)

        tk.Label(frame_izq, text="Pérdida (%) :").grid(row=2, column=0, sticky="w")
        self.entrada_perdida = ttk.Entry(frame_izq)
        self.entrada_perdida.grid(row=2, column=1)

        # Botones
        ttk.Button(frame_izq, text="Diagnosticar", command=self.diagnosticar).grid(row=3, column=0, pady=10)
        ttk.Button(frame_izq, text="Limpiar", command=self.limpiar).grid(row=3, column=1, pady=10)

        # Área resultados
        tk.Label(frame_der, text="Reglas activadas y diagnóstico:").pack(anchor="w")
        self.text_area = tk.Text(frame_der, width=50, height=20)
        self.text_area.pack(fill="both", expand=True)

    def diagnosticar(self):
        try:
            vel = float(self.entrada_velocidad.get())
            lat = float(self.entrada_latencia.get())
            per = float(self.entrada_perdida.get())

            self.sistema.input['velocidad'] = vel
            self.sistema.input['latencia'] = lat
            self.sistema.input['perdida'] = per
            self.sistema.compute()

            resultado = self.sistema.output['diagnostico']
            if resultado < 40:
                texto = "Internet LENTO"
            elif resultado < 70:
                texto = "Internet NORMAL"
            else:
                texto = "Internet RÁPIDO"

            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, f"Entrada:\n")
            self.text_area.insert(tk.END, f"- Velocidad: {vel} Mbps\n")
            self.text_area.insert(tk.END, f"- Latencia: {lat} ms\n")
            self.text_area.insert(tk.END, f"- Pérdida: {per} %\n\n")
            self.text_area.insert(tk.END, f"Diagnóstico: {texto}\n")
            self.text_area.insert(tk.END, f"(Valor difuso: {resultado:.2f})\n")

            # Mostrar gráficas
            self.velocidad.view()
            self.latencia.view()
            self.perdida.view()
            self.diagnostico.view(sim=self.sistema)
            plt.show()

        except Exception as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")

    def limpiar(self):
        self.entrada_velocidad.delete(0, tk.END)
        self.entrada_latencia.delete(0, tk.END)
        self.entrada_perdida.delete(0, tk.END)
        self.text_area.delete("1.0", tk.END)
