import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Sistema_Experto import SistemaExperto
from Sistema_difuso import SistemaDifuso


class SistemaInterfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Experto y Difuso - Clase IA")
        self.root.geometry("1000x700")
        self.frame_main = tk.Frame(self.root, bg="#f2f2f2")
        self.frame_main.pack(fill="both", expand=True)
        self.se = SistemaExperto()
        self.sd = SistemaDifuso()

        # Muestra por defecto el experto
        self.mostrarExperto()

    # ---------------- SISTEMA EXPERTO ----------------
    def mostrarExperto(self):
        self._limpiar_frame()

        encabezado = tk.Frame(self.frame_main, bg="#f2f2f2")
        encabezado.pack(fill="x", pady=6)
        tk.Label(encabezado, text="Sistema Experto - Diagnóstico Internet", font=("Arial", 20, "bold"), bg="#f2f2f2").pack(side="left", padx=10)
        tk.Button(encabezado, text="Ir a Sistema Difuso ➡️", bg="#101E63", fg="white",
                  font=("Arial", 12),
                  command=self.mostrarDifuso).pack(side="right", padx=12)

        # Frame principal para checkboxes y resultados
        main_frame = tk.Frame(self.frame_main, bg="#f2f2f2")
        main_frame.pack(fill="both", expand=True, padx=18, pady=10)

        # Frame izquierdo para checkboxes
        frame_izq = tk.Frame(main_frame, bg="#f2f2f2")
        frame_izq.pack(side="left", fill="both", expand=True, padx=10)

        tk.Label(frame_izq, text="Seleccione los hechos:", font=("Arial", 12, "bold"), bg="#f2f2f2").pack(anchor="w", pady=(0, 10))

        # Variables de selección múltiple
        self.hechos_vars = {
            "noInternet": tk.BooleanVar(value=False),
            "energiaDesconectada": tk.BooleanVar(value=False),
            "ethernetDesconectado": tk.BooleanVar(value=False),
            "wifiCaido": tk.BooleanVar(value=False),
            "dnsError": tk.BooleanVar(value=False),
            "routerApagado": tk.BooleanVar(value=False),
            "lucesRojas": tk.BooleanVar(value=False),
        }

        ttk.Checkbutton(frame_izq, text="No hay internet", variable=self.hechos_vars["noInternet"]).pack(anchor="w", pady=2)
        ttk.Checkbutton(frame_izq, text="Cable de energía del modem desconectado", variable=self.hechos_vars["energiaDesconectada"]).pack(anchor="w", pady=2)
        ttk.Checkbutton(frame_izq, text="El router está apagado", variable=self.hechos_vars["routerApagado"]).pack(anchor="w", pady=2)
        ttk.Checkbutton(frame_izq, text="Las luces del router están rojas", variable=self.hechos_vars["lucesRojas"]).pack(anchor="w", pady=2)
        ttk.Checkbutton(frame_izq, text="Cable Ethernet desconectado", variable=self.hechos_vars["ethernetDesconectado"]).pack(anchor="w", pady=2)
        ttk.Checkbutton(frame_izq, text="El WiFi está caído", variable=self.hechos_vars["wifiCaido"]).pack(anchor="w", pady=2)
        ttk.Checkbutton(frame_izq, text="Error de DNS", variable=self.hechos_vars["dnsError"]).pack(anchor="w", pady=2)

        # Botones
        btns = tk.Frame(frame_izq, bg="#f2f2f2")
        btns.pack(pady=10)
        tk.Button(btns, text="Diagnosticar", bg="#4361F0", fg="white", font=("Arial", 12), 
                  command=self._diagnosticar_internet).pack(side="left", padx=5)
        tk.Button(btns, text="Limpiar", bg="#d9534f", fg="white", font=("Arial", 12), 
                  command=self._limpiar_internet).pack(side="left", padx=5)

        # Frame derecho para resultados
        frame_der = tk.Frame(main_frame, bg="#f2f2f2")
        frame_der.pack(side="right", fill="both", expand=True, padx=10)

        tk.Label(frame_der, text="Resultados del diagnóstico:", font=("Arial", 12, "bold"), bg="#f2f2f2").pack(anchor="w", pady=(0, 5))
        self.salida_internet = tk.Text(frame_der, width=60, height=25, font=("Consolas", 10), bg="white")
        self.salida_internet.pack(fill="both", expand=True)

    def _diagnosticar_internet(self):
        """Ejecuta el diagnóstico de internet"""
        self.salida_internet.delete("1.0", tk.END)
        
        # Obtener hechos seleccionados
        hechos_seleccionados = []
        for nombre_hecho, var in self.hechos_vars.items():
            if var.get():
                hechos_seleccionados.append(nombre_hecho)
        
        if not hechos_seleccionados:
            self.salida_internet.insert(tk.END, "Por favor seleccione al menos un hecho para diagnosticar.\n")
            return
        
        # Ejecutar diagnóstico
        resultado = self.se.diagnosticar_internet(hechos_seleccionados)
        
        # Mostrar hechos
        self.salida_internet.insert(tk.END, "Hechos:\n")
        for hecho in resultado['hechos']:
            self.salida_internet.insert(tk.END, f"- {hecho}\n")
        
        self.salida_internet.insert(tk.END, "\n")
        
        # Mostrar reglas activadas
        self.salida_internet.insert(tk.END, "Reglas activadas:\n")
        if resultado['reglas_activadas']:
            for regla in resultado['reglas_activadas']:
                self.salida_internet.insert(tk.END, f"- {regla}\n")
        else:
            self.salida_internet.insert(tk.END, "- No se activaron reglas\n")
        
        self.salida_internet.insert(tk.END, "\n")
        
        # Mostrar recomendaciones
        if resultado['recomendaciones']:
            self.salida_internet.insert(tk.END, "Recomendaciones:\n")
            for recomendacion in resultado['recomendaciones']:
                self.salida_internet.insert(tk.END, f"- {recomendacion}\n")
        else:
            self.salida_internet.insert(tk.END, "No se generaron recomendaciones.\n")

    def _limpiar_internet(self):
        """Limpia la interfaz del sistema experto de internet"""
        for var in self.hechos_vars.values():
            var.set(False)
        self.salida_internet.delete("1.0", tk.END)

    # ---------------- SISTEMA DIFUSO ----------------
    def mostrarDifuso(self):
        self._limpiar_frame()
        
        encabezado = tk.Frame(self.frame_main, bg="#f2f2f2")
        encabezado.pack(fill="x", pady=6)
        tk.Label(encabezado, text="Sistema Difuso", font=("Arial", 20, "bold"), bg="#f2f2f2").pack(side="left", padx=10)
        tk.Button(encabezado, text="Ir a Sistema Experto ➡️", bg="#101E63", fg="white",
                  font=("Arial", 12), command=self.mostrarExperto).pack(side="right", padx=10)

        frame_izq = tk.Frame(self.frame_main)
        frame_izq.pack(side="left", padx=20, pady=20)

        tk.Label(frame_izq, text="Velocidad (Mbps):").grid(row=0, column=0, sticky="w")
        self.e_vel = ttk.Entry(frame_izq)
        self.e_vel.grid(row=0, column=1)

        tk.Label(frame_izq, text="Latencia (ms):").grid(row=1, column=0, sticky="w")
        self.e_lat = ttk.Entry(frame_izq)
        self.e_lat.grid(row=1, column=1)

        tk.Label(frame_izq, text="Pérdida (%) :").grid(row=2, column=0, sticky="w")
        self.e_per = ttk.Entry(frame_izq)
        self.e_per.grid(row=2, column=1)

        tk.Button(frame_izq, text="Diagnosticar", bg="#4361F0", fg="white",font=("Arial", 12),command=self._diagnosticar_difuso).grid(row=3, column=0, pady=10)
        tk.Button(frame_izq, text="🔄 Limpiar",bg="#d9534f", fg="white",font=("Arial", 12), command=self._limpiar_difuso).grid(row=3, column=1, pady=10)

        frame_der = tk.Frame(self.frame_main)
        frame_der.pack(side="right", padx=20, pady=20, fill="both", expand=True)

        tk.Label(frame_der, text="Calculo:").pack(anchor="w")
        self.text_area = tk.Text(frame_der, width=60, height=15)
        self.text_area.pack(fill="both", expand=True)

        self.fig, self.axs = plt.subplots(2, 2, figsize=(8, 6), constrained_layout=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_der)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def _diagnosticar_difuso(self):
        try:
            vel = float(self.e_vel.get())
            lat = float(self.e_lat.get())
            per = float(self.e_per.get())

            detalle = self.sd.diagnosticar(vel, lat, per)

            self.text_area.insert(tk.END, "--- DIAGNÓSTICO ---\n")
            self.text_area.insert(tk.END, f"Entradas → Vel={vel} Mbps, Lat={lat} ms, Perd={per} %\n")
            self.text_area.insert(tk.END, "-----------------------------\n")
            self.text_area.insert(tk.END, "Membership:\n")
            for var, subconjs in detalle["grados"].items():
                self.text_area.insert(tk.END, f"  {var.capitalize()}: " +
                                  ", ".join([f"{s}={v:.2f}" for s,v in subconjs.items()]) + "\n")

           # self.text_area.insert(tk.END, "Reglas activadas:\n")
            #for regla, valor in detalle["reglas"].items():
             #   self.text_area.insert(tk.END, f"  {regla}: {valor:.2f}\n")
            self.text_area.insert(tk.END, "-----------------------------\n")
          
            self.text_area.insert(tk.END, f"Diagnóstico final → {detalle['texto']} Valor difuso → ({detalle['valor']:.2f})\n")
            self.text_area.insert(tk.END, "-----------------------------\n")

            for ax in self.axs.ravel():
                ax.cla()

            self.axs[0,0].plot(self.sd.velocidad.universe, self.sd.velocidad['lenta'].mf, 'b', linewidth=2, label="Lenta")
            self.axs[0,0].plot(self.sd.velocidad.universe, self.sd.velocidad['normal'].mf, 'g', linewidth=2, label="Normal")
            self.axs[0,0].plot(self.sd.velocidad.universe, self.sd.velocidad['rapida'].mf, 'r', linewidth=2, label="Rápida")
            self.axs[0,0].set_title("Velocidad")
            self.axs[0,0].set_xlabel("Mbps")
            self.axs[0,0].set_ylabel("Membership")
            self.axs[0,0].legend()

            self.axs[0,1].plot(self.sd.latencia.universe, self.sd.latencia['baja'].mf,'b', linewidth=2, label="Baja")
            self.axs[0,1].plot(self.sd.latencia.universe, self.sd.latencia['media'].mf, 'g', linewidth=2, label="Media")
            self.axs[0,1].plot(self.sd.latencia.universe, self.sd.latencia['alta'].mf, 'r', linewidth=2, label="Alta")
            self.axs[0,1].set_title("Latencia")
            self.axs[0,1].set_xlabel("ms")
            self.axs[0,1].set_ylabel("Membership")
            self.axs[0,1].legend()

            self.axs[1,0].plot(self.sd.perdida.universe, self.sd.perdida['nula'].mf,'b', linewidth=2, label="Nula")
            self.axs[1,0].plot(self.sd.perdida.universe, self.sd.perdida['leve'].mf, 'g', linewidth=2, label="Leve")
            self.axs[1,0].plot(self.sd.perdida.universe, self.sd.perdida['grave'].mf, 'r', linewidth=2, label="Grave")
            self.axs[1,0].set_title("Pérdida")
            self.axs[1,0].set_xlabel("%")
            self.axs[1,0].set_ylabel("Membership")
            self.axs[1,0].legend()

            self.axs[1,1].plot(self.sd.diagnostico.universe, self.sd.diagnostico['lento'].mf, 'b', linewidth=2, label="Lento")
            self.axs[1,1].plot(self.sd.diagnostico.universe, self.sd.diagnostico['normal'].mf, 'g', linewidth=2, label="Normal")
            self.axs[1,1].plot(self.sd.diagnostico.universe, self.sd.diagnostico['rapido'].mf, 'r', linewidth=2, label="Rápido")
            self.axs[1,1].axvline(detalle["valor"], color="k", linestyle="--")
            self.axs[1,1].set_title("Diagnóstico")
            x = self.sd.diagnostico.universe
            lento_mf = np.fmin(self.sd.diagnostico['lento'].mf,
                   fuzz.interp_membership(x, self.sd.diagnostico['lento'].mf, detalle["valor"]))
            normal_mf = np.fmin(self.sd.diagnostico['normal'].mf,
                    fuzz.interp_membership(x, self.sd.diagnostico['normal'].mf, detalle["valor"]))
            rapido_mf = np.fmin(self.sd.diagnostico['rapido'].mf,
                    fuzz.interp_membership(x, self.sd.diagnostico['rapido'].mf, detalle["valor"]))
            agregado = np.fmax(lento_mf, np
            .fmax(normal_mf, rapido_mf))

            self.axs[1,1].fill_between(x, np.zeros_like(x), agregado,
                           facecolor="orange", alpha=0.4)
            self.axs[1,1].legend()
            self.canvas.draw_idle()

        except Exception as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")
        
    def _limpiar_difuso(self):
        self.e_vel.delete(0, tk.END)
        self.e_lat.delete(0, tk.END)
        self.e_per.delete(0, tk.END)
        self.text_area.delete("1.0", tk.END)
        for ax in self.fig.axes:
            ax.cla()
        self.canvas.draw()
        

    def _limpiar_frame(self):
        for widget in self.frame_main.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaInterfaz(root)
    root.mainloop()
