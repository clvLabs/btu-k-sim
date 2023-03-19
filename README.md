# btu-k-sim

Asistente avanzado de _batukación_

## Uso

### Teclas

#### Acciones _básicas_

|Tecla|Función|
|---|---|
|`ESC` / `q`|salir|
|`h`|mostrar/ocultar ayuda|
|`SPACE`|`play`/`pause`|
|`UP` / `DOWN`|anterior/siguiente sección|
|`PAGE_UP` / `PAGE_DOWN`|anterior/siguiente partitura|

#### Navegación

|Tecla|Función|
|---|---|
|`1`...`0`|ir a sección|
|`SHIFT` `1`...`0`|ir a sección (+10)|
|`LEFT` / `RIGHT`|cursor 1 negra izquierda/derecha|
|`SHIFT` `LEFT` / `RIGHT`|cursor 1 semicorchea izquierda/derecha|
|`HOME` / `END`|ir a inicio/fin de sección|

#### Control de reproducción

|Tecla|Función|
|---|---|
|`+` / `-`|más/menos `BPM` (+-5)|
|`SHIFT` `+` / `-`|más/menos `BPM` (+-10)|
|`ALT` `+` / `-`|más/menos `BPM` (+-1)|
|`F1`...`F12`|`mute` de un instrumento|
|`SHIFT` `F1`...`F12`|`solo` de un instrumento|
|`m`|`mute` (TODAS los instrumentos)|
|`j`|modo `jam`|
|`b`|modo `bolo`|
|`t`|metrónomo|

#### Otras acciones

|Tecla|Función|
|---|---|
|`i`|invertir orden de instrumentos|
|`r`|reset `mute`/`solo`/posición sección|
|`R`|reset `mute`/`solo`/posición TODAS las partituras|
|`w`|actualizar instrumentos/partituras|
|`CTRL` `+` / `-`|tamaño ventana +/- (10%)|
|`CTRL` `SHIFT` `+` / `-`|tamaño ventana +/- (30%)|

#### Cuando el modo `jam` está activo

|Tecla|Función|
|---|---|
|`1`...`0`|ir a sección cuando termine la sección actual|
|`SHIFT` 1...0|ir a sección (+10) cuando termine la sección actual|
|`CTRL` 1...0|ir a sección cuando termine el compás actual|
|`CTRL` `SHIFT` 1...0|ir a sección (+10) cuando termine el compás actual|
|`BACKSPACE`|Eliminar última sección preparada|

### Modo `jam`

Cuando está activo el modo `jam`:

* Al hacer un cambio de sección, en vez de hacer el cambio directamente se espera al final de la sección para hacer el cambio automáticamente.
* Usando la tecla `CTRL` se hace que la sección entre al próximo cambio de compás.
* Se pueden acumular secciones programadas y hacer una canción pulsando una secuencia de teclas.


### Modo `bolo`

En modo 'bolo' el simulador combina las partes de cada partitura para generar 'frases completas':

* Cuadra a 4 compases todas las secciones.
* Combina todas las bases con todas las variaciones.
* Añade marcas del director para los cambios.


## Configuración

En la misma carpeta donde se encuentra el programa está el archivo `config.yml`.

Este archivo se puede modificar para cambiar algunos valores de configuración.

### config.yml

```yml
auto_udpate:
  update_link: ''
display:
  size_factor: 1.0
simulator:
  bpm_increment: 5
  default_bpm: 100
```

* `auto_udpate`:
  * `update_link`: Link para actualizaciones automáticas.
* `display`:
  * `size_factor`: Factor de _zoom_ de la interface.
* `simulator`:
  * `default_bpm`: `BPM` por defecto.
  * `bpm_increment`: Incremento a usar al cambiar `BPM`.

## Desarrollo

Para crear un `.zip` con los archivos necesarios para funcionar en Windows, ejecutar desde la carpeta de proyecto:

```log
> python .\scripts\pack-windows-exe.py
```
