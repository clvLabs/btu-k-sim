# btu-k-sim

Asistente avanzado de _batukación_

## Uso

### Teclas

Funciones _básicas_:

|Tecla|Función|
|---|---|
|ESC / q|salir|
|? / h|mostrar ayuda|
|SPACE|play/pause|
|UP|anterior sección|
|DOWN|siguiente sección|
|PAGE_UP|anterior partitura|
|PAGE_DOWN|siguiente partitura|
|1...0|ir a sección|
|SHIFT+1...0|ir a sección (+10)|
|F1...F12|mute de una pista|
|SHIFT+F1...F12|solo de una pista|
|m|mute (TODAS las pistas)|
|+|más BPM|
|-|menos BPM|
|j|modo _jam_|
|t|metrónomo|
|w|actualizar instrumentos/partituras|

Funciones _avanzadas_:

|Tecla|Función|
|---|---|
|SHIFT++|más BPM (*2)|
|SHIFT+-|menos BPM (*2)|
|ALT++|más BPM (+1)|
|ALT+-|menos BPM (-1)|
|i|invertir orden de pistas|
|r|reset mute/solo/posición sección|
|R|reset mute/solo/posición TODAS las partituras|
|LEFT|mover cursor 1 negra izquierda|
|RIGHT|mover cursor 1 negra derecha|
|SHIFT+LEFT|mover cursor 1 semicorchea izquierda|
|SHIFT+RIGHT|mover cursor 1 semicorchea derecha|
|HOME|ir a inicio de sección|
|END|ir a fin de sección|

Cuando el modo `jam` está activo:

|Tecla|Función|
|---|---|
|1...0|ir a sección cuando termine la sección actual|
|SHIFT+1...0|ir a sección (+10) cuando termine la sección actual|
|CTRL+1...0|ir a sección cuando termine el compás actual|
|CTRL+SHIFT+1...0|ir a sección (+10) cuando termine el compás actual|
|BACKSPACE|Eliminar última sección preparada|

### Modo `jam`

Cuando está activo el modo `jam`:

* Los indicadores de posición y conteo de compases/frases no se reinician al llegar al final de la sección.
* Los cambios de sección se hacen _programados_, en vez de cambiar directamente esperan al final de sección/compás.

## Instalación

Una vez instalado el programa, hasta que no se configure un link para actualizaciones, el programa dará un error:

```log
Intentando descargar actualizaciones
- Descargando actualizaciones de recursos
  - No hay actualizaciones disponibles
```

Al haber ejecutado como mínimo una vez el programa, se habrá creado el archivo `config.yml` y se podrá editar para añadir el link de actualizaciones.

## Configuración

En la misma carpeta donde se encuentra el programa está el archivo `config.yml`.

Este archivo se puede modificar para cambiar algunos valores de configuración.

### config.yml

```yml
auto_udpate:
  update_link: ''
simulator:
  bpm_increment: 5
  default_bpm: 100
```

* `auto_udpate`:
  * `update_link`: Link para actualizaciones automáticas.
* `simulator`:
  * `default_bpm`: BPM por defecto.
  * `bpm_increment`: Incremento a usar al cambiar BPM.

## Desarrollo

Para crear un `.zip` con los archivos necesarios para funcionar en Windows, ejecutar desde la carpeta de proyecto:

```log
> python .\scripts\pack-windows-exe.py
```
