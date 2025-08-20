import clips
import tkinter as tk

#Sistema experto para el diagnostico de fallas en el PC

class SistemaExpertoFallosPC:
    def __init__(self):
        self.env=clips.Environment()
        self.env.clear()
        self.cargar_reglas()

    def cargar_reglas(self):
        
        reglas=[
            """
            (defrule fallo-pantalla-azul
                (problema pantalla-azul)
            =>
                (assert (diagnostico "Error crítico del sistema operativo")))
            """,
            """
            (defrule fallo-no-enciende
                (problema no-enciende)
            =>
                (assert (diagnostico "Revisar fuente de poder o batería")))
            """,
            """
            (defrule fallo-lento
                (problema muy-lento)
            =>
                (assert (diagnostico "Posible sobrecarga de programas o falta de RAM")))
            """ 
        ]
        for regla in reglas:
            self.env.build(regla)
    def resetear (self):
        self.env.reset()
        
    
        

        