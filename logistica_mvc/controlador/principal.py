"""Controlador principal: coordina la vista y el servicio del modelo."""

from __future__ import annotations

from datetime import datetime

from ..modelo import CentroLogistico, EstadoViaje
from ..vista import VistaConsola


class ControladorPrincipal:
    def __init__(self, centro: CentroLogistico, vista: VistaConsola) -> None:
        self.centro = centro
        self.vista = vista

    def iniciar(self) -> None:
        self.vista.mostrar_demostracion(self.centro.viajes["V-1001"])

        while True:
            opcion = self.vista.mostrar_menu()
            if opcion == "0":
                self.vista.mostrar_mensaje("Programa finalizado.")
                return
            acciones = {
                "1": self._consultar_conductores,
                "2": self._consultar_unidades,
                "3": self._consultar_rutas,
                "4": self._consultar_viajes,
                "5": self._registrar_viaje,
                "6": self._cambiar_estado,
                "7": self._mostrar_resumen,
            }
            accion = acciones.get(opcion)
            if accion is None:
                self.vista.mostrar_mensaje("Opción no válida.")
            else:
                accion()

    def _consultar_conductores(self) -> None:
        self.vista.mostrar_conductores(self.centro.conductores.values())

    def _consultar_unidades(self) -> None:
        self.vista.mostrar_unidades(self.centro.unidades.values())

    def _consultar_rutas(self) -> None:
        self.vista.mostrar_rutas(self.centro.rutas.values())

    def _consultar_viajes(self) -> None:
        self.vista.mostrar_viajes(self.centro.viajes.values())

    def _registrar_viaje(self) -> None:
        datos = self.vista.pedir_datos_viaje(
            self.centro.conductores.values(),
            self.centro.unidades.values(),
            self.centro.rutas.values(),
        )
        try:
            salida = datetime.strptime(
                f"{datos['fecha']} {datos['hora']}",
                "%Y-%m-%d %H:%M",
            )
            carga = float(datos["carga"].replace(",", "."))
            viaje = self.centro.programar_viaje(
                datos["codigo"],
                datos["id_conductor"],
                datos["placa"],
                datos["codigo_ruta"],
                salida,
                carga,
            )
            self.vista.mostrar_mensaje(
                "\nViaje creado correctamente.\n" + viaje.ficha()
            )
        except ValueError as error:
            self.vista.mostrar_mensaje(f"No se pudo crear el viaje: {error}")

    def _cambiar_estado(self) -> None:
        try:
            codigo, seleccion = self.vista.pedir_estado()
            opciones = list(EstadoViaje)
            if not 1 <= seleccion <= len(opciones):
                raise ValueError("El número de estado no existe.")
            self.centro.cambiar_estado(codigo, opciones[seleccion - 1])
            self.vista.mostrar_mensaje("Estado actualizado.")
        except ValueError as error:
            self.vista.mostrar_mensaje(f"No se pudo actualizar: {error}")

    def _mostrar_resumen(self) -> None:
        self.vista.mostrar_resumen(self.centro.resumen())

