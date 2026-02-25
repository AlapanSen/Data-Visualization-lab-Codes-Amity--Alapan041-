import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

circle = plt.Circle((0, 5), 0.5)
ax.add_patch(circle)

def update(frame):
    circle.center = (frame, 5)
    return circle,

ani = animation.FuncAnimation(
    fig, update,
    frames=range(0, 10),
    interval=500
)

plt.show()
