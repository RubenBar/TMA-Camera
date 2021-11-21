import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Consider to read a csv file
#pd.read_csv('file.csv')

#maxHours = 24
#hours = list(range(maxHours))

#rand_values = np.random.randint(0, 60, (1,24))
#rand_values = np.random.rand(23, 60)

#print("random_values", rand_values)

#print("hours", hours)

plotdata = pd.DataFrame(
    {"Minuts": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 3, 0, 8, 0, 2, 5, 0, 3, 0, 0, 0, 0]},
    index=["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]
)

#Plot a bar chart
plotdata.plot(kind="bar")

# Naming the x axis
plt.xlabel('Hour of the Day')
# Naming the y axis
plt.ylabel('Minutes using the Camera App')

# Giving a graph Title
plt.title('Pattern: App Activity during a Day')

# Function to show the plot
plt.show()