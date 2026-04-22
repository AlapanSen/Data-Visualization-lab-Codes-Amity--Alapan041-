import matplotlib.pyplot as plt

# Data for line chart
x = [1, 2, 3, 4, 5]
y = [12, 18, 15, 22, 30]

# Data for boxplot
data = [7, 15, 22, 30, 18, 12, 25, 27, 19]

plt.figure(figsize=(10, 5))

# 🔹 Line Chart
plt.subplot(1, 2, 1)
plt.plot(x, y, marker='o')
plt.title("Line Chart")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")

# 🔹 Boxplot
plt.subplot(1, 2, 2)
plt.boxplot(data)
plt.title("Boxplot")

plt.tight_layout()
plt.show()
