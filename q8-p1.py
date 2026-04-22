"""
Q8 - Part 1: Animated Circle with Keyboard Interaction
Controls: Arrow Keys = Move | W/S = Resize | R = Reset | Q = Quit
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.animation as animation

# ── State ──────────────────────────────────────────────────────────────────────
state = {
    'x': 0.0, 'y': 0.0,
    'radius': 0.08,
    'speed': 0.03,
    'color': 'royalblue',
    'pressed': set()
}

LIMITS = (-0.9, 0.9)

# ── Figure setup ───────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(-1, 1)
ax.set_ylim(-1, 1)
ax.set_aspect('equal')
ax.set_facecolor('#1a1a2e')
fig.patch.set_facecolor('#16213e')
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("⬆⬇⬅➡  Move  |  W/S  Resize  |  R  Reset  |  Q  Quit",
             color='white', fontsize=11, pad=10)

# Grid lines (faint)
for v in [-0.5, 0, 0.5]:
    ax.axhline(v, color='white', alpha=0.08, lw=0.8)
    ax.axvline(v, color='white', alpha=0.08, lw=0.8)

# Glow ring + solid circle
glow = plt.Circle((0, 0), 0.10, color='royalblue', alpha=0.25)
circle = plt.Circle((0, 0), 0.08, color='royalblue', zorder=5)
ax.add_patch(glow)
ax.add_patch(circle)

info_text = ax.text(-0.98, -0.97, '', color='white',
                    fontsize=9, va='bottom', family='monospace')

# ── Key handlers ───────────────────────────────────────────────────────────────
def on_press(event):
    if event.key:
        state['pressed'].add(event.key)
    if event.key == 'r':
        state['x'] = state['y'] = 0.0
        state['radius'] = 0.08
    if event.key == 'q':
        plt.close()

def on_release(event):
    state['pressed'].discard(event.key)

fig.canvas.mpl_connect('key_press_event', on_press)
fig.canvas.mpl_connect('key_release_event', on_release)

# ── Animation update ───────────────────────────────────────────────────────────
def update(_frame):
    s, r = state['speed'], state['radius']
    lo, hi = LIMITS

    if 'left'  in state['pressed']: state['x'] = max(lo + r, state['x'] - s)
    if 'right' in state['pressed']: state['x'] = min(hi - r, state['x'] + s)
    if 'up'    in state['pressed']: state['y'] = min(hi - r, state['y'] + s)
    if 'down'  in state['pressed']: state['y'] = max(lo + r, state['y'] - s)
    if 'w'     in state['pressed']: state['radius'] = min(0.35, r + 0.005)
    if 's'     in state['pressed']: state['radius'] = max(0.02, r - 0.005)

    cx, cy, cr = state['x'], state['y'], state['radius']
    circle.center = glow.center = (cx, cy)
    circle.set_radius(cr)
    glow.set_radius(cr * 1.25)

    info_text.set_text(
        f"X: {cx:+.2f}  Y: {cy:+.2f}  "
        f"R: {cr:.3f}  Speed: {s:.3f}"
    )
    return circle, glow, info_text

ani = animation.FuncAnimation(fig, update, interval=16,
                               blit=True, cache_frame_data=False)

plt.tight_layout()
plt.show()
