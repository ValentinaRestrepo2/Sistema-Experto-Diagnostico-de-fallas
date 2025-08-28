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
        self.root.geometry("1000x600")
        self.frame_main = tk.Frame(self.root, bg="#F3F3F3")
        self.frame_main.pack(fill="both", expand=True)
        self.se = SistemaExperto()
        self.sd = SistemaDifuso()

        # Muestra por defecto el experto
        self.mostrarExperto()

    # ---------------- SISTEMA EXPERTO ----------------
    def mostrarExperto(self):
        self._limpiar_frame()
        #Encabezado
        encabezado = tk.Frame(self.frame_main, bg="#f2f2f2")
        encabezado.pack(side="top",fill="x", pady=5)
        tk.Label(encabezado, text="SISTEMA EXPERTO", font=("Luckiest Guy", 35), fg="#1155CC", bg="#f2f2f2").pack(side="left", padx=20)
        tk.Button(encabezado, text="Ir al sistema difuso", bg="#1366F2", fg="white",font=("Poppins", 12,"bold"),relief="raised",
          padx=12,pady=3,anchor="center", justify="center",command=self.mostrarDifuso).pack(side="right", padx=20)
        diagnostico_frame = tk.Frame(self.frame_main, bg="#f2f2f2")
        diagnostico_frame.pack(fill="x", padx=20)
        tk.Label(diagnostico_frame, text="🛜Diagnóstico del internet", font=("Poppins", 25, "bold"), bg="#f2f2f2").pack(side="left",padx=10)
        #Principal
        main_content_frame = tk.Frame(self.frame_main, bg="#f2f2f2")
        main_content_frame.pack(fill="both", padx=10, pady=5)

        frame_izq = tk.Frame(main_content_frame, bg="#f2f2f2", padx=20, pady=5)
        frame_izq.pack(side="left", fill="both")

        tk.Label(frame_izq, text="Ingrese su nombre", font=("Poppins", 10,"bold"), bg="#f2f2f2").pack(anchor="w", pady=(0, 2))
        self.nombre_entry = tk.Entry(frame_izq, font=("Poppins", 10), relief="raised")
        self.nombre_entry.pack(anchor="w", fill="x", pady=(0, 20))

        tk.Label(frame_izq, text="Seleccione los hechos que aplican:", font=("Poppins", 12, "bold"), bg="#f2f2f2").pack(anchor="w", pady=(0, 5))

        self.hechos_vars = {
            "noInternet": tk.BooleanVar(value=False),
            "energiaDesconectada": tk.BooleanVar(value=False),
            "ethernetDesconectado": tk.BooleanVar(value=False),
            "wifiCaido": tk.BooleanVar(value=False),
            "dnsError": tk.BooleanVar(value=False),
            "routerApagado": tk.BooleanVar(value=False),
            "lucesRojas": tk.BooleanVar(value=False),
        }

        # Checkboxes
        tk.Checkbutton(frame_izq, text="No hay internet", variable=self.hechos_vars["noInternet"],font=("Poppins", 9), bg="#f2f2f2").pack(anchor="w")
        tk.Checkbutton(frame_izq, text="Cable de energía del modem desconectado", variable=self.hechos_vars["energiaDesconectada"],font=("Poppins", 9), bg="#f2f2f2").pack(anchor="w")
        tk.Checkbutton(frame_izq, text="El router está apagado", variable=self.hechos_vars["routerApagado"],font=("Poppins", 9), bg="#f2f2f2").pack(anchor="w")
        tk.Checkbutton(frame_izq, text="Las luces del router están rojas", variable=self.hechos_vars["lucesRojas"],font=("Poppins", 9), bg="#f2f2f2").pack(anchor="w")
        tk.Checkbutton(frame_izq, text="Cable Ethernet desconectado", variable=self.hechos_vars["ethernetDesconectado"],font=("Poppins", 9), bg="#f2f2f2").pack(anchor="w")
        tk.Checkbutton(frame_izq, text="El WiFi está caído", variable=self.hechos_vars["wifiCaido"],font=("Poppins", 9), bg="#f2f2f2").pack(anchor="w")
        tk.Checkbutton(frame_izq, text="Error de DNS", variable=self.hechos_vars["dnsError"],font=("Poppins", 9), bg="#f2f2f2").pack(anchor="w")
     
        btns = tk.Frame(frame_izq, bg="#f2f2f2")
        btns.pack(pady=20)
        tk.Button(btns, text="Diagnosticar", bg="#03BA4B", fg="white", font=("Poppins", 12,"bold"),relief="groove",
          padx=20,pady=3,anchor="center", justify="center", command=self._diagnosticar_internet).pack(side="left", padx=10)
        tk.Button(btns, text="Limpiar", bg="#FF3548", fg="white", font=("Poppins", 12,"bold"),relief="groove",
          padx=20,pady=3,anchor="center", justify="center",command=self._limpiar_internet).pack(side="left", padx=10)

        frame_der = tk.Frame(main_content_frame, bg="#f2f2f2")
        frame_der.pack(side="right", fill="none", expand=True)
        
        resultados_frame = tk.Frame(frame_der, bg="white", highlightbackground="gray", highlightthickness=1)
        resultados_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        tk.Label(resultados_frame, text="Resultados:", font=("Poppins", 12, "bold"), bg="white").pack(anchor="w", padx=10, pady=(5, 5))
        self.salida_internet = tk.Text(resultados_frame, font=("Poppins", 10), bg="white", relief="flat", height=10)
        self.salida_internet.pack(fill="both", expand=True, padx=10, pady=5)
        
        recomendaciones_frame = tk.Frame(frame_der, bg="white", highlightbackground="gray", highlightthickness=1)
        recomendaciones_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        tk.Label(recomendaciones_frame, text="✨ Recomendaciones:", font=("Poppins", 12, "bold"), bg="white").pack(anchor="w", padx=10, pady=(5, 5))
        self.salida_recomendaciones = tk.Text(recomendaciones_frame, font=("Poppins", 10), bg="white", relief="flat", height=10)
        self.salida_recomendaciones.pack(fill="both", expand=True, padx=10, pady=5)

    def _diagnosticar_internet(self):
        self.salida_internet.delete("1.0", tk.END)
        nombre_usuario = self.nombre_entry.get()
        hechos_seleccionados = []
        for nombre_hecho, var in self.hechos_vars.items():
            if var.get():
                hechos_seleccionados.append(nombre_hecho)
        
        if not hechos_seleccionados:
            self.salida_internet.insert(tk.END, "Por favor seleccione al menos un hecho para diagnosticar.\n")
            return
        
        resultado = self.se.diagnosticar_internet(hechos_seleccionados)
        
        self.salida_internet.insert(tk.END, "Hechos:\n")
        for hecho in resultado['hechos']:
            self.salida_internet.insert(tk.END, f"- {hecho}\n")
        
        self.salida_internet.insert(tk.END, "\n")
        
        self.salida_internet.insert(tk.END, "Reglas activadas:\n")
        if resultado['reglas_activadas']:
            for regla in resultado['reglas_activadas']:
                self.salida_internet.insert(tk.END, f"- {regla}\n")
        else:
            self.salida_internet.insert(tk.END, "- No se activaron reglas\n")
        
        self.salida_internet.insert(tk.END, "\n")
        self.salida_recomendaciones.insert(tk.END, f"{nombre_usuario} debes: \n")
        if resultado['recomendaciones']:
            #self.salida_recomendaciones.insert(tk.END, "Recomendaciones:\n")
            for recomendacion in resultado['recomendaciones']:
                self.salida_recomendaciones.insert(tk.END, f"- {recomendacion}\n")
        else:
            self.salida_recomendaciones.insert(tk.END, "No se generaron recomendaciones.\n")

    def _limpiar_internet(self):
        for var in self.hechos_vars.values():
            var.set(False)
        self.salida_internet.delete("1.0", tk.END)
        self.salida_recomendaciones.delete("1.0", tk.END)
        self.nombre_entry.delete(0, tk.END)

    # ---------------- SISTEMA DIFUSO ----------------
    def mostrarDifuso(self):
        self._limpiar_frame()
        
        encabezado = tk.Frame(self.frame_main, bg="#f2f2f2")
        encabezado.pack(fill="x", pady=6)
        tk.Label(encabezado, text="SISTEMA DIFUSO", font=("Luckiest Guy", 35), fg="#1155CC", bg="#f2f2f2").pack(side="left", padx=20)
        tk.Button(encabezado, text="Ir al sistema experto", bg="#1366F2", fg="white",font=("Poppins", 12,"bold"),relief="raised",
          padx=12,pady=3,anchor="center", justify="center",command=self.mostrarExperto).pack(side="right", padx=20)
        diagnostico_frame = tk.Frame(self.frame_main, bg="#f2f2f2")
        diagnostico_frame.pack(fill="x", padx=20)
        tk.Label(diagnostico_frame, text="🛜Diagnóstico velocidad del internet", font=("Poppins", 25, "bold"), bg="#f2f2f2").pack(side="left",padx=10)
       
        input_frame = tk.Frame(self.frame_main, bg="#f2f2f2")
        input_frame.pack(fill="x", pady=2)
        
        # Frame anidado para colocar las etiquetas y entradas en una sola fila usando grid
        fields_frame = tk.Frame(input_frame, bg="#f2f2f2")
        fields_frame.pack(expand=True)
        
        tk.Label(fields_frame, text="Ingrese su nombre", font=("Poppins", 10,"bold"), bg="#f2f2f2").grid(row=0, column=0, padx=10, pady=2)
        self.nombre_entry = tk.Entry(fields_frame, font=("Poppins", 10), relief="raised")
        self.nombre_entry.grid(row=1, column=0, padx=10, pady=5)
        
        tk.Label(fields_frame, text="Velocidad (Mbps):", font=("Poppins", 10,"bold"), bg="#f2f2f2").grid(row=0, column=1, padx=10, pady=2)
        self.e_vel = tk.Entry(fields_frame, font=("Poppins", 10), relief="raised")
        self.e_vel.grid(row=1, column=1, padx=10, pady=2)
        
        tk.Label(fields_frame, text="Latencia (ms):", font=("Poppins", 10,"bold"), bg="#f2f2f2").grid(row=0, column=2, padx=10, pady=2)
        self.e_lat = tk.Entry(fields_frame, font=("Poppins", 10), relief="raised")
        self.e_lat.grid(row=1, column=2, padx=10, pady=2)
        
        tk.Label(fields_frame, text="Pérdida (%) :", font=("Poppins", 10,"bold"), bg="#f2f2f2").grid(row=0, column=3, padx=10, pady=2)
        self.e_per = tk.Entry(fields_frame, font=("Poppins", 10), relief="raised")
        self.e_per.grid(row=1, column=3, padx=10, pady=2)
        
        tk.Button(fields_frame, text="Diagnosticar", bg="#03BA4B", fg="white", font=("Poppins", 12,"bold"),
                  command=self._diagnosticar_difuso).grid(row=1, column=4, padx=8,pady=5, sticky="ew")
        tk.Button(fields_frame, text="Limpiar", bg="#FF3548", fg="white", font=("Poppins", 12,"bold"),
                  command=self._limpiar_difuso).grid(row=1, column=5, padx=8,pady=5, sticky="ew")

        
        frame_izq = tk.Frame(self.frame_main)
        frame_izq.pack(side="left", fill="y",padx=10, pady=5)
       
        resultados_frame = tk.Frame(frame_izq, bg="white", highlightbackground="gray", highlightthickness=1)
        resultados_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        tk.Label(resultados_frame, text="Calculo:", font=("Poppins", 12, "bold"), bg="white").pack(anchor="w", padx=10, pady=(5, 5))
        self.text_area = tk.Text(resultados_frame, font=("Poppins", 10), bg="white", relief="flat", height=5, width=30)
        self.text_area.pack(fill="both", expand=True, padx=10, pady=5)
        
        finaldiagnostico_frame = tk.Frame(frame_izq, bg="white", highlightbackground="gray", highlightthickness=1)
        finaldiagnostico_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        tk.Label(finaldiagnostico_frame, text="✨ Diagnostico:", font=("Poppins", 12, "bold"), bg="white").pack(anchor="w", padx=10, pady=(5, 5))
        self.salida_diagnostico = tk.Text(finaldiagnostico_frame, font=("Poppins", 14 , "bold"), fg="#1366F2",bg="white", relief="flat", height=8,width=30)
        self.salida_diagnostico.pack(fill="both", expand=True, padx=10, pady=5)
        
        frame_der = tk.Frame(self.frame_main)
        frame_der.pack(side="right", padx=10, pady=10, fill="both", expand=True)

        self.fig, self.axs = plt.subplots(2, 2, figsize=(8, 6), constrained_layout=True)
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_der)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def _diagnosticar_difuso(self):
        try:
            vel = float(self.e_vel.get())
            lat = float(self.e_lat.get())
            per = float(self.e_per.get())
            nombre = self.nombre_entry.get()

            detalle = self.sd.diagnosticar(vel, lat, per)

            self.text_area.insert(tk.END, f"-- Entradas → Vel={vel} Mbps,  Lat={lat} ms,  Perd={per} %\n")
            self.text_area.insert(tk.END, "Membership:\n", "bold")
            for var, subconjs in detalle["grados"].items():
                self.text_area.insert(tk.END, f"--  {var.capitalize()}: " +
                                  ", ".join([f"{s}={v:.2f}" for s,v in subconjs.items()]) + "\n")

            self.salida_diagnostico.insert(tk.END, f"{nombre} tienes {detalle['texto']} \ncon valor difuso → ({detalle['valor']:.2f})\n")

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
                           facecolor="#B6D7A8", alpha=0.4)
            self.axs[1,1].legend()
            self.canvas.draw_idle()

        except Exception as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")
        
    def _limpiar_difuso(self):
        self.e_vel.delete(0, tk.END)
        self.e_lat.delete(0, tk.END)
        self.e_per.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.text_area.delete("1.0", tk.END)
        self.salida_diagnostico.delete("1.0", tk.END)
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