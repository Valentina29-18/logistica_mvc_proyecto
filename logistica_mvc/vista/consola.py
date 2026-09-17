"""Vista de consola: toda la entrada y salida del usuario vive aquí."""

from __future__ import annotations

from typing import Iterable

from ..modelo import Conductor, EstadoViaje, Ruta, Unidad, Viaje


class VistaConsola:
    def mostrar_demostracion(self, viaje: Viaje) -> None:
        print("=" * 72)
        print("CENTRAL DE DESPACHOS - DEMOSTRACIÓN DE RUTA")
        print("=" * 72)
        print(viaje.ficha())
        print(
            "  Paradas planificadas:",
            " -> ".join(viaje.ruta.paradas) or "Directo",
        )
        print("=" * 72)

    def mostrar_menu(self) -> str:
        print(
            "\nMENÚ PRINCIPAL\n"
            "1. Consultar conductores\n"
            "2. Consultar unidades\n"
            "3. Consultar rutas\n"
            "4. Consultar viajes\n"
            "5. Registrar un viaje\n"
            "6. Cambiar estado de un viaje\n"
            "7. Ver resumen operativo\n"
            "0. Salir"
        )
        return input("Selecciona una opción: ").strip()

    def mostrar_conductores(self, conductores: Iterable[Conductor]) -> None:
        print("\nCONDUCTORES")
        for conductor in conductores:
            estado = "Activo" if conductor.activo else "Inactivo"
            print(
                f"  {conductor.identificacion}: {conductor.nombre} | "
                f"Licencia {conductor.categoria_licencia} | {estado}"
            )

    def mostrar_unidades(self, unidades: Iterable[Unidad]) -> None:
        print("\nUNIDADES")
        for unidad in unidades:
            estado = "Activa" if unidad.activa else "Inactiva"
            print(
                f"  {unidad.placa}: {unidad.tipo} | "
                f"Capacidad {unidad.capacidad_toneladas:.1f} t | {estado}"
            )

    def mostrar_rutas(self, rutas: Iterable[Ruta]) -> None:
        print("\nRUTAS DISPONIBLES")
        for ruta in rutas:
            print(
                f"  {ruta.codigo}: {ruta.trayecto()} | "
                f"{ruta.distancia_km:.0f} km | "
                f"duración aproximada {ruta.minutos_estimados} min"
            )

    def mostrar_viajes(self, viajes: Iterable[Viaje]) -> None:
        print("\nVIAJES PROGRAMADOS")
        lista = list(viajes)
        if not lista:
            print("  No hay viajes registrados.")
            return
        for viaje in lista:
            print(viaje.ficha())

    def mostrar_resumen(self, datos: dict[str, float]) -> None:
        print("\nRESUMEN OPERATIVO")
        print(f"  Conductores en catálogo: {datos['conductores']:.0f}")
        print(f"  Unidades registradas: {datos['unidades']:.0f}")
        print(f"  Rutas disponibles: {datos['rutas']:.0f}")
        print(f"  Viajes no cancelados: {datos['viajes']:.0f}")
        print(f"  Kilómetros planificados: {datos['kilometros']:.0f} km")
        print(f"  Carga planificada: {datos['carga']:.1f} t")
        print(f"  Costo estimado: COP {datos['costo']:,.0f}")

    def pedir_datos_viaje(
        self,
        conductores: Iterable[Conductor],
        unidades: Iterable[Unidad],
        rutas: Iterable[Ruta],
    ) -> dict[str, str]:
        print("\nNUEVO VIAJE")
        codigo = input("Código del viaje: ").strip()

        print(
            "Conductores:",
            ", ".join(f"{c.identificacion} ({c.nombre})" for c in conductores),
        )
        id_conductor = input("Identificación del conductor: ").strip()

        print("Unidades:", ", ".join(u.placa for u in unidades))
        placa = input("Placa de la unidad: ").strip()

        self.mostrar_rutas(rutas)
        codigo_ruta = input("Código de ruta: ").strip()

        fecha = input("Fecha de salida (AAAA-MM-DD): ").strip()
        hora = input("Hora de salida (HH:MM): ").strip()
        carga = input("Carga en toneladas: ").strip()

        return {
            "codigo": codigo,
            "id_conductor": id_conductor,
            "placa": placa,
            "codigo_ruta": codigo_ruta,
            "fecha": fecha,
            "hora": hora,
            "carga": carga,
        }

    def pedir_estado(self) -> tuple[str, int]:
        codigo = input("Código del viaje: ").strip().upper()
        opciones = list(EstadoViaje)
        for indice, estado in enumerate(opciones, start=1):
            print(f"{indice}. {estado.value}")
        seleccion = input("Nuevo estado: ").strip()
        return codigo, int(seleccion)

    def mostrar_mensaje(self, mensaje: str) -> None:
        print(mensaje)

