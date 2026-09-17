# Central de Despachos

Programa de consola para administrar una operacion pequeña de logistica de transporte.

## Que incluye

* Catalogo de conductores con licencia, telefono y estado.

* Catalogo de unidades con capacidad, costo por kilometro y kilometraje.

* Rutas con origen, destino, distancia, velocidad y paradas.

* Programacion de viajes con fecha y hora de salida.

* Calculo de hora de llegada, duracion, carga y costo estimado.

* Validacion de capacidad, recursos inactivos, codigos repetidos y cruces de horario.

* Estados del viaje: programado, en ruta, completado y cancelado.

* Resumen operativo de kilometros, toneladas y costo.

* Datos de demostracion para que el programa muestre una ruta al iniciar.

## Estructura del proyecto

```
logistica_transporte.py    # lanzador compatible

logistica_mvc/
├── main.py                # punto de entrada
├── datos_demo.py          # informacion de demostracion
├── modelo/
│   ├── entidades.py       # Conductor, Unidad, Ruta y Viaje
│   └── centro_logistico.py# reglas y operaciones del negocio
├── vista/
│   └── consola.py         # menus, entradas y salidas
└── controlador/
    └── principal.py       # coordinacion entre vista y modelo
```

La aplicacion sigue el patron MVC: el modelo no imprime menus, la vista no aplica reglas del negocio y el controlador coordina las acciones del usuario.

## Ejecucion


En una terminal:

```
python -m logistica_mvc.main
```

Tambien se puede usar el lanzador corto:

```
