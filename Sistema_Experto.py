import clips

class SistemaExperto:
    def __init__(self):
        self.env = clips.Environment()
        self.reestablecer()

    def reestablecer(self):
        self.env.clear()

        self.build('(defrule reglaEnergia (energiaDesconectada) => (assert(revisarCableEnergia)))')
        # 2) Encendido del router
        self.build('(defrule reglaRouterApagado (routerApagado) (or (energiaDesconectada) (not (noInternet))) => (assert(encenderRouter)))')
        # 3) Señales del router
        self.build('(defrule reglaLucesRojas (lucesRojas) (not (routerApagado)) => (assert(revisarRouter)))')
        # 4) Conexión física y WiFi
        self.build('(defrule reglaEthernet (ethernetDesconectado) (noInternet) (not (energiaDesconectada)) (not (routerApagado)) => (assert(conectarCableEthernet)))')
        self.build('(defrule reglaWifi (wifiCaido) (noInternet) (not (energiaDesconectada)) (not (routerApagado)) => (assert(reiniciarModem)))')
        # 5) Resolución de nombres
        self.build('(defrule reglaDNS (dnsError) (noInternet) (not (energiaDesconectada)) (not (routerApagado)) => (assert(cambiarDNS)))')
        # 6) Escalación
        self.build('(defrule reglaGrave (wifiCaido) (dnsError) (noInternet) (not (energiaDesconectada)) (not (routerApagado)) => (assert(contactarProveedor)))')
        self.build('(defrule reglaRouterDanado (noInternet) (routerApagado) (not (energiaDesconectada)) => (assert(contactarProveedor)))')
        self.build('(defrule reglaProveedor (noInternet) (not (energiaDesconectada)) (not (routerApagado)) (not (lucesRojas)) (not (wifiCaido)) (not (dnsError)) (not (ethernetDesconectado)) => (assert(contactarProveedor)))')

    def agregarHecho(self, hecho: str):
        self.env.assert_string(f"({hecho})")
        #self.env.run() 

    def verHechos(self):
        return [f"f-{i} {fact}" for i, fact in enumerate(self.env.facts())]

    def verAgenda(self):
            return [f"{act.name}: f-{i}" for i,act in enumerate(self.env.activations())]

    def build(self, rule):
        self.env.build(rule)

    def reset(self):
        self.env.reset()

    def run(self):
        self.env.run()

    def diagnosticar_internet(self, hechos_seleccionados):
        """Método para diagnosticar problemas de internet"""
        self.reset()
        
        # Agregar hechos seleccionados
        for hecho in hechos_seleccionados:
            self.env.assert_string(f"({hecho})")
        
        # Obtener hechos antes de ejecutar
        hechos_antes = [str(fact) for fact in self.env.facts()]
        
        # Obtener reglas activadas antes de ejecutar
        reglas_activadas = []
        for act in self.env.activations():
            try:
                regla_pp = str(act.rule.pp_form).strip()
                if regla_pp.startswith("(") and regla_pp.endswith(")"):
                    regla_pp = regla_pp[1:-1]
                reglas_activadas.append(regla_pp)
            except Exception:
                reglas_activadas.append(f"- {act}")
        
        # Ejecutar el sistema
        self.run()
        
        # Obtener recomendaciones
        recomendaciones = []
        for fact in self.env.facts():
            f = str(fact)
            if "reiniciarModem" in f:
                recomendaciones.append("Reiniciar el router")
            if "cambiarDNS" in f:
                recomendaciones.append("Cambiar los DNS en la configuración")
            if "contactarProveedor" in f:
                recomendaciones.append("Contactar al proveedor de internet")
            if "encenderRouter" in f:
                recomendaciones.append("Revisa el cable de alimentación de energía")
            if "revisarRouter" in f:
                recomendaciones.append("Reiniciar el router")
            if "revisarCableEnergia" in f:
                recomendaciones.append("Revisar cable de energía y conectarlo correctamente")
            if "conectarCableEthernet" in f:
                recomendaciones.append("Conectar correctamente el cable Ethernet al módem y al equipo")
        
        return {
            'hechos': hechos_antes,
            'reglas_activadas': reglas_activadas,
            'recomendaciones': recomendaciones
        }
