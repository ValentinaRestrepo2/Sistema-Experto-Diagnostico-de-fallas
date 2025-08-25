import clips

class SistemaExperto:
    def __init__(self):
        self.env = clips.Environment()
        self.reestablecer()

    def reestablecer(self):
        self.env.clear()

        self.env.build('(defrule desfribilacion_urgente (riesgo ?nombre infarto) (anterior ?nombre infarto) => (assert (aplicar ?nombre desfribilacion_urgente)) (printout t "dar a " ?nombre " desfribilacion urgente." crlf))')
        self.env.build('(defrule riesgo_infarto (dolor ?nombre lado_izquierdo) (alta ?nombre presion_alterial) => (assert (riesgo ?nombre infarto)) (printout t ?nombre " corre riesgo infarto" crlf))')
        self.env.build('(defrule presion_alterial_alta (alta ?nombre presion_ocular) => (assert (alta ?nombre presion_alterial)) (printout t ?nombre " tiene la presión alterial alta" crlf))')
        self.env.build('(defrule esclerotico (paciente ?nombre sobrepeso fumador) => (assert (propenso ?nombre esclerosis)) (printout t ?nombre " es propenso a la esclerosis" crlf))')
        self.env.build('(defrule desfribilacion_general (propenso ?nombre esclerosis) (alta ?nombre presion_ocular) => (assert (aplicar ?nombre desfribilacion_general)) (printout t "dar a " ?nombre " desfribilacion general." crlf))')

    def agregarHecho(self, hecho: str):
        self.env.assert_string(f"({hecho})")
        #self.env.run() 

    def verHechos(self):
        return [f"f-{i} {fact}" for i, fact in enumerate(self.env.facts())]

    def verAgenda(self):
            return [f"{act.name}: f-{i}" for i,act in enumerate(self.env.activations())]
