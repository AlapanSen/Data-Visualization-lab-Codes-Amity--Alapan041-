import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
data = {
    "Name": ["A", "B", "C", "D", "E"], "Math": [90, np.nan, 75, 88, np.nan], 
    "Science": [np.nan, 85, 80, np.nan, 95], "English": [70, 78, np.nan, 82, 88]
}
df = pd.DataFrame(data)
print("Original Data:\n", df)
plt.figure()
plt.title("Missing Values Visualization")
plt.imshow(df.isnull())
plt.xticks(range(len(df.columns)), df.columns)
plt.yticks(range(len(df)), df["Name"])
plt.show()
df_filled = df.fillna(df.mean(numeric_only=True))

print("\nAfter Handling Missing Values:\n", df_filled)