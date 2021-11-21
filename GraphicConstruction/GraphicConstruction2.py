import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plotdata = pd.DataFrame(
    {"Minuts": [10, 5, 20, 8, 0, 40, 90]},
    index=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
)

#Plot a bar chart
plotdata.plot(kind="bar")

# Naming the x axis
plt.xlabel('Week Days')
# Naming the y axis
plt.ylabel('Minutes using the Camera App')

# Giving a graph Title
plt.title('Pattern: App Activity during the week')

# Function to show the plot
plt.show()