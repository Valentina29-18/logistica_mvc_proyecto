"""Entidades y reglas básicas del dominio de transporte."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


class EstadoViaje(str, Enum):
    PROGRAMADO = "Programado"
    EN_RUTA = "En ruta"
    COMPLETADO = "Completado"
    CANCELADO = "Cancelado"


@dataclass(slots=True)
class Conductor:
    identificacion: str
    nombre: str
    categoria_licencia: str
    telefono: str
    activo: bool = True


@dataclass(slots=True)
class Unidad:
    placa: str
    tipo: str
    capacidad_toneladas: float
    costo_por_km: float
    kilometraje: int = 0
    activa: bool = True


@dataclass(slots=True)
class Ruta:
    codigo: str
    origen: str
    destino: str
    distancia_km: float
    velocidad_promedio_kmh: float
    paradas: list[str] = field(default_factory=list)
    minutos_por_parada: int = 15

    def __post_init__(self) -> None:
        if self.distancia_km <= 0:
            raise ValueError("La distancia debe ser mayor que cero.")
        if self.velocidad_promedio_kmh <= 0:
            raise ValueError("La velocidad debe ser mayor que cero.")
        if self.minutos_por_parada < 0:
            raise ValueError("El tiempo de parada no puede ser negativo.")

    @property
    def minutos_estimados(self) -> int:
        movimiento = round(self.distancia_km / self.velocidad_promedio_kmh * 60)
        pausas = len(self.paradas) * self.minutos_por_parada
        return movimiento + pausas

    def llegada_estimada(self, salida: datetime) -> datetime:
        return salida + timedelta(minutes=self.minutos_estimados)

    def trayecto(self) -> str:
        return " -> ".join([self.origen, *self.paradas, self.destino])


@dataclass(slots=True)
class Viaje:
    codigo: str
    conductor: Conductor
    unidad: Unidad
    ruta: Ruta
    salida: datetime
    carga_toneladas: float
    estado: EstadoViaje = EstadoViaje.PROGRAMADO
    observacion: str = ""

    def __post_init__(self) -> None:
        if self.carga_toneladas <= 0:
            raise ValueError("La carga debe ser mayor que cero.")
        if self.carga_toneladas > self.unidad.capacidad_toneladas:
            raise ValueError("La carga supera la capacidad de la unidad.")

    @property
    def llegada(self) -> datetime:
        return self.ruta.llegada_estimada(self.salida)

    @property
    def costo_estimado(self) -> float:
        return self.ruta.distancia_km * self.unidad.costo_por_km

    @property
    def ventana_operativa(self) -> tuple[datetime, datetime]:
        return self.salida, self.llegada

    def ficha(self) -> str:
        return (
            f"Viaje {self.codigo} | {self.estado.value}\n"
            f"  Ruta: {self.ruta.trayecto()}\n"
            f"  Conductor: {self.conductor.nombre} | Unidad: {self.unidad.placa}\n"
            f"  Salida: {self.salida:%Y-%m-%d %H:%M} | "
            f"Llegada: {self.llegada:%Y-%m-%d %H:%M}\n"
            f"  Carga: {self.carga_toneladas:.1f} t | "
            f"Distancia: {self.ruta.distancia_km:.0f} km\n"
            f"  Costo estimado: COP {self.costo_estimado:,.0f}"
        )

