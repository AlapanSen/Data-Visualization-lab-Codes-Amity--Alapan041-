import matplotlib.pyplot as plt

n = int(input("Enter number of slices: "))

labels = []
sizes = []

for i in range(n):
    label = input(f"Enter label {i+1}: ")
    size = float(input(f"Enter size for {label}: "))
    labels.append(label)
    sizes.append(size)

plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.title("Pie Chart (User Input)")

plt.show()
