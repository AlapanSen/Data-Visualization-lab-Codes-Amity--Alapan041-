"""
Q8 - Part 2: Fully User-Input Driven Animated Circle
Tkinter sidebar lets the user change Speed, Diameter, Color, Trail ON/OFF
in real-time while the circle moves with arrow keys.
"""

import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# ── App state ──────────────────────────────────────────────────────────────────
state = {
    'x': 0.0, 'y': 0.0,
    'speed': 0.04,
    'radius': 0.10,
    'color': 'royalblue',
    'trail': True,
    'trail_pts': [],
    'pressed': set()
}

COLORS_MAP = {
    'Royal Blue':  'royalblue',
    'Crimson':     'crimson',
    'Lime Green':  'limegreen',
    'Orange':      'orange',
    'Magenta':     'magenta',
    'Cyan':        'cyan',
    'Gold':        'gold',
    'White':       'white'
}
LIMITS = (-0.88, 0.88)

# ── Root tkinter window ────────────────────────────────────────────────────────
root = tk.Tk()
root.title("Q8 Part 2 – Animated Circle | User Controls")
root.configure(bg='#1a1a2e')
root.resizable(False, False)

# ── Matplotlib figure embedded in tkinter ─────────────────────────────────────
fig, ax = plt.subplots(figsize=(6, 6), facecolor='#1a1a2e')
ax.set_facecolor('#1a1a2e')
ax.set_xlim(-1, 1); ax.set_ylim(-1, 1)
ax.set_aspect('equal'); ax.set_xticks([]); ax.set_yticks([])
ax.set_title("Arrow Keys to Move", color='white', fontsize=10, pad=6)
for v in [-0.5, 0, 0.5]:
    ax.axhline(v, color='white', alpha=0.07, lw=0.7)
    ax.axvline(v, color='white', alpha=0.07, lw=0.7)

glow   = plt.Circle((0, 0), 0.13,  color='royalblue', alpha=0.2)
circle = plt.Circle((0, 0), 0.10,  color='royalblue', zorder=5)
ax.add_patch(glow)
ax.add_patch(circle)

trail_line, = ax.plot([], [], '-', color='royalblue',
                      alpha=0.35, lw=1.5, zorder=2)

info = ax.text(-0.97, -0.96, '', color='lightgray',
               fontsize=8, va='bottom', family='monospace')

canvas_widget = FigureCanvasTkAgg(fig, master=root)
canvas_widget.get_tk_widget().grid(row=0, column=0, rowspan=20, padx=6, pady=6)

# ── Sidebar (right column) ────────────────────────────────────────────────────
FONT_H = ('Helvetica', 10, 'bold')
FONT_L = ('Helvetica', 9)
FG, BG = 'white', '#16213e'

def label(text, row):
    tk.Label(root, text=text, fg=FG, bg=BG,
             font=FONT_L).grid(row=row, column=1, sticky='w', padx=(10,4), pady=2)

# Title
tk.Label(root, text="⚙  Controls", fg='#00d4ff', bg=BG,
         font=FONT_H).grid(row=0, column=1, columnspan=2, pady=(10,4))

# Speed slider
label("Speed", 1)
speed_var = tk.DoubleVar(value=0.04)
speed_sl  = ttk.Scale(root, from_=0.005, to=0.15,
                       variable=speed_var, orient='horizontal', length=160)
speed_sl.grid(row=2, column=1, columnspan=2, padx=10)
speed_val = tk.Label(root, text="0.040", fg=FG, bg=BG, font=FONT_L)
speed_val.grid(row=3, column=1, columnspan=2)

# Diameter slider
label("Diameter (radius)", 4)
diam_var = tk.DoubleVar(value=0.10)
diam_sl  = ttk.Scale(root, from_=0.02, to=0.40,
                      variable=diam_var, orient='horizontal', length=160)
diam_sl.grid(row=5, column=1, columnspan=2, padx=10)
diam_val = tk.Label(root, text="0.100", fg=FG, bg=BG, font=FONT_L)
diam_val.grid(row=6, column=1, columnspan=2)

# Color picker
label("Circle Color", 7)
color_var = tk.StringVar(value='Royal Blue')
color_menu = ttk.Combobox(root, textvariable=color_var,
                           values=list(COLORS_MAP.keys()), width=14, state='readonly')
color_menu.grid(row=8, column=1, columnspan=2, padx=10, pady=4)

# Trail toggle
trail_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text=" Show Trail", variable=trail_var,
               fg=FG, bg=BG, selectcolor='#0f3460', activebackground=BG,
               activeforeground=FG, font=FONT_L).grid(row=9, column=1, columnspan=2, pady=4)

# Reset button
def reset_circle():
    state['x'] = state['y'] = 0.0
    state['trail_pts'].clear()

tk.Button(root, text="⟳  Reset Position", command=reset_circle,
          bg='#0f3460', fg=FG, font=FONT_L, relief='flat',
          padx=8, pady=4).grid(row=10, column=1, columnspan=2, pady=4)

# ── Instructions ───────────────────────────────────────────────────────────────
instructions = """
⬆ ⬇ ⬅ ➡  Move circle
Sliders update live
Trail shows path
Reset clears trail
"""
tk.Label(root, text=instructions, fg='#aaaacc', bg=BG,
         font=('Helvetica', 8), justify='left').grid(
    row=11, column=1, columnspan=2, padx=10, pady=8)

# ── Key bindings on canvas ─────────────────────────────────────────────────────
def on_key_press(event):
    state['pressed'].add(event.keysym.lower())

def on_key_release(event):
    state['pressed'].discard(event.keysym.lower())

root.bind('<KeyPress>',   on_key_press)
root.bind('<KeyRelease>', on_key_release)

# ── Animation loop ─────────────────────────────────────────────────────────────
def update(_frame):
    # Read live slider / control values
    state['speed']  = speed_var.get()
    state['radius'] = diam_var.get()
    state['color']  = COLORS_MAP[color_var.get()]
    state['trail']  = trail_var.get()

    speed_val.config(text=f"{state['speed']:.3f}")
    diam_val.config(text=f"{state['radius']:.3f}")

    s, r = state['speed'], state['radius']
    lo, hi = LIMITS

    if 'left'  in state['pressed']: state['x'] = max(lo + r, state['x'] - s)
    if 'right' in state['pressed']: state['x'] = min(hi - r, state['x'] + s)
    if 'up'    in state['pressed']: state['y'] = min(hi - r, state['y'] + s)
    if 'down'  in state['pressed']: state['y'] = max(lo + r, state['y'] - s)

    cx, cy = state['x'], state['y']
    col = state['color']

    circle.center = glow.center = (cx, cy)
    circle.set_radius(r)
    glow.set_radius(r * 1.3)
    circle.set_color(col)
    glow.set_color(col)
    trail_line.set_color(col)

    if state['trail']:
        state['trail_pts'].append((cx, cy))
        if len(state['trail_pts']) > 300:
            state['trail_pts'].pop(0)
        if len(state['trail_pts']) > 1:
            xs, ys = zip(*state['trail_pts'])
            trail_line.set_data(xs, ys)
    else:
        state['trail_pts'].clear()
        trail_line.set_data([], [])

    info.set_text(
        f"X:{cx:+.2f} Y:{cy:+.2f} | "
        f"Speed:{s:.3f} | R:{r:.3f}"
    )
    canvas_widget.draw_idle()
    return circle, glow, trail_line, info

ani = animation.FuncAnimation(fig, update, interval=16, cache_frame_data=False)

root.mainloop()
