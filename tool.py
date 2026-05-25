import arcade
from typing import Protocol
import random 
import math 


class Tool(Protocol):
    """
    Protocolo que define las operaciones que una herramienta debe ofrecer.

    Cada herramienta concreta tiene un `name` unico que coincide con el
    valor "tool" de las entradas en la lista de trazos.
    """
    name: str

    def draw_traces(self, traces: list[dict]):
        ...

    def get_name(self):
        return self.name


class PencilTool(Tool):
    name = "PENCIL"

    def draw_traces(self, traces: list[dict]):
        for trace in traces:
            if trace["tool"] != self.name:
                continue
            if len(trace["trace"]) < 2:
                continue
            arcade.draw_line_strip(trace["trace"], trace["color"])


class MarkerTool(Tool):
    """
    Marcador. Similar al lapiz pero con un grosor mayor.

    El grosor debera ser un argumento al __init__ con un default razonable
    (por ejemplo 8 pixeles).

    Pista: arcade.draw_line_strip no soporta grosor directamente, pero
    `arcade.draw_lines` o `arcade.draw_line` si lo aceptan.
    """
    name = "MARKER"

    def __init__(self, thickness: int = 8):
        self.thickness = thickness

    def draw_traces(self, traces: list[dict]):
        for trace in traces:
            if trace["tool"] != self.name:
                continue
            
            points = trace["trace"]
            if len(points) < 2:
                continue

            for i in range(len(points) - 1):
                start_x, start_y = points[i]
                end_x, end_y = points[j := i + 1]
                arcade.draw_line(
                    start_x, 
                    start_y, 
                    end_x, 
                    end_y, 
                    trace["color"], 
                    line_width=self.thickness
                )


class SprayTool(Tool):
    """
    Spray. En cada punto del trazo dibuja N pixeles dispersos
    aleatoriamente dentro de un radio.

    El numero de pixeles por punto y el radio deberan ser argumentos al
    __init__ con defaults razonables (por ejemplo 12 pixeles dentro de un
    radio de 10).

    Pista: usar `random.uniform` para dispersar dentro del radio y
    `arcade.draw_point` para dibujar cada pixel.
    """
    name = "SPRAY"

    def __init__(self, count: int = 12, radius: float = 10.0):
        self.count = count
        self.radius = radius

    def draw_traces(self, traces: list[dict]):
        for trace in traces:
            if trace["tool"] != self.name:
                continue

            for center_x, center_y in trace["trace"]:
                random.seed(int(center_x * 1000 + center_y))
                
                for _ in range(self.count):
                    angle = random.uniform(0, 2 * math.pi)
                    r = self.radius * math.sqrt(random.uniform(0, 1))
                    
                    offset_x = r * math.cos(angle)
                    offset_y = r * math.sin(angle)
                    
                    arcade.draw_point(
                        center_x + offset_x, 
                        center_y + offset_y, 
                        trace["color"], 
                        size=2 
                    )
        
        random.seed(None)


class EraserTool(Tool):
    """
    Borrador. NO es una herramienta que dibuje: su efecto es modificar la
    lista de trazos al pasar el cursor sobre ellos.

    Comportamiento esperado:
    - Mientras el usuario arrastra el cursor con esta herramienta
      seleccionada, los PUNTOS de cualquier trazo que esten dentro de
      `radius` pixeles del cursor deben eliminarse.
    - El borrador NO elimina trazos enteros: solo los puntos cercanos.
    - Cuidado: si se elimina un punto en medio de un trazo, dibujarlo
      como una sola line_strip va a unir los extremos restantes con una
      linea cruzada incorrecta. Decida como manejar esto (por ejemplo,
      dividiendo el trazo en dos al borrar puntos intermedios).
    - El borrador no tiene draw_traces propio (no se dibuja a si mismo),
      pero puede necesitar un metodo extra para procesar la lista de
      trazos. La firma de ese metodo y como se invoca desde main.py
      forma parte del ejercicio.
    """
    name = "ERASER"

    def __init__(self, radius: float = 15.0):
        self.radius = radius

    def draw_traces(self, traces: list[dict]):
        # El borrador no dibuja nada 
        pass

    def erase(self, traces: list[dict], mouse_x: float, mouse_y: float):
        """
        Recorre la lista de trazos actual y remueve los puntos que estén 
        dentro del radio del borrador. Si se borra un punto intermedio,
        el trazo se divide en múltiples segmentos.
        """
        new_traces = []

        for trace in traces:
            current_sub_trace = []
            
            for x, y in trace["trace"]:
                distance = math.hypot(x - mouse_x, y - mouse_y)
                
                if distance <= self.radius:
                    if current_sub_trace:
                        new_traces.append({
                            "tool": trace["tool"],
                            "color": trace["color"],
                            "trace": current_sub_trace
                        })
                        current_sub_trace = []
                else:
                    current_sub_trace.append((x, y))
            
            if current_sub_trace:
                new_traces.append({
                    "tool": trace["tool"],
                    "color": trace["color"],
                    "trace": current_sub_trace
                })

        traces.clear()
        traces.extend(new_traces)
