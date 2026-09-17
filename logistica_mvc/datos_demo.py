"""Datos iniciales para demostrar el funcionamiento de la aplicación."""

from datetime import datetime

from .modelo import CentroLogistico, Conductor, Ruta, Unidad


def cargar_datos_demo() -> CentroLogistico:
    centro = CentroLogistico()

    centro.registrar_conductor(
        Conductor("C-104", "Mariana Cardenas", "C2", "310 555 0184")
    )
    centro.registrar_conductor(
        Conductor("C-207", "Oscar Valdes", "C3", "315 555 0421")
    )

    centro.registrar_unidad(
        Unidad("LQX-482", "Camion rigido", 8.0, 2850, 184320)
    )
    centro.registrar_unidad(
        Unidad("RMT-719", "Furgon refrigerado", 5.0, 3400, 98750)
    )

    centro.registrar_ruta(
        Ruta(
            "R-01",
            "Bogota",
            "Ibague",
            205,
            62,
            ["Girardot", "Melgar"],
            minutos_por_parada=12,
        )
    )
    centro.registrar_ruta(
        Ruta("R-02", "Cali", "Pereira", 215, 58, ["Armenia"])
    )

    centro.programar_viaje(
        "V-1001",
        "C-104",
        "LQX-482",
        "R-01",
        datetime(2026, 9, 18, 6, 30),
        6.5,
        "Entrega de alimentos secos",
    )
    return centro

