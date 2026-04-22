import matplotlib.pyplot as plt
n = int(input("Enter number of points: "))
x = []
y = []
for i in range(n):
    xi = float(input(f"Enter x{i+1}: "))
    yi = float(input(f"Enter y{i+1}: "))
    x.append(xi)
    y.append(yi)
plt.plot(x, y)
plt.title("Line Chart")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.show()
