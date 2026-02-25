import matplotlib.pyplot as plt

n = int(input("Enter number of categories: "))

categories = []
values = []

for i in range(n):
    cat = input(f"Enter category {i+1}: ")
    val = int(input(f"Enter value for {cat}: "))
    categories.append(cat)
    values.append(val)

plt.bar(categories, values)
plt.title("Bar Chart (User Input)")
plt.xlabel("Categories")
plt.ylabel("Values")

plt.show()
