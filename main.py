import json
import arcade
from tool import PencilTool, MarkerTool, SprayTool, EraserTool

WIDTH = 800
HEIGHT = 600
TITLE = "Paint"

COLORS = {
    "black": arcade.color.BLACK,
    "red": arcade.color.RED,
    "blue": arcade.color.BLUE,
    "yellow": arcade.color.YELLOW,
    "green": arcade.color.GREEN,
}


class Paint(arcade.View):
    def __init__(self, load_path: str | None = None):
        super().__init__()
        self.background_color = arcade.color.WHITE
        
        # Inicializamos herramientas
        self.tool = PencilTool()
        self.used_tools = {
            "PENCIL": PencilTool(),
            "MARKER": MarkerTool(),
            "SPRAY": SprayTool(),
            "ERASER": EraserTool()
        }
        self.color = arcade.color.BLUE

        self.buttons = [
            {"text": "Lápiz",    "x": 100, "y": 30, "w": 90, "h": 40, "action": "PENCIL"},
            {"text": "Marcador", "x": 200, "y": 30, "w": 90, "h": 40, "action": "MARKER"},
            {"text": "Spray",    "x": 300, "y": 30, "w": 90, "h": 40, "action": "SPRAY"},
            {"text": "Borrador", "x": 400, "y": 30, "w": 90, "h": 40, "action": "ERASER"},
            {"text": "Guardar",  "x": 510, "y": 30, "w": 110, "h": 40, "action": "SAVE"}
        ]

        if load_path is not None:
            try:
                with open(load_path, "r", encoding="utf-8") as f:
                    loaded_traces = json.load(f)
                
                for trace in loaded_traces:
                    trace["color"] = tuple(trace["color"])
                    trace["trace"] = [(p[0], p[1]) for p in trace["trace"]]
                
                self.traces = loaded_traces
                print(f"Dibujo cargado exitosamente desde: {load_path}")
            except Exception as e:
                print(f"Error al cargar el archivo: {e}")
                self.traces = []
        else:
            self.traces = []

    def save_drawing(self):
        """Serializa los trazos actuales a un archivo JSON"""
        filename = "dibujo.json"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.traces, f, indent=4)
            print(f"¡Dibujo guardado exitosamente en '{filename}'!")
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.KEY_1:
            self.tool = self.used_tools["PENCIL"]
        elif symbol == arcade.key.KEY_2:
            self.tool = self.used_tools["MARKER"]
        elif symbol == arcade.key.KEY_3:
            self.tool = self.used_tools["SPRAY"]
        elif symbol == arcade.key.KEY_4:
            self.tool = self.used_tools["ERASER"]
            
        # Selección de color con teclas asd
        elif symbol == arcade.key.A:
            self.color = arcade.color.RED
        elif symbol == arcade.key.S:
            self.color = arcade.color.GREEN
        elif symbol == arcade.key.D:
            self.color = arcade.color.BLUE
        elif symbol == arcade.key.O:
            self.save_drawing()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if button == arcade.MOUSE_BUTTON_LEFT:
            for btn in self.buttons:
                left = btn["x"] - btn["w"] / 2
                right = btn["x"] + btn["w"] / 2
                bottom = btn["y"] - btn["h"] / 2
                top = btn["y"] + btn["h"] / 2
                
                if left <= x <= right and bottom <= y <= top:
                    if btn["action"] == "SAVE":
                        self.save_drawing()
                    else:
                        self.tool = self.used_tools[btn["action"]]
                        print(f"Herramienta seleccionada: {btn['action']}")
                    return  
           
            if y <= 60:
                return

            if self.tool.name == "ERASER":
                self.tool.erase(self.traces, x, y)
            else:
                self.traces.append({"tool": self.tool.name, "color": self.color, "trace": [(x, y)]})

    def on_mouse_drag(self, x: int, y: int, dx: int, dy: int, buttons: int, modifiers: int):
        if y <= 60:
            return

        if buttons == arcade.MOUSE_BUTTON_LEFT:
            if self.tool.name == "ERASER":
                self.tool.erase(self.traces, x, y)
            elif self.traces:
                self.traces[-1]["trace"].append((x, y))

    def on_draw(self):
        self.clear()
   
        for tool in self.used_tools.values():
            tool.draw_traces(self.traces)
  
        arcade.draw_rect_filled(
            arcade.XYWH(400, 30, 800, 60),  
            arcade.color.LIGHT_GRAY
        )
        
        for btn in self.buttons:
            if self.tool.name == btn["action"]:
                btn_color = arcade.color.GRAY
            else:
                btn_color = arcade.color.DARK_GRAY
                
            arcade.draw_rect_filled(
                arcade.XYWH(btn["x"], btn["y"], btn["w"], btn["h"]),
                btn_color
            )
            
            arcade.draw_text(
                btn["text"], 
                btn["x"], 
                btn["y"] - 5, 
                arcade.color.WHITE, 
                font_size=12, 
                anchor_x="center"
            )

    def save_drawing(self):
        """Función auxiliar para centralizar el guardado en JSON"""
        filename = "dibujo.json"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(self.traces, f, indent=4)
            print(f"¡Dibujo guardado exitosamente en '{filename}'!")
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")


if __name__ == "__main__":
    import sys
    window = arcade.Window(WIDTH, HEIGHT, TITLE)
    if len(sys.argv) > 1:
        app = Paint(sys.argv[1])
    else:
        app = Paint()
    window.show_view(app)
    arcade.run()
