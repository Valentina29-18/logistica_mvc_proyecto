"""Servicio de aplicación que coordina los recursos logísticos."""

from __future__ import annotations

from datetime import datetime

from .entidades import Conductor, EstadoViaje, Ruta, Unidad, Viaje


class CentroLogistico:
    """Mantiene catálogos y aplica las reglas al programar despachos."""

    def __init__(self) -> None:
        self.conductores: dict[str, Conductor] = {}
        self.unidades: dict[str, Unidad] = {}
        self.rutas: dict[str, Ruta] = {}
        self.viajes: dict[str, Viaje] = {}

    def registrar_conductor(self, conductor: Conductor) -> None:
        self._registrar_unico(self.conductores, conductor.identificacion, "conductor")
        self.conductores[conductor.identificacion] = conductor

    def registrar_unidad(self, unidad: Unidad) -> None:
        unidad.placa = unidad.placa.upper()
        self._registrar_unico(self.unidades, unidad.placa, "unidad")
        self.unidades[unidad.placa] = unidad

    def registrar_ruta(self, ruta: Ruta) -> None:
        ruta.codigo = ruta.codigo.upper()
        self._registrar_unico(self.rutas, ruta.codigo, "ruta")
        self.rutas[ruta.codigo] = ruta

    def programar_viaje(
        self,
        codigo: str,
        id_conductor: str,
        placa: str,
        codigo_ruta: str,
        salida: datetime,
        carga_toneladas: float,
        observacion: str = "",
    ) -> Viaje:
        codigo = codigo.upper()
        placa = placa.upper()
        codigo_ruta = codigo_ruta.upper()
        self._registrar_unico(self.viajes, codigo, "viaje")

        conductor = self._buscar(self.conductores, id_conductor, "conductor")
        unidad = self._buscar(self.unidades, placa, "unidad")
        ruta = self._buscar(self.rutas, codigo_ruta, "ruta")

        if not conductor.activo:
            raise ValueError("El conductor seleccionado no esta activo.")
        if not unidad.activa:
            raise ValueError("La unidad seleccionada no esta activa.")
        if self._tiene_solapamiento(conductor, unidad, salida, ruta):
            raise ValueError("El conductor o la unidad ya tienen un viaje en ese horario.")

        viaje = Viaje(
            codigo,
            conductor,
            unidad,
            ruta,
            salida,
            carga_toneladas,
            observacion=observacion,
        )
        self.viajes[codigo] = viaje
        return viaje

    def cambiar_estado(self, codigo: str, nuevo_estado: EstadoViaje) -> None:
        viaje = self._buscar(self.viajes, codigo.upper(), "viaje")
        if viaje.estado == EstadoViaje.CANCELADO and nuevo_estado != EstadoViaje.CANCELADO:
            raise ValueError("Un viaje cancelado no puede reactivarse.")
        viaje.estado = nuevo_estado

    def viajes_activos(self) -> list[Viaje]:
        return [
            viaje for viaje in self.viajes.values()
            if viaje.estado != EstadoViaje.CANCELADO
        ]

    def resumen(self) -> dict[str, float]:
        activos = self.viajes_activos()
        return {
            "conductores": len(self.conductores),
            "unidades": len(self.unidades),
            "rutas": len(self.rutas),
            "viajes": len(activos),
            "kilometros": sum(v.ruta.distancia_km for v in activos),
            "carga": sum(v.carga_toneladas for v in activos),
            "costo": sum(v.costo_estimado for v in activos),
        }

    @staticmethod
    def _registrar_unico(registro: dict, clave: str, concepto: str) -> None:
        if clave in registro:
            raise ValueError(f"Ya existe ese {concepto}: {clave}.")

    @staticmethod
    def _buscar(registro: dict, clave: str, concepto: str):
        if clave not in registro:
            raise ValueError(f"No existe el {concepto} solicitado: {clave}.")
        return registro[clave]

    def _tiene_solapamiento(
        self,
        conductor: Conductor,
        unidad: Unidad,
        salida: datetime,
        ruta: Ruta,
    ) -> bool:
        llegada = ruta.llegada_estimada(salida)
        for viaje in self.viajes_activos():
            usa_recurso = viaje.conductor is conductor or viaje.unidad is unidad
            if not usa_recurso:
                continue
            inicio, fin = viaje.ventana_operativa
            if salida < fin and llegada > inicio:
                return True
        return False

