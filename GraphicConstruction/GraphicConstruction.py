import numpy as np
import matplotlib.pyplot as plt

maxHours = 24

# x axis values
#x = [1,2,3,4,5,6,7,8,9, 10]
#x = range(maxHours)
# corresponding y axis values: hours watching app during a day
#y = [2,6,8,9,1,0,3,2,8,3]

weekDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
minutesPerDay = [10, 5, 20, 8, 0, 40, 90]

# Plotting the points
plt.plot(weekDays, minutesPerDay, color='green', linestyle='dashed', linewidth = 3, marker='o', markerfacecolor='blue', markersize=12)

# Setting x and y axis range
#plt.ylim(0,7)
#plt.xlim(0,100)

# Naming the x axis
plt.xlabel('Week Days')
# Naming the y axis
plt.ylabel('Minutes using the Camera App')

# Giving a graph Title
plt.title('Week Pattern')

# Function to show the plot
plt.show()
