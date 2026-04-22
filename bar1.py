import matplotlib.pyplot as plt

categories = ['A', 'B', 'C', 'D']
values = [10, 25, 15, 30]

plt.bar(categories, values)
plt.title("Normal Bar Chart")
plt.xlabel("Categories")
plt.ylabel("Values")

plt.show()
