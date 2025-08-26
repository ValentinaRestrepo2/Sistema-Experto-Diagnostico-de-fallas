import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

class SistemaDifuso:
    def __init__(self):

        # Variables difusas
        self.velocidad = ctrl.Antecedent(np.arange(0, 101, 1), 'velocidad')
        self.latencia = ctrl.Antecedent(np.arange(0, 201, 1), 'latencia')
        self.perdida = ctrl.Antecedent(np.arange(0, 21, 1), 'perdida')
        self.diagnostico = ctrl.Consequent(np.arange(0, 101, 1), 'diagnostico')

        #Configuración de las Membership Function
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

    def diagnosticar(self, vel, lat, per):
        # ---- Grados de pertenencia ----
        grados = {
            "velocidad": {
                "lenta": fuzz.interp_membership(self.velocidad.universe, self.velocidad['lenta'].mf, vel),
                "normal": fuzz.interp_membership(self.velocidad.universe, self.velocidad['normal'].mf, vel),
                "rapida": fuzz.interp_membership(self.velocidad.universe, self.velocidad['rapida'].mf, vel)
            },
            "latencia": {
                "baja": fuzz.interp_membership(self.latencia.universe, self.latencia['baja'].mf, lat),
                "media": fuzz.interp_membership(self.latencia.universe, self.latencia['media'].mf, lat),
                "alta": fuzz.interp_membership(self.latencia.universe, self.latencia['alta'].mf, lat)
            },
            "perdida": {
                "nula": fuzz.interp_membership(self.perdida.universe, self.perdida['nula'].mf, per),
                "leve": fuzz.interp_membership(self.perdida.universe, self.perdida['leve'].mf, per),
                "grave": fuzz.interp_membership(self.perdida.universe, self.perdida['grave'].mf, per)
            }
        }

        # Diagnoctico final
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

        return {
            "entradas": {"velocidad": vel, "latencia": lat, "perdida": per},
            "grados": grados,
            "valor": resultado,
            "texto": texto
           }
