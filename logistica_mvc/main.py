"""Punto de entrada de la aplicación MVC."""

from .controlador import ControladorPrincipal
from .datos_demo import cargar_datos_demo
from .vista import VistaConsola


def main() -> None:
    centro = cargar_datos_demo()
    vista = VistaConsola()
    controlador = ControladorPrincipal(centro, vista)
    controlador.iniciar()


if __name__ == "__main__":
    main()

