import matplotlib.pyplot as plt
import matplotlib.animation as animation

x = []
y = []

fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

line, = ax.plot([], [])

def update(frame):
    x.append(frame)
    y.append(frame)
    line.set_data(x, y)
    return line,

ani = animation.FuncAnimation(
    fig, update,
    frames=range(10),
    interval=500
)

plt.show()
