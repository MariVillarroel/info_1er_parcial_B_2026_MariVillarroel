# Infografia UPB I/2026 - 1er parcial B (Paint)

## Descripcion

Este repositorio contiene el codigo base para el proyecto de tipo B.

Implementa una version inicial de PAINT sobre `arcade`. El mecanismo de
dibujo esta basado en una lista de trazos: `self.traces` es una lista de
diccionarios, cada uno con la forma

```python
{"tool": TOOL_NAME, "color": COLOR, "trace": [(x0, y0), (x1, y1), ..., (xn, yn)]}
```

Usted debera completar el codigo fuente e implementar funcionalidades
adicionales.

## Requisitos y ejecucion

Este proyecto usa [uv](https://docs.astral.sh/uv/) para gestionar Python
y las dependencias. Una vez instalado uv:

```bash
git clone <su-fork>.git
cd info_1er_parcial_B_2026

uv run main.py
# o para cargar un dibujo guardado:
uv run main.py ruta/a/dibujo.json
```

Controles del codigo base:

- Click izquierdo + arrastre: dibujar con la herramienta activa.
- `1` / `2` / `3` / `4`: seleccionar herramienta (solo `1` esta cableada
  en el codigo base; las demas son su tarea).
- `A` / `S` / `D`: colores rojo / verde / azul.
- `O`: guardar dibujo (su tarea implementarlo).

## Tareas

### 1. Nuevas herramientas (`tool.py`)

Implemente las siguientes clases (stubs ya creados en `tool.py`). Todas
implementan el protocolo `Tool`.

- **MarkerTool** - como el lapiz pero con grosor mayor. El grosor es un
  argumento del `__init__` con un default razonable.

- **SprayTool** - en cada punto del trazo, dibuja N pixeles dispersos
  aleatoriamente dentro de un radio. N y el radio son argumentos del
  `__init__`.

- **EraserTool** - al pasar el cursor sobre los trazos, elimina los
  puntos que esten dentro de un radio. **No elimina trazos enteros**:
  solo los puntos cercanos al cursor. Considere que borrar un punto
  intermedio de un trazo abre un "hueco"; decida como manejarlo
  (sugerencia: partir el trazo en dos).

Ademas, en `main.py` debe cablear las teclas `2`, `3` y `4` a las nuevas
herramientas (los stubs `### KEY_2 -> ...` ya estan marcados).

### 2. Guardado y carga de dibujos

- **Guardado:** al presionar `O`, serialice `self.traces` a un archivo
  de texto. Use **JSON** (`json.dumps`). Decida usted el nombre del
  archivo o pidalo al usuario.

- **Carga:** al invocar el programa con un argumento de linea de
  comandos (`uv run main.py ruta/a/dibujo.json`), lea el archivo y
  pueble `self.traces` con su contenido. El programa debe renderizar
  inmediatamente el dibujo cargado. En este proyecto (Mariana Villarroel), el comando es "uv run main.py dibujo.json"

Nota: los colores de `arcade.color.*` son tuplas `(R, G, B)`; JSON los
serializa como listas. Asegurese de que la carga las re-convierta a
tuplas si es necesario.

### 3. (Extra) Interfaz grafica

Se considerara la implementacion de una interfaz grafica con botones
para cambiar herramientas y colores, y cualquier adicion de
funcionalidad.

## Criterios de evaluacion

Al revisar, ejecutaremos `uv run main.py` y verificaremos:

- [ ] El programa arranca sin errores.
- [ ] La herramienta `MarkerTool` dibuja trazos visiblemente mas
      gruesos que `PencilTool`, en el color seleccionado.
- [ ] La herramienta `SprayTool` dibuja varios pixeles dispersos por
      cada punto del trazo.
- [ ] La herramienta `EraserTool` elimina puntos cercanos al cursor
      sin eliminar el trazo completo (los huecos no producen lineas
      cruzadas).
- [ ] Al presionar `O`, se genera un archivo JSON con la lista de
      trazos.
- [ ] Invocar `uv run main.py ruta/al/archivo.json` restaura
      visualmente el dibujo guardado.
- [ ] El codigo se ejecuta sin agregar dependencias extra al
      `pyproject.toml`.
- [ ] (Extra) Interfaz grafica con botones funcionales.

## Reglas

- Solo puede usar la dependencia declarada en `pyproject.toml`
  (`arcade`) y modulos de la libreria estandar (`json`, `random`,
  `math`, etc.). No agregue `numpy`, `pygame`, `Pillow`, etc.
- No modifique la estructura del diccionario de trazos
  (`{"tool", "color", "trace"}`) sin justificacion; otras herramientas
  dependen de el.
- El codigo debe correr con `uv run main.py` sin pasos adicionales.

## Envio del codigo

Suba su trabajo a un fork publico de este repositorio. Envie UN solo
correo por grupo a:

- **Destinatario:** eduardo.laruta+tareas@gmail.com
- **Asunto:** `1era Evaluacion parcial Infografia - Grupo <nombres>`
- **Contenido:** nombres y codigos de los integrantes + enlace al
  repositorio.
