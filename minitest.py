import tkinter as tk
import screen_brightness_control as sbc

# Initialize window
root = tk.Tk()
root.title("Drag to Control Brightness")
root.geometry("200x400")

canvas = tk.Canvas(root, width=200, height=400, bg="white")
canvas.pack()

# Draw vertical line
line_x = 100
canvas.create_line(line_x, 50, line_x, 350, fill="gray", width=2)

# Create draggable knob (circle)
knob = canvas.create_oval(line_x - 10, 200 - 10, line_x + 10, 200 + 10, fill="blue", outline="black")

# Initial brightness setup
try:
    current_brightness = sbc.get_brightness(display=0)[0]
except:
    current_brightness = 50

def set_knob_position_from_brightness():
    # Map brightness (0-100) to canvas Y (50-350)
    y = 350 - ((current_brightness / 100) * 300)
    canvas.coords(knob, line_x - 10, y - 10, line_x + 10, y + 10)

set_knob_position_from_brightness()

def on_drag(event):
    y = event.y
    y = max(50, min(350, y))  # Clamp y within line

    # Move knob
    canvas.coords(knob, line_x - 10, y - 10, line_x + 10, y + 10)

    # Map y to brightness
    brightness = int((350 - y) / 300 * 100)
    try:
        sbc.set_brightness(brightness, display=0)
    except Exception as e:
        print(f"Error: {e}")

    # Show brightness in title
    root.title(f"Brightness: {brightness}%")

# Bind drag motion
canvas.tag_bind(knob, "<B1-Motion>", on_drag)

root.mainloop()
