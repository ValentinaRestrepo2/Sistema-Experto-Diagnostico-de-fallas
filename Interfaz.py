import tkinter as tk
from tkinter import ttk,messagebox
from Sistema_Experto import SistemaExpertoFallosPC

class Interfaz:
    def __init__ (self,root):
        self.root=root
        self.root.title("Sistema experto - Soporte Técnico")
        self.root.geometry("800x600")
        
        self.sistema=SistemaExpertoFallosPC()
        
        self.Ventana_principal()
        self.Ventana_hechos()
        self.Ventana_agenda()
        self.Crear_botones()
        
    def Ventana_principal(self):
        frame=ttk.LabelFrame(self.root,text="Principal")
        frame.pack(fill="x",padx=10,pady=5)
        
        self.problema=ttk.Entry(frame,width=60)
        self.problema.pack(side="left",padx=5,pady=5)
        
        btnAgregar=ttk.Button(frame,text="Agregar hecho",command=self.Crear_hecho)
        btnAgregar.pack(side="left",padx=5)
        
        btnEjecutar=ttk.Button(frame,text="Ejecutar",command=self.Ejecutar)
        btnEjecutar.pack(side="left",padx=5)
        
    def Ventana_hechos(self):
        frame=ttk.LabelFrame(self.root,text="Hechos")
        frame.pack(fill="both",expand=True,side="left",padx=10,pady=5)
        
        self.hechos=tk.Text(frame,height=20,width=40)
        self.hechos.pack(fill="both",expand=True)
        
    def Ventana_agenda(self):
        frame=ttk.LabelFrame(self.root,text="Agenda")
        frame.pack(fill="both",expand=True,side="right",padx=10,pady=5)
        
        self.agenda=tk.Text(frame,height=20,width=40)
        self.agenda.pack(fill="both",expand=True)
        
    def Crear_botones(self):
        frame=ttk.Frame(self.root)
        frame.pack(fill="x",padx=10,pady=5)
        
        BtnResetear=ttk.Button(frame,text="Resetear",command=self.Resetear)
        BtnResetear.pack(side="left",padx=5)
        
        BtnDiagnostio=ttk.Button(frame,text="Ver diagnostico",command=self.Mostrar_diagnostico)
        BtnDiagnostio.pack(side="left", padx=5)
    
    def Crear_hecho(self):
        hecho=self.problema.get().strip()
        if hecho:
            self.sistema.crear_hecho(hecho)
            self.actualizar_hecho()
            messagebox.showinfo("Hecho agregado", f"se agrego:{hecho}")
        else:
            messagebox.showwarning("Entrada vacía","Por favor ingresa un hecho")
    
    def Ejecutar(self):
        self.sistema.ejecutar()
        self.actualizar_hecho()
        self.actualizar_agenda()
        messagebox.showinfo("Ejecución","Ejecución de inferencia exitoso")
    
    def Resetear(self):
        self.sistema.resetear()
        self.hechos.delete("1.0",tk.END)
        self.agenda.delete("1.0",tk.END)
        messagebox.showinfo("Reset","Sistema experto reseteado")
    
    def Mostrar_diagnostico(self):
        diagnosticos=self.sistema.diagnostico()
        if diagnosticos:
            mensaje="\n".join(diagnosticos)
        else:
            mensaje="No se encontraron diagnosticoa asociados"
        messagebox.showinfo("Diagnosticos", mensaje)
    
    def actualizar_hecho(self):
        self.hechos.delete("1.0",tk.END)
        for hecho in self.sistema.mostrar_hechos():
            self.hechos.insert(tk.END,hecho+"\n")
    
    def actualizar_agenda(self):
        self.agenda.delete("1.0",tk.END)
        for agenda in self.sistema.mostrar_agenda():
            self.agenda.insert(tk.END, agenda+"\n")
        
if __name__ == "__main__":
    root=tk.Tk()
    app=Interfaz(root)
    root.mainloop()